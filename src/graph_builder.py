
import networkx as nx
import math

class GraphBuilder:
    """
    Converts detected shapes and connection evidence into a Directed Graph.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, shapes, arrows):
        """
        shapes: List of dictionaries with 'type', 'bbox', 'text'
        arrows: Evidence of flow between shapes
        """
        # 1. Add nodes
        for i, shape in enumerate(shapes):
            self.graph.add_node(i, **shape)

        # 2. Add edges based on arrow proximity or centroid distance
        # In this prototype, we use a simple distance heuristic if arrows are messy
        for i, source in self.graph.nodes(data=True):
            for j, target in self.graph.nodes(data=True):
                if i == j: continue
                
                # Heuristic: If arrow endpoints are near source/target bounding boxes
                # For this prototype, we simulate connection logic
                if self.is_connected(source['bbox'], target['bbox'], arrows):
                    self.graph.add_edge(i, j)

        return self.graph

    def is_connected(self, bbox1, bbox2, arrows):
        """
        Check if an arrow connects two bounding boxes.
        Simple heuristic: Does the arrow start near bbox1 and end near bbox2?
        """
        # Logic for research feasibility: 
        # Check coordinates of arrows against bbox centers
        # Mocking implementation for the prototype structure
        return False # Placeholder - replaced by real logic in integration

    def validate_flow(self):
        """Validates basic flowchart properties."""
        has_start = any(d.get('type') == 'Start/End' and 'start' in d.get('text', '').lower() 
                        for n, d in self.graph.nodes(data=True))
        has_end = any(d.get('type') == 'Start/End' and 'stop' in d.get('text', '').lower() 
                      for n, d in self.graph.nodes(data=True))
        
        is_dag = nx.is_directed_acyclic_graph(self.graph)
        return has_start and has_end and is_dag

if __name__ == "__main__":
    print("GraphBuilder module loaded.")
