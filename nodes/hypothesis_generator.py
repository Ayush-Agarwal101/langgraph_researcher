# FILE: nodes/hypothesis_generator.py

from typing import Dict, Any
from utils.llm_api import query_huggingface_api

def hypothesis_generator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: HYPOTHESIS GENERATOR---")
    documents = state.get("documents", [])
    context = "\n\n---\n\n".join(documents)

    prompt = f"""
    You are a senior research scientist. Based on the following research context, identify a knowledge gap and formulate a single, clear, testable scientific hypothesis.

    **Research Context:**
    {context}

    **Your Output:**
    Provide only the formulated hypothesis as a single sentence.
    Hypothesis:
    """

    print("🧠 Generating hypothesis...")
    hypothesis = query_huggingface_api(prompt)
    print(f"✅ Generated Hypothesis: {hypothesis}")
    return {"hypothesis": hypothesis}