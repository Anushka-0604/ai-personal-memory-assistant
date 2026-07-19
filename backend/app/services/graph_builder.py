from app.schemas.extraction import MemoryExtraction
from app.schemas.graph import GraphEdge, GraphNode, MemoryGraph


class GraphBuilder:
    """Builds a knowledge graph from extracted memory data."""

    def build(self, extraction: MemoryExtraction) -> MemoryGraph:
        graph = MemoryGraph()

        # ----------------------------
        # People
        # ----------------------------
        for person in extraction.people:
            graph.nodes.append(
                GraphNode(
                    id=f"person:{person}",
                    label=person,
                    type="person",
                )
            )

            graph.edges.append(
                GraphEdge(
                    source="user",
                    target=f"person:{person}",
                    relationship="MET",
                )
            )

        # ----------------------------
        # Organizations
        # ----------------------------
        for organization in extraction.organizations:
            graph.nodes.append(
                GraphNode(
                    id=f"organization:{organization}",
                    label=organization,
                    type="organization",
                )
            )

        # ----------------------------
        # Locations
        # ----------------------------
        for location in extraction.locations:
            graph.nodes.append(
                GraphNode(
                    id=f"location:{location}",
                    label=location,
                    type="location",
                )
            )

        # ----------------------------
        # Person -> Organization
        # ----------------------------
        if extraction.people and extraction.organizations:
            for person in extraction.people:
                for organization in extraction.organizations:
                    graph.edges.append(
                        GraphEdge(
                            source=f"person:{person}",
                            target=f"organization:{organization}",
                            relationship="ASSOCIATED_WITH",
                        )
                    )

        # ----------------------------
        # Person -> Location
        # ----------------------------
        if extraction.people and extraction.locations:
            for person in extraction.people:
                for location in extraction.locations:
                    graph.edges.append(
                        GraphEdge(
                            source=f"person:{person}",
                            target=f"location:{location}",
                            relationship="LOCATED_IN",
                        )
                    )

        return graph