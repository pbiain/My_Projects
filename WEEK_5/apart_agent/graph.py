from langgraph.graph import StateGraph, END
from apart_agent.state import AgentState
from apart_agent.nodes.retrieve_context import retrieve_context
from apart_agent.nodes.react_agent import react_agent
from apart_agent.nodes.assemble_output import assemble_output


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("react_agent",      react_agent)
    graph.add_node("assemble_output",  assemble_output)

    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "react_agent")
    graph.add_edge("react_agent",      "assemble_output")
    graph.add_edge("assemble_output",  END)

    return graph.compile()