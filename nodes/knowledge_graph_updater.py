# FILE: nodes/knowledge_graph_updater.py

import json
from typing import Dict, Any
from utils.database import knowledge_graph_collection
from utils.llm_api import query_huggingface_api

def knowledge_graph_updater_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: KNOWLEDGE GRAPH UPDATER---")
    documents = state.get("documents", [])
    if not documents: return {}
    if knowledge_graph_collection is None:
        print("❌ MongoDB connection not available. Skipping.")
        return {}
        
    prompt_template = """
    From the research document text below, extract key entities and their relationships.
    Extract entity types: 'concept', 'method', 'metric'.
    Format the output as a valid JSON list of objects. Each object must have 'source_entity', 'relation', and 'target_entity' keys.
    Example: [{"source_entity": "BERT", "relation": "uses", "target_entity": "attention mechanism"}]

    Document text:
    ---
    {document_text}
    ---
    JSON Output:
    """

    all_relations = []
    for doc in documents:
        prompt = prompt_template.format(document_text=doc)
        try:
            response_text = query_huggingface_api(prompt)
            cleaned_response = response_text[response_text.find('['):response_text.rfind(']')+1]
            extracted_relations = json.loads(cleaned_response)
            all_relations.extend(extracted_relations)
        except Exception as e:
            print(f"❗️ Failed to extract relations from a document: {e}")

    if all_relations:
        print(f"📝 Inserting {len(all_relations)} new relations into the knowledge graph...")
        knowledge_graph_collection.insert_many(all_relations)
        print("✅ Knowledge graph updated.")
    else:
        print("🤷 No new relations were extracted.")
    return {}