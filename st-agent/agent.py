
import datetime
import string
import re

# -----------------------------
# Tool 1: get_time(location)
# -----------------------------
def get_time(location):
    times = {
        "london": "2025-12-25 12:22:34",
        "new york": "2025-12-25 08:22:34",
        "cape town": "2025-12-25 14:22:34"
    }
    loc = location.lower()
    if loc in times:
        return {"location": location, "time": times[loc]}
    return {"error": f"Unsupported location: {location}"}

# -----------------------------
# Tool 2: calc(expression)
# -----------------------------
def calc(expression):
    try:
        result = eval(expression, {"__builtins__": {}})
        return {"result": result}
    except Exception:
        return {"error": "Invalid mathematical expression"}

# -----------------------------
# Tool 3: lookup_faq(query)
# -----------------------------
def lookup_faq(query):
    kb = {
        "forgot password": {"answer": "Click 'Forgot Password'.", "source_title": "Account Help"},
        "support email": {"answer": "Email support@example.com.", "source_title": "Support Guide"}
    }
    query_lower = query.lower()
    for k in kb:
        if k in query_lower:
            return kb[k]
    return {"answer": "Sorry, no matching FAQ was found.", "source_title": "N/A"}


# -----------------------------
# Agent class
# -----------------------------
class Agent:
    def __init__(self):
        self.memory = {
            "last_goals": [],
            "last_tool_result": None,
            "last_location": None
        }
        self.timezones = {"london": 0, "new york": -4, "cape town": 2}

    # -----------------------------
    # Decide which tool(s) to call
    # -----------------------------
    def mock_model(self, user_input):
        user_input_lower = user_input.lower()

        # Task 1: Time + UTC
        if "time" in user_input_lower and "utc" in user_input_lower:
            match = re.search(r"in\s+([a-zA-Z\s]+?)(?:\s+and|$)", user_input_lower)
            loc_clean = match.group(1).strip().lower() if match else ""
            return [
                {"tool": "get_time", "args": {"location": loc_clean}},
                {"tool": "convert_utc", "args": {}}
            ]

        # Task 2: Percentage calculation
        perc_match = re.search(r'(\d+)%\s+of\s+([\d,]+)', user_input_lower)
        if perc_match:
            percent = int(perc_match.group(1)) / 100
            number = float(perc_match.group(2).replace(",", ""))
            expr = f"{number}*{percent}"
            return [{"tool": "calc", "args": {"expression": expr}}]

        # Single-step tools
        if "convert that to utc" in user_input_lower:
            return [{"tool": "convert_utc", "args": {}}]

        if "time" in user_input_lower:
            match = re.search(r"in\s+([a-zA-Z\s]+)", user_input_lower)
            loc_clean = match.group(1).strip().lower() if match else ""
            return [{"tool": "get_time", "args": {"location": loc_clean}}]

        if "calculate" in user_input_lower:
            expr = user_input_lower.replace("calculate", "").strip()
            return [{"tool": "calc", "args": {"expression": expr}}]

        if "how" in user_input_lower or "help" in user_input_lower:
            return [{"tool": "lookup_faq", "args": {"query": user_input}}]

        return [{"tool": None, "args": {}}]

    # -----------------------------
    # Convert last tool result to UTC
    # -----------------------------
    def convert_to_utc(self):
        last = self.memory.get("last_tool_result")
        location = self.memory.get("last_location", "").lower()

        if not last or "time" not in last:
            return {"error": "No previous time to convert"}

        offset = self.timezones.get(location)
        if offset is None:
            return {"error": f"Cannot convert UTC: unknown location '{location}'"}

        local_time = datetime.datetime.strptime(last["time"], "%Y-%m-%d %H:%M:%S")
        utc_time = local_time - datetime.timedelta(hours=offset)
        return {"utc_time": utc_time.strftime("%Y-%m-%d %H:%M:%S")}

    # -----------------------------
    # Run a single tool
    # -----------------------------
    def run_tool(self, tool_call):
        tool = tool_call.get("tool")
        args = tool_call.get("args", {})

        try:
            if tool == "get_time":
                result = get_time(**args)
                if "location" in args:
                    self.memory["last_location"] = args["location"].lower()
            elif tool == "calc":
                result = calc(**args)
            elif tool == "lookup_faq":
                result = lookup_faq(**args)
            elif tool == "convert_utc":
                result = self.convert_to_utc()
            else:
                result = {"error": "Unknown tool"}
        except Exception as e:
            result = {"error": f"Tool failed: {str(e)}"}

        self.memory["last_tool_result"] = result
        return result

    def run_tool_sequence(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            result = self.run_tool(tool_call)
            results.append(result)
        return results
