# FILE: nodes/experiment_designer.py

import json
from typing import Dict, Any
import pprint
from utils.llm_api import query_huggingface_api

def experiment_designer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: EXPERIMENT DESIGNER---")
    hypothesis = state.get("hypothesis", "")
    
    prompt = f"""
    You are a meticulous lab director. Design a detailed experiment to test the hypothesis: "{hypothesis}"
    Provide the plan in a valid JSON format with keys: "datasets", "methodology", "metrics".
    - "datasets": List of public dataset names.
    - "methodology": Step-by-step experimental procedure.
    - "metrics": List of specific, measurable metrics for evaluation.

    JSON Output:
    """

    print("📝 Designing experiment plan...")
    plan_str = query_huggingface_api(prompt)
    
    try:
        cleaned_plan_str = plan_str[plan_str.find('{'):plan_str.rfind('}')+1]
        experiment_plan = json.loads(cleaned_plan_str)
        print("✅ Experiment Plan Generated:")
        pprint.pprint(experiment_plan)
        return {"experiment_plan": experiment_plan}
    except json.JSONDecodeError:
        print(f"❗️ Error: Failed to parse JSON from LLM response: {plan_str}")
        raise ValueError("Could not generate a valid JSON experiment plan.")