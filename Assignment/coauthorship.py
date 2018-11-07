import matplotlib.pyplot as plt


def load_graph():

    txt = open("coauthorship.txt")
    # TODO: This doesn't load the vertices with no co-authors. Load them first, then fill in the blanks.

    graph = {}

    for i in range(1, 1560):
        graph[i] = set()

    for line in txt:
        neighbors = line.strip(' ').split(' ')
        vertex1 = int(neighbors[0])
        vertex2 = int(neighbors[1])

        if vertex2 not in graph[vertex1] and vertex1 != vertex2:
            graph[vertex1].add(vertex2)
            graph[vertex2].add(vertex1)

    return graph


def neighbours_subgraph(graph, node):
    subgraph = {}
    independent = set()

    neighbours = graph[node]
    for neighbour in neighbours:
        subgraph[neighbour] = graph[neighbour].intersection(neighbours)
        if subgraph[neighbour] == set():
            independent.add(neighbour)

    return subgraph, independent


def recursion_boi(graph, current_best, remaining_neighbours, locked_in, depth):
    if len(locked_in) >= len(remaining_neighbours) - 1:
        return remaining_neighbours
    for neighbour in remaining_neighbours.difference(locked_in):
        if neighbour not in locked_in:
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
        subgraph, independent = neighbours_subgraph(graph, vertex)
        neighbours = graph[vertex]
        neighbour_count = len(neighbours)
        independent_count = len(independent)
        print("Vertex", vertex, "has", neighbour_count, "neighbours.")
        print(independent_count, "of them are immediately independent.")
        if neighbour_count - independent_count < 20:
            print("Calculating brilliance for vertex", vertex)
            brilliance = len(recursion_boi(subgraph, set(), neighbours, independent, 0))
        else:
            print("Approximating brilliance for vertex", vertex)
            brilliance = approximate_brilliance(subgraph)
        print("Brilliance:", brilliance)
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
    distribution = normalise_distribution(get_brilliance_distribution(citation_graph), len(citation_graph))

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

    graph = make_ring_group(16, 100, 0.06, 0.03)
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


if __name__ == '__main__':
    print_coauthorship()
