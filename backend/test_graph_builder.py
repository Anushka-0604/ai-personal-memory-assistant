from app.schemas.extraction import MemoryExtraction
from app.services.graph_builder import GraphBuilder

builder = GraphBuilder()

extraction = MemoryExtraction(
    people=["Alice"],
    organizations=["Microsoft"],
    locations=["Bangalore"],
)

graph = builder.build(extraction)

print("\nNodes:")
for node in graph.nodes:
    print(node)

print("\nEdges:")
for edge in graph.edges:
    print(edge)