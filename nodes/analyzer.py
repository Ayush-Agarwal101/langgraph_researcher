# FILE: nodes/analyzer.py

from typing import Dict, Any
from utils.llm_api import query_huggingface_api
import json

def analyzer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: ANALYZER---")
    results = state.get("results", {})
    if "error" in results:
        return {"analysis": "The experiment failed to run. Cannot analyze results."}

    results_str = json.dumps(results, indent=2)
    prompt = f"""
    You are a data analyst. Analyze the following experiment results and provide a brief, one-paragraph summary of their implications.

    **Experiment Results:**
    {results_str}

    **Analysis Summary:**
    """
    print("📈 Analyzing results...")
    analysis = query_huggingface_api(prompt)
    print(f"✅ Analysis complete: {analysis}")
    return {"analysis": analysis}