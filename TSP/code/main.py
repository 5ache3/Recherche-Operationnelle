import random as ra
import networkx as nx


def christofides(distance_dict):
    G = nx.Graph()
    
    # Add all nodes and edges to the graph
    nodes = set()
    for (u, v), dist in distance_dict.items():
        nodes.add(u)
        nodes.add(v)
        if u != v:  # avoid self-loops
            G.add_edge(u, v, weight=dist)
    
    nodes = sorted(nodes)
    
    # Step 1: Create a Minimum Spanning Tree (MST)
    mst = nx.minimum_spanning_tree(G)
    
    # Step 2: Find nodes with odd degree in the MST
    odd_degree_nodes = [v for v, degree in mst.degree() if degree % 2 == 1]
    
    # Step 3: Create a minimum weight perfect matching for the odd degree nodes
    subgraph = G.subgraph(odd_degree_nodes)
    min_weight_matching = nx.algorithms.min_weight_matching(subgraph, weight='weight')
    mst_weight=map(lambda item : distance_dict[item],min_weight_matching)
    # Convert matching to a set of edges for easier handling
    matching_edges = set()
    for u, v in min_weight_matching:
        if (u, v) not in matching_edges and (v, u) not in matching_edges:
            matching_edges.add((u, v))
    
    # Step 4: Combine MST and matching to create a multigraph where all nodes have even degree
    multigraph = nx.MultiGraph(mst)
    for u, v in matching_edges:
        multigraph.add_edge(u, v, weight=G[u][v]['weight'])
    
    # Step 5: Find an Eulerian circuit in this multigraph
    eulerian_circuit = list(nx.eulerian_circuit(multigraph))
    
    # Step 6: Convert Eulerian circuit to Hamiltonian path by skipping visited nodes
    visited = set()
    hamiltonian_path = []
    for u, v in eulerian_circuit:
        if u not in visited:
            visited.add(u)
            hamiltonian_path.append(u)
        if v not in visited:
            visited.add(v)
            hamiltonian_path.append(v)
    
    # Add the starting node at the end to complete the cycle
    hamiltonian_path.append(hamiltonian_path[0])
    
    # Calculate the total distance of the tour
    
    
    return hamiltonian_path



def count_cost(tour,distences):
    s=0
    for i in range(1,len(tour)):
        s+=distences[(tour[i],tour[i-1])]

    return s

def get_Distences(cyties='ABCDEFGH',seed=None):
    distences={}
    if seed:
        ra.seed(seed)
        
    for c1 in cyties:
        for c2 in cyties:
            if c1==c2:
                distences[(c1,c2)]=0
            if (c2,c1) in distences:
                distences[(c1,c2)]=distences[(c2,c1)]
                continue
            distences[(c1,c2)]=ra.randint(1,50)
    return distences

def tsp_nearest_neighbor(distnces,cyties):
    
    n = len(cyties) # nombres des villes
    
    start=cyties[0]
    
    visited = [False] * n 
    tour = [start] # add the first city to the tour
    visited[0] = True # mark the city as visited
    total_cost = 0 # null at the first city
    current = 0

    for _ in range(n-1):

        next_node = 0 # holds the index of the node with lowest cost 
        min_cost = float('inf')

        for i in range(n):
            c=cyties[i]
            c2=cyties[current]
            
            if not visited[i] and distnces[(c2,c)] < min_cost:
                # the curent point is the one with the minimum cost for now
                min_cost = distnces[(c2,c)]
                next_node = i
       # after this loop next will have the index of the city with the lowest cost         
        tour.append(cyties[next_node]) #we add it to the tour
        visited[next_node] = True # mark it as visited

        total_cost += min_cost 
        current = next_node
    total_cost += distnces[(cyties[next_node],cyties[0])]
    tour.append(cyties[0])

    return tour, total_cost

