"""StudyTracker entry point — REPL + demo.

Phase 0 acceptance: this file runs and exits cleanly with empty stubs.
"""
from agent import StudyTrackerAgent
from memory import MS

def choose_session(session_list):
    if session_list == []:
        return input("New session name: ")

    print("Session Choosing \n")

    sessions = {}
    for i in range(len(session_list)):
        sessions[i] = session_list[i]
        print(f"{i}: {session_list[i]}")

    print("\nType session number (e.g: 1) to access session")
    print("Type 'new' for new session")

    user_input = (input("Choose: "))
    if user_input == "new":
        return input("New session name: ")
    
    return sessions[int(user_input)]

def repl(agent):
    """TODO: while True: user_input = input("You: ")
    quit/exit breaks; else print("Agent:", agent.chat(user_input))."""
    print("StudyTracker — type 'quit' to exit")
    while True:
        user_input = input("You: ")

        if user_input == "quit":
            break

        print(f"Agent: ", agent.chat(user_input))


def demo(agent):
    """TODO: the acceptance flow:
    1. agent.chat("Log 45 minutes of langgraph")      -> tool fires, JSON grows
    2. agent.chat("What did I study most recently?")  -> answered via weekly_report
    """
    ...
    agent.chat("Log 45 minutes of langgraph") 
    agent.chat("What did I study most recently?")

if __name__ == "__main__":
    session_id = choose_session(MS.get_conversation_all_session_id())
    agent = StudyTrackerAgent(session_id)
    # demo(agent)
    repl(agent)
