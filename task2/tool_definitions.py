FUNCTION_DEFINITIONS = [
    {
        "name": "get_weather",
        "description": "Get fake weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "calculate_area",
        "description": "Calculate area of a circle by radius",
        "parameters": {
            "type": "object",
            "properties": {
                "radius": {"type": "number", "description": "Radius of the circle"}
            },
            "required": ["radius"]
        }
    },
    {
        "name": "search_wikipedia",
        "description": "Search Wikipedia for a summary of a query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
]