def two_opt(tour, distances):
    best = tour[:]
    improved = True

    while improved:
        improved = False
        best_distance = count_cost(best, distances)

        for i in range(1, len(best) - 2):  
            for j in range(i + 1, len(best) - 1):
                if j - i == 1:
                    continue  # 
                new_tour = best[:i] + best[i:j][::-1] + best[j:]
                new_distance = count_cost(new_tour, distances)

                if new_distance < best_distance:
                    best = new_tour
                    improved = True
                    break  
            if improved:
                break

    return best


def three_opt_swap(dist,tour, i, j, k):
    # All 7 possible reconnections for 3-opt on edges (i, i+1), (j, j+1), (k, k+1)
    a, b, c, d, e, f = tour[i], tour[i+1], tour[j], tour[j+1], tour[k], tour[(k+1) % len(tour)]

    # The possible reconnections as new tours slices:
    # Original: [0..i] + [i+1..j] + [j+1..k] + [k+1..end]

    # Each option rearranges and/or reverses these slices:
    options = []

    # 1. No change (identity) - just return None since no improvement
    # 2. Reverse segment i+1 to j
    options.append(tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:])

    # 3. Reverse segment j+1 to k
    options.append(tour[:j+1] + tour[j+1:k+1][::-1] + tour[k+1:])

    # 4. Reverse segment i+1 to j and j+1 to k
    options.append(tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:k+1][::-1] + tour[k+1:])

    # 5. Swap segments i+1 to j and j+1 to k
    options.append(tour[:i+1] + tour[j+1:k+1] + tour[i+1:j+1] + tour[k+1:])

    # 6. Reverse segment i+1 to j and swap with segment j+1 to k
    options.append(tour[:i+1] + tour[j+1:k+1] + tour[i+1:j+1][::-1] + tour[k+1:])

    # 7. Reverse segment j+1 to k and swap with segment i+1 to j
    options.append(tour[:i+1] + tour[j+1:k+1][::-1] + tour[i+1:j+1] + tour[k+1:])

    best_tour = None
    best_distance = count_cost(tour, dist)

    for opt in options:
        length = count_cost(opt, dist)
        if length < best_distance:
            best_tour = opt
            best_distance = length

    return best_tour, best_distance


def three_opt(tour, dist):
    improved = True
    while improved:
        improved = False
        n = len(tour) - 1  # assuming tour ends where it starts
        for i in range(n - 5):
            for j in range(i + 2, n - 3):
                for k in range(j + 2, n - 1):
                    new_tour, new_dist = three_opt_swap(dist,tour, i, j, k)
                    if new_tour:
                        tour = new_tour
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
    return tour




nb_villes=50
villes=[f'ville_{i}' for i in range(nb_villes)]

distences=get_Distences(villes)


nn_tour,nn_cost=tsp_nearest_neighbor(distences,villes)
print(f'nerest neighbour solution : {nn_cost}')

nn_2opt_tour=two_opt(nn_tour,distences)
nn_2opt_cost=count_cost(nn_2opt_tour,distences)
print(f'nerest neighbour + 2-opt solution : {nn_2opt_cost}')


nn_3opt_tour=three_opt(nn_2opt_tour,distences)
nn_3opt_cost=count_cost(nn_3opt_tour,distences)
print(f'nerest neighbour + 2-opt + 3-opt solution : {nn_3opt_cost} ')



chr_tour=christofides(distences)
chr_cost=count_cost(chr_tour,distences)
print(f'\n\n\nchristophedes solution : {chr_cost}')
chr_2opt_tour=two_opt(chr_tour,distences)
chr_2opt_cost=count_cost(chr_2opt_tour,distences)
print(f'christophedes + 2-opt solution : {chr_2opt_cost}')

chr_3opt_tour=three_opt(chr_2opt_tour,distences)
chr_3opt_cost=count_cost(chr_3opt_tour,distences)
print(f'christophedes + 2-opt + 3-opt solution : {chr_3opt_cost}')

