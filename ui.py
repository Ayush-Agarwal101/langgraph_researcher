# FILE: ui.py

import streamlit as st
from dotenv import load_dotenv
import sys
import os
import pprint

# This allows the script to find and import the 'graph' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Load environment variables from your .env file
load_dotenv()

# Import the compiled LangGraph app
try:
    from graph import app
except ImportError:
    st.error(
        "Failed to import the graph application. "
        "Ensure this script is in the project's root directory and all dependencies are installed."
    )
    st.stop()

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Autonomous Scientific Researcher", layout="wide")
st.title("🔬 Autonomous Scientific Researcher")

# --- Main Application Logic ---

# Use session state to store the final result to avoid rerunning on every interaction
if "final_state" not in st.session_state:
    st.session_state.final_state = None

# Sidebar for user input
with st.sidebar:
    st.header("Research Configuration")
    topic = st.text_input(
        "Enter the research topic:",
        "The use of mobile devices by advanced learners for English language study"
    )
    start_button = st.button("Start Research", type="primary", use_container_width=True)

# Main panel for displaying results
if start_button:
    # Clear previous results when starting a new run
    st.session_state.final_state = None
    
    if not topic:
        st.warning("Please enter a research topic to begin.")
    else:
        inputs = {"topic": topic, "loop_count": 0}
        
        # Stream the graph execution and display live updates
        with st.spinner("The agent is thinking... This will take several minutes."):
            try:
                for output in app.stream(inputs):
                    for key, value in output.items():
                        with st.status(f"Executing Node: {key.replace('_', ' ').title()}", state="running", expanded=True) as status:
                            if key == "retriever":
                                status.write("Finding relevant documents from the corpus...")
                            elif key == "knowledge_graph_updater":
                                status.write("Extracting entities and updating the knowledge graph...")
                            elif key == "hypothesis_generator":
                                status.write("Formulating a novel hypothesis...")
                                st.markdown("**Generated Hypothesis:**")
                                st.markdown(value['hypothesis'])
                            elif key == "experiment_designer":
                                status.write("Designing a new experiment...")
                                st.markdown("**Experiment Plan:**")
                                st.json(value['experiment_plan'])
                            elif key == "code_synthesizer":
                                status.write("Generating experiment code...")
                                st.markdown("**Generated Code:**")
                                st.code(value['code'], language="python")
                            elif key == "sandbox_runner":
                                status.write("Running experiment in a secure sandbox...")
                                st.markdown("**Experiment Results:**")
                                st.json(value['results'])
                            elif key == "analyzer":
                                status.write("Analyzing results...")
                                st.markdown("**Analysis:**")
                                st.markdown(value['analysis'])
                            elif key == "reviewer":
                                status.write(f"Reviewing the results...")
                                st.markdown(f"**Decision:** The reviewer decided to **{value['decision']}**.")
                                if value['decision'] == 'redesign':
                                    status.update(label="Redesigning Experiment...", state="running")
                            
                            status.update(label=f"Node '{key.replace('_', ' ').title()}' completed!", state="complete", expanded=False)

                    # Store the final state when the process ends
                    if "__end__" in output:
                        st.session_state.final_state = output["__end__"]

            except Exception as e:
                st.error(f"An error occurred during the research process: {e}")

# Display the final, complete results once the run is finished
if st.session_state.final_state:
    st.success("Research process completed successfully!")
    
    st.markdown("---")
    st.subheader("Final Research Paper")
    
    # Display the paper if it was generated
    if "paper" in st.session_state.final_state and st.session_state.final_state["paper"]:
        st.markdown(st.session_state.final_state["paper"])
    else:
        st.warning("The process finished, but no paper was generated (this can happen if the review loop maxed out).")

    # Optionally display the full final state for debugging
    with st.expander("Show Full Final State (for debugging)"):
        st.json(st.session_state.final_state)