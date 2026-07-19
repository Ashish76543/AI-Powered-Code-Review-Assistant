from langgraph.graph import StateGraph

from app.Orchastrator.state import ReviewState
from app.Orchastrator.node import *

builder = StateGraph(ReviewState)

builder.add_node("validate", validate_input)
builder.add_node("context", build_context)

builder.add_node("code", code_review_agent)
builder.add_node("security", security_review_agent)
builder.add_node("performance", performance_review_agent)

builder.add_node("aggregate", aggregate_reviews)
builder.add_node("finish", finish)

builder.set_entry_point("validate")

builder.add_edge("validate", "context")

builder.add_edge("context", "code")
builder.add_edge("context", "security")
builder.add_edge("context", "performance")

builder.add_edge(
    ["code", "security", "performance"],
    "aggregate"
)

builder.add_edge("aggregate", "finish")

builder.set_finish_point("finish")

graph = builder.compile()