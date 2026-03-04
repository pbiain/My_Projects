from typing import TypedDict, List


class AgentState(TypedDict):
    user_message:      str
    retrieved_context: str
    agent_response:    str
    lead_score:        str
    score_reason:      str
    actions_taken:     List[str]
    chat_history:      List[dict]   # [{"user": "...", "assistant": "..."}, ...]
    final_output:      dict
    language:          str          # "es" or "en", set by frontend flag