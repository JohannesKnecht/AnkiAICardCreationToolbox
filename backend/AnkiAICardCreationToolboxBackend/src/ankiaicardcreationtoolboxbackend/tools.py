import json


def best_practices_of_formulating_knowledge(city: str) -> str:
    """Get best practices of formulating knowledge"""
    # load json knowledge_base.json
    return json.load("knowledge_base.json")