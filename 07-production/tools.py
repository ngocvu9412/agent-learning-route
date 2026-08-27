"""StudyTracker tools — TWO simple tools + schemas.

Data lives in study_log.json — plain file I/O, exactly your exercise-6 skills.
No classes, no binding magic: module-level functions + the same dispatch
dict you built in exercises 2 and 3.
"""
import json
from datetime import date, timedelta
from pathlib import Path

LOG_FILE = Path(__file__).parent / "study_log.json"


def _load():
    """TODO: return the log dict; {"sessions": []} if file doesn't exist yet."""
    # Hint: if LOG_FILE.exists(): json.loads(LOG_FILE.read_text(encoding="utf-8"))
    if LOG_FILE.exists(): 
        return json.loads(LOG_FILE.read_text(encoding = "utf-8"))
    else: return {"sessions": []}


def _save(data):
    # Hint: LOG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    LOG_FILE.write_text(json.dumps(data, indent = 2), encoding = "utf-8")


def log_session(topic: str, minutes: int):
    """TODO: append {"topic": topic, "minutes": minutes, "date": str(date.today())}
    to the log and save. Return a confirmation string."""
    # Hint: data = _load(); data["sessions"].append({...}); _save(data)
    #       return f"Logged {minutes} minutes of {topic}."
    data = _load()
    data["sessions"].append({"topic": topic, "minutes": minutes, "date": str(date.today())})
    _save(data)
    return f"Logged {minutes} minutes of {topic}."


def weekly_report():
    """TODO: sum minutes per topic for the last 7 days, return a string like
    'langgraph: 90min, rag: 45min'."""
    # Hint: cutoff = date.today() - timedelta(days=7)
    #       plain Python loop over _load()["sessions"] — no SQL, nothing fancy
    cutoff = date.today() - timedelta(days = 7)
    results = {}
    sessions = _load()["sessions"]
    for session in sessions:
        if date.fromisoformat(session["date"]) >= cutoff:
            if session["topic"] not in results:
                results[session["topic"]] = session["minutes"]
            else: results[session["topic"]] += session["minutes"]

    return json.dumps(results)


# The dispatch dict — same shape as exercise 2/3's func = {"get_time": get_time}
TOOL_FUNCTIONS = {
    "log_session": log_session,
    "weekly_report": weekly_report,
}


def get_tool_schemas():
    """TODO: return TWO schema dicts in the ex-2 shape.

    Hint — one per tool:
        {"type": "function",
         "function": {"name": "log_session",
                      "description": "Log a study session for a topic.",
                      "parameters": {"type": "object",
                                     "properties": {
                                         "topic": {"type": "string", "description": "..."},
                                         "minutes": {"type": "integer", "description": "..."}},
                                     "required": ["topic", "minutes"]}}}
    weekly_report takes NO parameters: properties {}, required [].
    Good descriptions = the model picks the right tool. Write them carefully.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "log_session",
                "description": "Log a study session for a topic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "Learning Topic"},
                        "minutes": {"type": "integer", "description": "Learning time for topic."}
                    },
                    "required": ["topic", "minutes"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "weekly_report",
                "description": "Return a string like 'langgraph: 90min, rag: 45min'.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    ]