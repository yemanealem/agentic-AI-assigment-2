def get_time(location):
    times = {
        "london": "2025-12-25 12:22:34",
        "new york": "2025-12-25 08:22:34",
        "cape town": "2025-12-25 14:22:34"
    }
    loc = location.lower()
    if loc in times:
        return {"location": location, "time": times[loc]}
    print(location)
    return {"error": f"Unsupported location: {location}"}

def calc(expression):
    try:
        result = eval(expression, {"__builtins__": {}})
        return {"result": result}
    except Exception:
        return {"error": "Invalid mathematical expression"}

def lookup_faq(query):
    kb = {
        "forgot password": {"answer": "Click 'Forgot Password'.", "source_title": "Account Help"},
        "support email": {"answer": "Email support@example.com.", "source_title": "Support Guide"}
    }
    query_lower = query.lower()
    for k, v in kb.items():
        if k in query_lower:
            return v
    return {"answer": "Sorry, no matching FAQ was found.", "source_title": "N/A"}
