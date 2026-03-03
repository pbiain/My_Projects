from typing import TypedDict, List


class AgentState(TypedDict):
    user_message:      str
    retrieved_context: str
    agent_response:    str
    lead_score:        str
    score_reason:      str
    actions_taken:     List[str]
    final_output:      dict