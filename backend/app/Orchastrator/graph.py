from langgraph.graph import StateGraph

from app.Orchastrator.state import ReviewState

from app.Orchastrator.node import *

builder = StateGraph(
    ReviewState
)

builder.add_node(
    "validate",
    validate_input
)

builder.add_node(
    "context",
    build_context
)

builder.add_node(
    "finish",
    finish
)

builder.set_entry_point(
    "validate"
)

builder.add_edge(
    "validate",
    "context"
)

builder.add_edge(
    "context",
    "finish"
)

builder.set_finish_point(
    "finish"
)

graph = builder.compile()