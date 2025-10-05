# FILE: nodes/experiment_designer.py

import json
from typing import Dict, Any
import pprint
from utils.llm_api import query_huggingface_api
import re

# CORRECTED FUNCTION SIGNATURE
def experiment_designer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: EXPERIMENT DESIGNER---")
    hypothesis = state.get("hypothesis", "")
    
    prompt = f"""
    You are a meticulous lab director. Design a detailed experiment to test the hypothesis: "{hypothesis}"
    
    **CRITICAL INSTRUCTIONS:**
    1.  Provide the plan in a single, syntactically correct JSON object.
    2.  The JSON object must have keys: "datasets", "methodology", and "metrics".
    3.  All objects and sub-objects within the JSON MUST be composed of key-value pairs (e.g., "key": "value"). Do not use lists of strings where an object is expected.
    4.  The response should contain ONLY the JSON object, with no explanatory text before or after it.

    Wrap the final JSON object in a single markdown code block.
    ```json
    {{
      "datasets": [...],
      "methodology": {{...}},
      "metrics": [...]
    }}
    ```
    """

    print("📝 Designing experiment plan...")
    response_text = query_huggingface_api(prompt)
    
    match = re.search(r"```json\n({.*?})\n```", response_text, re.DOTALL)
    
    try:
        if match:
            json_str = match.group(1)
        else:
            json_str = response_text[response_text.find('{'):response_text.rfind('}')+1]

        experiment_plan = json.loads(json_str)
        print("✅ Experiment Plan Generated:")
        pprint.pprint(experiment_plan)
        return {"experiment_plan": experiment_plan}
    except (json.JSONDecodeError, IndexError) as e:
        print(f"❗️ Error: Failed to parse JSON from LLM response. Error: {e}")
        print(f"Raw response was: {response_text}")
        raise ValueError("Could not generate a valid JSON experiment plan.")