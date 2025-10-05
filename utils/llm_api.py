# FILE: utils/llm_api.py

import os
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace

# Get the Hugging Face API token from environment variables
API_TOKEN = os.getenv("HUGGING_FACE_HUB_TOKEN")
if not API_TOKEN:
    raise ValueError("HUGGING_FACE_HUB_TOKEN environment variable not set!")

Repo_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

def get_chat_model():
    """
    Initializes and returns a ChatHuggingFace instance configured for our needs.
    This function centralizes the LLM configuration.
    """
    # First, define the endpoint that points to our chosen model
    llm = HuggingFaceEndpoint(
        huggingfacehub_api_token=API_TOKEN,
        model=Repo_ID,
        task="text-generation",
        max_new_tokens=4096,
        temperature=0.5, # A bit of creativity, but still mostly factual
        repetition_penalty=1.2,
    )
    
    # Wrap the endpoint in the ChatHuggingFace class for a standardized chat interface
    model = ChatHuggingFace(llm=llm)
    return model

def query_huggingface_api(prompt: str) -> str:
    """
    Sends a prompt to the Hugging Face API using the LangChain ChatHuggingFace wrapper.
    This replaces the manual requests.post logic.

    Args:
        prompt (str): The prompt to send to the model.

    Returns:
        str: The generated text from the model.
    """
    try:
        # Get a configured model instance
        chat_model = get_chat_model()
        
        # The .invoke() method handles the API call, retries, and parsing.
        # The result is a message object, so we access its .content attribute.
        response_message = chat_model.invoke(prompt)
        
        # If content is a list, join string elements; otherwise, just use as is
        content = response_message.content
        if isinstance(content, list):
            # Join all string elements, ignore dicts or non-strings
            text = " ".join([str(item) for item in content if isinstance(item, str)])
        else:
            text = str(content)
        return text.strip()
        
    except Exception as e:
        print(f"❌ An error occurred during the API call: {e}")
        # Reraise the exception so the calling node is aware of the failure.
        raise