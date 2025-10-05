# FILE: ui.py

import streamlit as st
from dotenv import load_dotenv
import sys
import os
import pprint
import shutil

# This allows the script to find and import the 'graph' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Load environment variables
load_dotenv()

# LangChain imports for the ingestion process
from langchain_community.document_loaders import PyMuPDFLoader # More robust for single files
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Import the compiled LangGraph app
try:
    from graph import app
except ImportError:
    st.error("Failed to import the graph application. Ensure this script is in the project's root directory.")
    st.stop()

# --- Constants and Directories ---
PERSISTENT_CORPUS_PATH = "persistent_corpus"
FAISS_INDEXES_PATH = "faiss_indexes" # Stores a permanent index for each PDF
TEMP_FAISS_PATH = "faiss_index" # A temporary, merged index for the current run

# Ensure directories exist
os.makedirs(PERSISTENT_CORPUS_PATH, exist_ok=True)
os.makedirs(FAISS_INDEXES_PATH, exist_ok=True)

# --- Helper Functions ---
def get_existing_pdfs():
    """Scans the persistent corpus for existing PDF files."""
    return [f for f in os.listdir(PERSISTENT_CORPUS_PATH) if f.endswith(".pdf")]

def get_faiss_index_path(file_name):
    """Generates a unique path for a file's FAISS index."""
    return os.path.join(FAISS_INDEXES_PATH, f"{file_name}.faiss")

def process_selected_files(selected_files):
    """
    Loads pre-built indexes for existing files and creates new ones for new files.
    Merges them into a single temporary index for the current run.
    """
    with st.spinner("Processing selected documents... This may take a moment."):
        # 1. Clean up the temporary merged index from the last run
        if os.path.exists(TEMP_FAISS_PATH):
            shutil.rmtree(TEMP_FAISS_PATH)
        
        individual_indexes = []
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        for file_name in selected_files:
            index_path = get_faiss_index_path(file_name)
            
            # 2. If a pre-built index exists, load it
            if os.path.exists(index_path):
                st.write(f"Loading pre-built index for {file_name}...")
                db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
                individual_indexes.append(db)
            
            # 3. If not, create a new index and save it
            else:
                st.write(f"Creating new index for {file_name}...")
                file_path = os.path.join(PERSISTENT_CORPUS_PATH, file_name)
                
                loader = PyMuPDFLoader(file_path)
                documents = loader.load()
                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
                docs = text_splitter.split_documents(documents)

                db = FAISS.from_documents(docs, embeddings)
                db.save_local(index_path) # Save the individual index permanently
                individual_indexes.append(db)
        
        if not individual_indexes:
            st.error("No documents were processed.")
            return False

        # 4. Merge all loaded/created indexes into one
        st.write("Merging indexes for the current session...")
        merged_db = individual_indexes[0]
        for i in range(1, len(individual_indexes)):
            merged_db.merge_from(individual_indexes[i])
        
        # 5. Save the final merged index to the temporary path that the agent uses
        merged_db.save_local(TEMP_FAISS_PATH)
        
        st.success("✅ Documents processed and ready for research!")
        return True

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Autonomous Scientific Researcher", layout="wide")
st.title("🔬 Autonomous Scientific Researcher")

# --- Main Application Logic ---
# (The rest of the UI code remains largely the same)
if "final_state" not in st.session_state:
    st.session_state.final_state = None

with st.sidebar:
    st.header("1. Select & Upload Documents")
    existing_pdfs = get_existing_pdfs()
    
    selected_existing_files = st.multiselect(
        "Select from previously uploaded PDFs:",
        options=existing_pdfs
    ) if existing_pdfs else []

    newly_uploaded_files = st.file_uploader(
        "Or upload new PDFs:",
        type="pdf",
        accept_multiple_files=True
    )

    st.header("2. Enter Topic")
    topic = st.text_input("Enter the research topic:", "")
    
    start_button = st.button("Start Research", type="primary", use_container_width=True)

if start_button:
    st.session_state.final_state = None
    
    if newly_uploaded_files:
        with st.spinner("Saving new files..."):
            for uploaded_file in newly_uploaded_files:
                if uploaded_file.name not in selected_existing_files:
                    selected_existing_files.append(uploaded_file.name)
                with open(os.path.join(PERSISTENT_CORPUS_PATH, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success("New files uploaded and saved!")
    
    if not selected_existing_files:
        st.warning("Please select or upload at least one PDF document.")
    elif not topic:
        st.warning("Please enter a research topic.")
    else:
        ingestion_success = process_selected_files(selected_existing_files)
        
        if ingestion_success:
            inputs = {"topic": topic, "loop_count": 0}
            
            with st.spinner("The agent is thinking..."):
                try:
                    for output in app.stream(inputs):
                        for key, value in output.items():
                            with st.status(f"Executing Node: {key.replace('_', ' ').title()}", state="running", expanded=False) as status:
                                status.update(label=f"Node '{key.replace('_', ' ').title()}' completed!", state="complete")
                        if "__end__" in output:
                            st.session_state.final_state = output["__end__"]
                except Exception as e:
                    st.error(f"An error occurred during the research process: {e}")

if st.session_state.final_state:
    st.success("Research process completed successfully!")
    st.markdown("---")
    st.subheader("Final Research Paper")
    if "paper" in st.session_state.final_state and st.session_state.final_state["paper"]:
        st.markdown(st.session_state.final_state["paper"])
    else:
        st.warning("The process finished, but no paper was generated.")