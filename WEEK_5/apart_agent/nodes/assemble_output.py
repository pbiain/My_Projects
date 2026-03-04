def assemble_output(state):
    score = state["lead_score"]
    updated_history = state.get("chat_history", []) + [{
        "user":      state["user_message"],
        "assistant": state["agent_response"],
    }]
    state["chat_history"] = updated_history

    state["final_output"] = {
        "type":             "inbound",
        "answer":           state["agent_response"],
        "score":            score,
        "score_reason":     state["score_reason"],
        "original_message": state["user_message"],
        "actions_taken":    state["actions_taken"],
        "chat_history":     updated_history,
        "send_telegram":    score == "HOT",
        "send_email":       score == "WARM",
        "log_to_sheets":    True,
    }
    return state