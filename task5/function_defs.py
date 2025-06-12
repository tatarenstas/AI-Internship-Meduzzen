FUNCTION_DEFINITIONS = [
    {
        "name": "semantic_search",
        "description": "Search knowledge base for relevant information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "User question or search request"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "summarize_session",
        "description": "Generate a natural language summary of the session so far",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]