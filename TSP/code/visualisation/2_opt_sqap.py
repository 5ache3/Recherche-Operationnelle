from manim import *
import itertools
import numpy as np
import random as rd

def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))



def tsp_shortest_path(nodes):
    indices = list(range(len(nodes)))
    start = indices[0]
    other_indices = indices[1:]

    min_path = None
    min_dist = float('inf')

    for perm in itertools.permutations(other_indices):
        path = [start] + list(perm) + [start]  # round trip
        dist = 0
        for i in range(len(path) - 1):
            p1 = np.array(nodes[path[i]])
            p2 = np.array(nodes[path[i + 1]])
            dist += np.linalg.norm(p1 - p2)
        if dist < min_dist:
            min_dist = dist
            min_path = path

    return min_path, min_dist

def tsp_nearest_neighbor(nodes):
    n = len(nodes)
    visited = [False] * n
    path = [0]  # start at node 0
    visited[0] = True
    total_dist = 0

    current = 0
    for _ in range(n - 1):
        nearest = None
        min_dist = float('inf')
        for i in range(n):
            if not visited[i]:
                dist = np.linalg.norm(np.array(nodes[current]) - np.array(nodes[i]))
                if dist < min_dist:
                    min_dist = dist
                    nearest = i
        path.append(nearest)
        visited[nearest] = True
        total_dist += min_dist
        current = nearest

    # Return to start
    path.append(0)
    total_dist += np.linalg.norm(np.array(nodes[current]) - np.array(nodes[0]))

    return path, total_dist

def path_distance(path, nodes):
    return sum(
        euclidean_distance(nodes[path[i]], nodes[path[i + 1]])
        for i in range(len(path) - 1)
    )

def two_opt_step(path, nodes):
    """Performs a single 2-opt improvement step on the path."""
    best_distance = path_distance(path, nodes)
    n = len(path)
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            new_path = path[:i] + path[i:j+1][::-1] + path[j+1:]
            new_distance = path_distance(new_path, nodes)
            if new_distance < best_distance:
                return new_path, True
    return path, False

def nodes_mover(nodes):
    lis=[]
    for i in range(len(nodes)):
        item=nodes[i]
        item[0]=item[0]+4
        lis.append(item)
    return lis

class Two_opt_tsp(Scene):

    def __init__(self,nodes,**kwargs):
        self.nodes=nodes
        super().__init__(**kwargs)


    def draw_nodes(self, nodes):
        dots = []
        labels = []
        for i, (x, y) in enumerate(nodes):
            dot = Dot(point=[x, y, 0], color=BLUE)
            label = Text(str(i), font_size=24).next_to(dot, UP)
            dots.append(dot)
            labels.append(label)
        return dots, labels
    
    def draw_edges(self, nodes, edge_list, **kwargs):
        lines = VGroup()
        for u, v in edge_list:
            start = np.array([*nodes[u], 0])
            end = np.array([*nodes[v], 0])
            line = Line(start, end, **kwargs)  # Pass any additional kwargs to the Line constructor
            lines.add(line)
        return lines


    def draw_paths(self, nodes, path, color=YELLOW, width=4):
        edges = VGroup()
        for i in range(len(path) - 1):
            start = np.array([*nodes[path[i]], 0])
            end = np.array([*nodes[path[i + 1]], 0])
            line = Line(start, end, color=color, stroke_width=width)
            edges.add(line)
        return edges
    

    def construct(self):
        def container(self,nodes,path,total_dist,label,mst=False):
            if mst :
                edges=self.draw_edges(nodes,path)
            else:
                edges = self.draw_paths(nodes, path)
            dots, labels = self.draw_nodes(nodes)
            graph=VGroup(*edges, *dots)
            distance_label = Text(f"{label}: {total_dist:.2f}", font_size=24).next_to(graph, DOWN)
            box=SurroundingRectangle(VGroup(graph,distance_label), color=WHITE, buff=0.2)
            
            return VGroup(graph,box,distance_label)
        
        title=Title("Nearest neighbour + 2-opt swap")
        self.add(title)
        nodes=self.nodes
        path, best_len = tsp_nearest_neighbor(nodes)
        opt_path, opt_dist = tsp_shortest_path(nodes)
        opt_box=container(self, nodes, opt_path,opt_dist, "optimal").shift(LEFT*4)

        local_nodes=nodes_mover(nodes)

        xs = [p[0] for p in local_nodes]
        ys = [p[1] for p in local_nodes]
        padding = 0.5
        lower_left = np.array([min(xs)-padding, min(ys)-padding, 0])
        upper_right = np.array([max(xs)+padding, max(ys)+padding, 0])
        box = Rectangle(
            width=upper_right[0]-lower_left[0],
            height=upper_right[1]-lower_left[1]
        ).move_to((lower_left + upper_right) / 2)
        self.play(Create(box),Create(opt_box))

        # 3) Draw local_nodes without labels
        dots = self.draw_nodes(local_nodes)[0]  # Removing labels from nodes
        self.play(*[FadeIn(d) for d in dots])

        # 4) Draw initial tour
        tour_lines = self.draw_edges(local_nodes, [(path[i], path[i+1]) for i in range(len(path)-1)],
                                    color=YELLOW, stroke_width=4)
        self.play(Create(tour_lines))
        self.wait(0.5)

        # 5) Text showing the current best tour length, positioned under the box
        info = Text(f"Best tour length: {best_len:.2f}", font_size=24)
        info.next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(info))
        self.wait(1)

        # 6) Show the current tour and update using 2-opt swaps
        n = len(path)
        for i in range(1, n-2):
            for j in range(i+1, n-1):
                # Create candidate tour after 2-opt swap
                candidate = path[:i] + path[i:j+1][::-1] + path[j+1:]
                old_len = path_distance(path, local_nodes)
                new_len = path_distance(candidate, local_nodes)

                # Highlight the edges being swapped
                seg_old = self.draw_edges(
                    local_nodes,
                    [(path[i-1], path[i]), (path[j], path[j+1])],
                    color=RED, stroke_width=6,
                )
                seg_new = self.draw_edges(
                    local_nodes,
                    [(path[i-1], path[j]), (path[i], path[j+1])],
                    color=GREEN, stroke_width=6,
                )
                # Show old edges removal → new edges
                self.play(ReplacementTransform(seg_old, seg_new), run_time=1)

                if new_len < old_len:
                    # Accept the candidate if it's better
                    self.remove(tour_lines)
                    tour_lines = self.draw_edges(
                        local_nodes,
                        [(candidate[k], candidate[k+1]) for k in range(len(candidate)-1)],
                        color=YELLOW, stroke_width=4
                    )
                    self.play(Create(tour_lines), run_time=1)
                    path, best_len = candidate, new_len

                    # Update info text to show new best tour length
                    new_info = Text(f"Best tour length: {best_len:.2f}",
                                    font_size=24).move_to(info)
                    self.play(Transform(info, new_info), run_time=0.8)
                    self.wait(0.3)
                else:
                    # Reject the candidate if it's not better
                    self.play(FadeOut(seg_new), run_time=0.5)

        self.wait(2)


if __name__=="__main__":
    nodes = [[rd.random()*4-2, rd.random()*4-2] for _ in range(8)]
    print(nodes)
    with tempconfig({"quality": "high_quality"}): 
        scene=Two_opt_tsp(nodes)
        scene.render()