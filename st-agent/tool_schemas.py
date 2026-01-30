def define_tool_schemas():
    TOOLS = [
        {
            "name": "get_time",
            "description": "Get the current time for a given location",
            "parameters": {"location": "string"},
            "required": ["location"]
        },
        {
            "name": "calc",
            "description": "Evaluate a mathematical expression",
            "parameters": {"expression": "string"},
            "required": ["expression"]
        },
        {
            "name": "lookup_faq",
            "description": "Search a FAQ knowledge base",
            "parameters": {"query": "string"},
            "required": ["query"]
        }
    ]
    for t in TOOLS:
        print(t)
    return TOOLS

#    print("=== Tool Schemas Defined ===\n")
#     print(json.dumps(TOOLS, indent=4))    

# if __name__ == "__main__":
#     define_tool_schemas()