from manim import *

class Prims(Scene):
    def construct(self):
        # Define graph vertices and positions
        vertices = ["A", "B", "C", "D", "E", "F", "G"]
        positions = {
            "A": LEFT + UP,
            "B": LEFT*1.75 + DOWN,
            "C": RIGHT*2 + UP*2,
            "D": RIGHT*1.75 + DOWN*1.75,
            "E": 2.5 * RIGHT + UP,
            "F": 2 * DOWN,
            "G": 2 * LEFT
        }

        # Define edges and weights
        edges = [
            ("A", "B", 2), ("A", "C", 3), ("A", "D", 3),
            ("B", "D", 4), ("B", "E", 3),
            ("C", "D", 5), ("C", "F", 1),
            ("D", "E", 2), ("D", "F", 6),
            ("E", "F", 7), ("E", "G", 5),
            ("F", "G", 8)
        ]

        # Create graph object
        graph = Graph(
            vertices,
            [(u, v) for u, v, _ in edges],
            layout=positions,
            vertex_config={"fill_color": BLUE, "radius": 0.3},  
            edge_config={"stroke_width": 1, "stroke_opacity": 0.3}
        )

        # Enlarge and center the labels manually
        self.add(graph)
        

        # Manually add vertex labels
        for v in vertices:
            label = Text(v, color=WHITE).scale(0.5)
            label.move_to(graph[v])
            self.add(label)

        # Add edge weights
        weights = {}
        for u, v, w in edges:
            edge = graph.edges.get((u, v)) or graph.edges.get((v, u))
            dot = Dot(color=BLACK).move_to(edge.get_center()).scale(2)
            label = MathTex(str(w)).scale(0.4)
            label.move_to(dot.get_center())
            self.add(dot, label)
            weights[frozenset((u, v))] = label  # store weight label by edge set

        # Prim's algorithm steps (minimum spanning tree edges)
        mst_edges = [("C", "F"), ("C", "A"), ("A", "B"), ("B", "E"), ("E", "D"), ("E", "G")]
        colors = color_gradient([YELLOW], len(mst_edges))

        tree_vertices = set()

        for i, (u, v) in enumerate(mst_edges):
            edge = graph.edges.get((u, v)) or graph.edges.get((v, u))

            self.play(edge.animate.set_color(colors[i]).set_stroke(width=3, opacity=1),
                      weights[frozenset((u, v))].animate.scale(2),
                      run_time=1)
            self.wait(3)
            for vertex in (u, v):
                if vertex not in tree_vertices:
                    tree_vertices.add(vertex)
                    self.play(graph[vertex].animate.set_fill(color=GREEN), run_time=0.02)
        graph['C'].set_fill(color=GREEN)
        for i in range(6):
            (u, v) = mst_edges[i]
            edge = graph.edges.get((u, v)) or graph.edges.get((v, u))
            edge.set_color(YELLOW).set_stroke(width=3, opacity=1)
            weights[frozenset((u, v))].scale(2)
            self.add(edge, weights[frozenset((u, v))])

            for vertex in (u, v):
                if vertex not in tree_vertices:
                    tree_vertices.add(vertex)
                    graph[vertex].set_fill(color=GREEN)
                    self.add(graph[vertex])

        for v in vertices:
            label = Text(v, color=WHITE).scale(0.5)
            label.move_to(graph[v].get_center())  # center on the Dot
            self.add(label)


if __name__ == "__main__":

    with tempconfig({"quality": "high_quality"}): 
        scene=Prims()
        scene.render() 