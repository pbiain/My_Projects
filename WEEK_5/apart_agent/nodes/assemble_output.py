def assemble_output(state):
    score = state["lead_score"]
    state["final_output"] = {
        "answer":           state["agent_response"],
        "score":            score,
        "score_reason":     state["score_reason"],
        "original_message": state["user_message"],
        "actions_taken":    state["actions_taken"],
        "send_telegram":    score == "HOT",
        "send_email":       score == "WARM",
        "log_to_sheets":    True,
    }
    return state