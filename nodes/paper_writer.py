# FILE: nodes/paper_writer.py

import os
from typing import Dict, Any
from utils.llm_api import query_huggingface_api

def paper_writer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: PAPER WRITER---")
    
    # Gather all content from the state
    topic = state.get("topic")
    hypothesis = state.get("hypothesis")
    plan = state.get("experiment_plan")
    results = state.get("results")
    analysis = state.get("analysis")

    prompt = f"""
    You are a research assistant. Synthesize the following information into a well-structured research paper in Markdown format.

    **Topic:** {topic}
    **Hypothesis:** {hypothesis}
    **Methodology:** {plan.get('methodology', 'N/A')}
    **Results:** {results}
    **Analysis/Discussion:** {analysis}

    **Instructions:**
    Write a complete paper with the following sections:
    1.  **Abstract:** A brief summary of the work.
    2.  **Introduction:** Background on the topic and statement of the hypothesis.
    3.  **Methodology:** Describe the experiment based on the plan.
    4.  **Results:** Present the results.
    5.  **Discussion:** Interpret the results based on the analysis.
    6.  **Conclusion:** Summarize the findings and future work.
    
    The paper should be comprehensive and well-written.
    """
    print("✍️ Writing final paper...")
    paper = query_huggingface_api(prompt)
    
    os.makedirs("outputs", exist_ok=True)
    filename = "outputs/research_paper.md"
    with open(filename, "w") as f:
        f.write(paper)
    
    print(f"✅ Final paper saved to '{filename}'")
    return {"paper": paper}