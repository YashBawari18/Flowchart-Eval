
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

        # 2. Add edges - Spatial Heuristic (Top-to-Bottom Flow)
        # Since arrow detection is unreliable in the prototype, we assume imperfect flow.
        # We connect each node to the nearest node *strictly below* it to form a flow.
        
        nodes = list(self.graph.nodes(data=True))
        
        for i, source in nodes:
            bs = source['bbox']
            source_center = (bs[0] + bs[2]/2, bs[1] + bs[3]/2)
            source_bottom = bs[1] + bs[3]
            
            best_target = None
            min_dist = float('inf')
            
            for j, target in nodes:
                if i == j: continue
                
                bt = target['bbox']
                target_center = (bt[0] + bt[2]/2, bt[1] + bt[3]/2)
                target_top = bt[1]
                
                # Check 1: Target must be below source
                if target_top > source_bottom - 10: # Allow small overlap
                    # Check 2: Lateral distance shouldn't be too huge (relative to width)
                    # This prevents connecting left-column to right-column widely
                    dx = abs(source_center[0] - target_center[0])
                    dy = target_top - source_bottom
                    
                    # Distance metric favoring vertical proximity
                    dist = math.sqrt(dx**2 + dy**2)
                    
                    if dist < min_dist:
                        min_dist = dist
                        best_target = j
            
            # Add edge if a valid downstream neighbor is found
            # Threshold: Don't connect if it's too far away
            if best_target is not None and min_dist < max(self.image_height, self.image_width) * 0.5:
                 self.graph.add_edge(i, best_target)

        return self.graph

    def set_image_dimensions(self, width, height):
        self.image_width = width
        self.image_height = height

    def is_connected(self, bbox1, bbox2, arrows):
        # Deprecated in favor of spatial heuristic for this phase
        return False

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
