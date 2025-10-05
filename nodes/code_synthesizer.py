# FILE: nodes/code_synthesizer.py

from typing import Dict, Any
from utils.llm_api import query_huggingface_api
import pprint

def code_synthesizer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: CODE SYNTHESIZER---")
    plan = state.get("experiment_plan")
    plan_str = pprint.pformat(plan)

    prompt = f"""
    You are an expert Python programmer. Based on the following experiment plan, write a single, complete Python script to execute the experiment.

    **Experiment Plan:**
    {plan_str}

    **Instructions for the Python Script:**
    1. The script must be self-contained and import necessary libraries (e.g., pandas, scikit-learn, numpy).
    2. Implement the methodology. Use mock data if no public dataset is easily available.
    3. Calculate all metrics listed in the plan.
    4. Save all results into a dictionary, then save this dictionary to a JSON file named exactly 'results.json'.
    Example JSON output: {{"accuracy": 0.95, "precision": 0.92}}

    **Python Script:**
    """

    print("🤖 Generating experiment code...")
    code = query_huggingface_api(prompt)
    cleaned_code = code.replace("```python", "").replace("```", "").strip()
    
    print("✅ Generated Code:")
    print(cleaned_code)

    dockerfile = f"""
FROM python:3.9-slim
WORKDIR /app
RUN pip install pandas scikit-learn numpy
COPY experiment.py .
CMD ["python", "experiment.py"]
"""
    print("\n✅ Generated Dockerfile.")
    return {"code": cleaned_code, "dockerfile": dockerfile}