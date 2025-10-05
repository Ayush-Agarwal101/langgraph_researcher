# FILE: nodes/reviewer.py

from typing import Dict, Any
from utils.llm_api import query_huggingface_api

def reviewer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: REVIEWER---")
    hypothesis = state.get("hypothesis")
    analysis = state.get("analysis")

    prompt = f"""
    You are a senior scientist reviewing a research experiment.
    **Hypothesis:** {hypothesis}
    **Analysis of Results:** {analysis}

    **Your Task:**
    Based on the analysis, are the results sufficient and clear enough to support or refute the hypothesis?
    Respond with only ONE of the following words: 'proceed' or 'redesign'.
    """
    print("🧐 Reviewing analysis...")
    decision = query_huggingface_api(prompt).strip().lower()
    
    # Clean up decision string
    if "proceed" in decision:
        final_decision = "proceed"
    elif "redesign" in decision:
        final_decision = "redesign"
    else:
        final_decision = "redesign" # Default to redesign if unclear
        
    print(f"✅ Reviewer decision: {final_decision}")
    return {"decision": final_decision}