# FILE: graph.py

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# Import all node functions
from nodes.retriever import retriever_node
from nodes.knowledge_graph_updater import knowledge_graph_updater_node
from nodes.hypothesis_generator import hypothesis_generator_node
from nodes.experiment_designer import experiment_designer_node
from nodes.code_synthesizer import code_synthesizer_node
from nodes.sandbox_runner import sandbox_runner_node
from nodes.analyzer import analyzer_node
from nodes.reviewer import reviewer_node
from nodes.paper_writer import paper_writer_node

MAX_LOOPS = 3

class GraphState(TypedDict):
    topic: str
    documents: List[str]
    hypothesis: str
    experiment_plan: Dict[str, Any]
    code: str
    dockerfile: str
    results: Dict[str, Any]
    analysis: str
    decision: str
    paper: str
    loop_count: int

def should_continue(state: GraphState) -> str:
    """Conditional edge to decide whether to proceed or redesign."""
    if state["decision"] == "proceed":
        return "paper_writer"
    
    if state["loop_count"] >= MAX_LOOPS:
        print("---MAX LOOPS REACHED---")
        return END

    return "experiment_designer"

def increment_loop_count(state: GraphState) -> Dict[str, Any]:
    """Increments the loop counter."""
    count = state.get("loop_count", 0) + 1
    return {"loop_count": count}

# Define the workflow
workflow = StateGraph(GraphState)

workflow.add_node("retriever", retriever_node)
workflow.add_node("knowledge_graph_updater", knowledge_graph_updater_node)
workflow.add_node("hypothesis_generator", hypothesis_generator_node)
workflow.add_node("experiment_designer", experiment_designer_node)
workflow.add_node("code_synthesizer", code_synthesizer_node)
workflow.add_node("sandbox_runner", sandbox_runner_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("paper_writer", paper_writer_node)
workflow.add_node("increment_loop_count", increment_loop_count)

# Define the edges
workflow.set_entry_point("retriever")
workflow.add_edge("retriever", "knowledge_graph_updater")
workflow.add_edge("knowledge_graph_updater", "hypothesis_generator")
workflow.add_edge("hypothesis_generator", "experiment_designer")
workflow.add_edge("experiment_designer", "code_synthesizer")
workflow.add_edge("code_synthesizer", "sandbox_runner")
workflow.add_edge("sandbox_runner", "analyzer")
workflow.add_edge("analyzer", "reviewer")
workflow.add_conditional_edges("reviewer", should_continue, {
    "paper_writer": "paper_writer",
    "experiment_designer": "increment_loop_count",
})
workflow.add_edge("increment_loop_count", "experiment_designer")
workflow.add_edge("paper_writer", END)

# Compile the graph
app = workflow.compile()