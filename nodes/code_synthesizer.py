# FILE: nodes/code_synthesizer.py

from typing import Dict, Any
from utils.llm_api import query_huggingface_api
import pprint
import re

# CORRECTED FUNCTION SIGNATURE
def code_synthesizer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: CODE SYNTHESIZER---")
    plan = state.get("experiment_plan")
    plan_str = pprint.pformat(plan)

    prompt = f"""
    You are an expert Python programmer writing clean, bug-free code. Based on the following experiment plan, write a single, complete Python script.

    **Experiment Plan:**
    {plan_str}

    **CRITICAL INSTRUCTIONS for the Python Script:**
    1.  The script MUST be self-contained and import all necessary libraries.
    2.  All variable names, especially dictionary keys and DataFrame columns, MUST be valid Python identifiers (e.g., use 'app_usage' instead of 'app usage'). **This is a strict requirement.**
    3.  Implement the methodology using mock data. The code must be runnable and free of syntax or runtime errors.
    4.  The script MUST save all results into a dictionary, then save this dictionary to a JSON file named exactly 'results.json'.
    5.  The script should contain ONLY Python code. Do not add any explanatory text after the code block.

    Wrap the final Python code in a single markdown code block.
    ```python
    # Your Python code here
    ```
    """

    print("🤖 Generating experiment code...")
    response = query_huggingface_api(prompt)
    
    match = re.search(r"```python\n(.*)```", response, re.DOTALL)
    if match:
        cleaned_code = match.group(1).strip()
    else:
        cleaned_code = response.strip()

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