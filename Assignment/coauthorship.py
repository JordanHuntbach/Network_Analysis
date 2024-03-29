import matplotlib.pyplot as plt
import random


def load_graph():

    txt = open("coauthorship.txt")

    # Initialise empty graph
    graph = {}
    for i in range(1, 1560):
        graph[i] = set()

    edges = 0
    # Read file and fill in edges
    for line in txt:
        neighbors = line.strip(' ').split(' ')
        vertex1 = int(neighbors[0])
        vertex2 = int(neighbors[1])

        if vertex2 not in graph[vertex1] and vertex1 != vertex2:
            edges += 1
            graph[vertex1].add(vertex2)
            graph[vertex2].add(vertex1)

    print("Loaded coauthorship graph with 1559 vertices and", edges, "edges.")
    return graph


def neighbours_subgraph(graph, node):
    subgraph = {}
    independent = set()

    # Get neighbours of the target
    neighbours = graph[node]

    # Create subgraph containing only the neighbours
    for neighbour in neighbours:
        subgraph[neighbour] = graph[neighbour].intersection(neighbours)
        # Add any neighbours that are already independent to this set
        if subgraph[neighbour] == set():
            independent.add(neighbour)

    return subgraph, independent


def recursion_boi(graph, current_best, remaining_neighbours, locked_in, depth):
    # This function is used to calculate the brilliance of a vertex from its subgraph
    if len(locked_in) >= len(remaining_neighbours) - 1:
        return remaining_neighbours
    for neighbour in remaining_neighbours.difference(locked_in):
        new_locked_in = set(locked_in)
        new_locked_in.add(neighbour)

        to_remove = graph[neighbour]
        new_remaining_members = remaining_neighbours.difference(to_remove)

        if len(new_remaining_members) > len(current_best):
            recursed = recursion_boi(graph, current_best, new_remaining_members, new_locked_in, depth + 1)
            if len(recursed) > len(current_best):
                current_best = recursed
    return current_best


def approximate_brilliance(graph):
    # This function keeps removing neighbours connected to the vertex with the smallest degree, until the whole set of
    # vertices is independent
    independent = set()
    to_remove = set()
    while True:
        min_degree = 2000
        min_vertex = None
        for vertex in graph:
            graph[vertex] = graph[vertex].difference(to_remove)
        for vertex in graph:
            degree = len(graph[vertex])
            if degree < min_degree:
                min_degree = degree
                min_vertex = vertex
                if degree <= 1:
                    break
        if min_vertex is not None:
            to_remove = set()
            independent.add(min_vertex)
            for vertex in graph[min_vertex]:
                to_remove.add(vertex)
                del graph[vertex]
            del graph[min_vertex]
        else:
            return len(independent)


def get_brilliance_distribution(graph):
    brilliances = {}
    count = 0
    for vertex in graph:
        count += 1
        print(count, "/", len(graph))

        # Get the subgraph consisting of just neighbour to the vertex
        subgraph, independent = neighbours_subgraph(graph, vertex)
        neighbours = graph[vertex]
        neighbour_count = len(neighbours)
        independent_count = len(independent)
        print("Vertex", vertex, "has", neighbour_count, "neighbours.")
        print(independent_count, "of them are immediately independent.")

        # If the graph is simple, calculate the brilliance, otherwise estimate it
        if neighbour_count - independent_count < 20:
            print("Calculating brilliance for vertex", vertex)
            brilliance = len(recursion_boi(subgraph, set(), neighbours, independent, 0))
        else:
            print("Approximating brilliance for vertex", vertex)
            brilliance = approximate_brilliance(subgraph)
        print("Brilliance:", brilliance)

        # Add the brilliance to the distribution
        if brilliance in brilliances:
            brilliances[brilliance] += 1
        else:
            brilliances[brilliance] = 1
    return brilliances


def normalise_distribution(distribution, count):
    normalised = {}
    for brilliance in distribution:
        normalised[brilliance] = distribution[brilliance] / count
    return normalised


def print_coauthorship():
    x_data = []
    y_data = []

    citation_graph = load_graph()
    distribution = normalise_distribution(get_brilliance_distribution(citation_graph), 1559)

    for degree in distribution:
        x_data += [degree]
        y_data += [distribution[degree]]

    plt.clf()
    plt.xlabel('Brilliance')
    plt.ylabel('Normalized Rate')
    plt.title('Brilliance Distribution of \'coauthorship.txt\'')
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='black')
    plt.savefig('question2coauthorship.png')


def print_ring_group():
    from Assignment.ring_group import make_ring_group

    x_data = []
    y_data = []

    graph = make_ring_group(16, 97, 0.047, 0.030)
    distribution = normalise_distribution(get_brilliance_distribution(graph), len(graph))

    for degree in distribution:
        x_data += [degree]
        y_data += [distribution[degree]]

    plt.clf()
    plt.xlabel('Brilliance')
    plt.ylabel('Normalized Rate')
    plt.title('Brilliance Distribution of Ring Group Graph')
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='black')
    plt.savefig('question2ring.png')


def make_pa_graph(vertices, degree):
    graph = {}
    prob_list = []
    edges = 0

    for i in range(degree):
        graph[i] = set()

    for i in range(degree):
        for j in range(i, degree):
            if i != j:
                prob_list.append(i)
                prob_list.append(j)
                graph[i].add(j)
                graph[j].add(i)
                edges += 1

    for vertex in range(degree, vertices):
        graph[vertex] = set()
        to_add = set()
        for i in range(degree):
            choice = random.choice(prob_list)
            to_add.add(choice)
        for neighbour in to_add:
            prob_list.append(vertex)
            prob_list.append(neighbour)
            graph[vertex].add(neighbour)
            graph[neighbour].add(vertex)
            edges += 1

    print("Made a PA graph with", vertices, "vertices and", edges, "edges.")
    return graph


def print_pa_graph():
    x_data = []
    y_data = []

    graph = make_pa_graph(1559, 27)
    distribution = normalise_distribution(get_brilliance_distribution(graph), len(graph))

    for degree in distribution:
        x_data += [degree]
        y_data += [distribution[degree]]

    plt.clf()
    plt.xlabel('Brilliance')
    plt.ylabel('Normalized Rate')
    plt.title('Brilliance Distribution of PA Graph')
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='black')
    plt.savefig('question2pa.png')


if __name__ == '__main__':
    print_pa_graph()
