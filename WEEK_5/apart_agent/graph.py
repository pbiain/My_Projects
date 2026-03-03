from langgraph.graph import StateGraph, END
from apart_agent.state import AgentState
from apart_agent.nodes.retrieve_context import retrieve_context
from apart_agent.nodes.react_agent import react_agent
from apart_agent.nodes.classify_lead import classify_lead
from apart_agent.nodes.assemble_output import assemble_output


def route_by_score(state):
    return state["lead_score"]


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("react_agent",      react_agent)
    graph.add_node("classify_lead",    classify_lead)
    graph.add_node("assemble_output",  assemble_output)

    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "react_agent")
    graph.add_edge("react_agent",      "classify_lead")
    graph.add_conditional_edges(
        "classify_lead",
        route_by_score,
        {
            "HOT":  "assemble_output",
            "WARM": "assemble_output",
            "COLD": "assemble_output",
        }
    )
    graph.add_edge("assemble_output", END)

    return graph.compile()