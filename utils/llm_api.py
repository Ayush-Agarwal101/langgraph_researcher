# FILE: utils/llm_api.py

import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

API_TOKEN = os.getenv("HUGGING_FACE_HUB_TOKEN")
if not API_TOKEN:
    raise ValueError("HUGGING_FACE_HUB_TOKEN environment variable not set!")

# UPDATED: Switched back to a highly compatible and powerful model
REPO_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

def get_chat_model():
    """Initializes and returns a ChatHuggingFace instance."""
    llm = HuggingFaceEndpoint(
        huggingfacehub_api_token=API_TOKEN,
        repo_id=REPO_ID,
        task="text-generation",
        max_new_tokens=4096,
        temperature=0.5,
        repetition_penalty=1.2,
    )
    model = ChatHuggingFace(llm=llm)
    return model

def query_huggingface_api(prompt: str) -> str:
    """Sends a prompt to the Hugging Face API using the LangChain wrapper."""
    try:
        chat_model = get_chat_model()
        response_message = chat_model.invoke(prompt)
        
        if isinstance(response_message.content, list):
            contents = []
            for item in response_message.content:
                if isinstance(item, str):
                    contents.append(item)
                elif isinstance(item, dict) and "text" in item:
                    contents.append(item["text"])
            return " ".join(contents).strip()
        else:
            return str(response_message.content).strip()
            
    except Exception as e:
        print(f"❌ An error occurred during the API call: {e}")
        raise