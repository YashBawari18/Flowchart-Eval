
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

class Evaluator:
    """
    Traverses the graph to generate algorithm and compares it with model.
    """
    def __init__(self, student_graph, model_algorithm):
        self.student_graph = student_graph
        self.model_algorithm = model_algorithm # List of strings/steps

    def generate_pseudo_code(self):
        """
        Traverses the graph from 'Start' to 'End' to produce a step-by-step algorithm.
        """
        try:
            # Find start node
            start_node = [n for n, d in self.student_graph.nodes(data=True) 
                          if 'start' in d.get('text', '').lower()][0]
        except IndexError:
            return ["Error: No Start node found."]

        # Simple topological or DFS traversal for linear/branching logic
        steps = []
        visited = set()
        
        def traverse(u):
            if u in visited: return
            visited.add(u)
            data = self.student_graph.nodes[u]
            steps.append(f"{data.get('type')}: {data.get('text')}")
            
            # DFS-like traversal
            for v in self.student_graph.neighbors(u):
                traverse(v)
        
        traverse(start_node)
        return steps

    def evaluate(self, student_steps):
        """
        Compares student steps with model algorithm using semantic similarity.
        Awards partial marks and provides feedback.
        """
        marks = 0
        feedback = []
        
        # 1. Structural similarity (length comparison)
        len_orig = len(self.model_algorithm)
        len_stud = len(student_steps)
        marks += max(0, 10 - abs(len_orig - len_stud)) # Rough penalty
        
        # 2. Semantic Step Matching (using TF-IDF + Cosine Similarity)
        if not student_steps or not self.model_algorithm:
            return 0, ["Empty algorithm provided."]

        vectorizer = TfidfVectorizer()
        
        for i, m_step in enumerate(self.model_algorithm):
            best_sim = 0
            for s_step in student_steps:
                # Calculate similarity between current model step and all student steps
                try:
                    tfidf = vectorizer.fit_transform([m_step, s_step])
                    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
                    best_sim = max(best_sim, sim)
                except:
                    continue
            
            if best_sim > 0.7:
                marks += 10
                feedback.append(f"Step {i+1} Correct: '{m_step}' found.")
            elif best_sim > 0.4:
                marks += 5
                feedback.append(f"Step {i+1} Partial: '{m_step}' partially addressed.")
            else:
                feedback.append(f"Step {i+1} Missing: '{m_step}' not found.")

        # Total score calculation (normalized to 100)
        total_possible = (len_orig * 10) + 10
        final_score = (marks / total_possible) * 100
        
        return round(final_score, 2), feedback

if __name__ == "__main__":
    print("Evaluator module loaded.")
