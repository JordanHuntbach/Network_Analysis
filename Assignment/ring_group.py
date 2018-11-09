import random
import matplotlib.pyplot as plt
import queue


def make_ring_group(m, k, p, q):
    vertices = m * k
    edges = 0

    # Initialize empty graph
    graph = {}
    for vertex in range(vertices):
        graph[vertex] = set()

    # Consider each vertex, making edges when necessary
    for u in range(vertices):
        u_group = u // k
        for v in range(u + 1, vertices):
            v_group = v // k
            probability = random.random()
            if u_group == v_group or (v_group - u_group == 1) or (u_group == 0 and v_group == m - 1):
                if probability <= p:
                    edges += 1
                    graph[u].add(v)
                    graph[v].add(u)
            else:
                if probability <= q:
                    edges += 1
                    graph[u].add(v)
                    graph[v].add(u)
    print("Made a ring group graph with", vertices, "vertices and", edges, "edges.")
    return graph


def compute_degrees(graph):
    degrees = {}

    for vertex in graph:
        degrees[vertex] = len(graph[vertex])

    return degrees


def get_degree_distribution(graph):
    # Get the degree of each vertex
    degrees = compute_degrees(graph)

    degree_distribution = {}

    # Initialise dictionary
    for vertex in degrees:
        degree_distribution[degrees[vertex]] = 0

    # Count number of vertices with the same degree
    for vertex in degrees:
        degree_distribution[degrees[vertex]] += 1

    return degree_distribution


def normalise(distribution, total):
    # Divide the distributions by the number of vertices.
    for degree in distribution:
        distribution[degree] /= total
    return distribution


def get_average_distribution(n):
    m = 100
    k = 20
    p = 0.26
    q = 0.5 - p

    cumulative_distribution = {}

    for i in range(n):
        print(i)

        # Make new graph
        graph = make_ring_group(m, k, p, q)

        # Get the normalised degree distributions
        distribution = normalise(get_degree_distribution(graph), m * k)

        # Add the distribution to the cumulative total
        for degree in distribution:
            if degree in cumulative_distribution:
                cumulative_distribution[degree] += distribution[degree]
            else:
                cumulative_distribution[degree] = distribution[degree]

    average_distribution = {}

    # Get the average by dividing the total cumulative distribution by the number of graphs used.
    for degree in cumulative_distribution:
        average_distribution[degree] = cumulative_distribution[degree] / n

    return average_distribution


def print_graph():
    x_data = []
    y_data = []

    averages = get_average_distribution(250)

    for degree in averages:
        x_data += [degree]
        y_data += [averages[degree]]

    parameters = "m = 100\nk = 20\np = 0.26\nq = 0.24"

    plt.clf()
    plt.xlabel('Degree')
    plt.ylabel('Normalized Rate')
    plt.title('Degree Distribution of Ring Group Graph')
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='black', label=parameters)
    plt.legend(loc="upper right")
    plt.savefig('question1.png')


def find_diameter(graph):
    print("Calculating diameter...")
    diameter = 0
    for vertex in graph:
        distance = max_dist(graph, vertex)
        if distance > diameter:
            diameter = distance
    print("Diameter =", diameter)
    return diameter


def max_dist(graph, source):  # Taken from the lectures
    """Finds the distance (the length of the shortest path) from the source to
    every other vertex in the same component using breadth-first search, and
    returns the value of the largest distance found."""
    q = queue.Queue()
    found = {}
    distance = {}
    for vertex in graph:                                        # Set up arrays
        found[vertex] = 0                                       # To record whether a vertex has been discovered
        distance[vertex] = -1                                   # and its distance from the source
    max_distance = 0
    found[source] = 1                                           # Initialize arrays with values for the source
    distance[source] = 0
    q.put(source)                                               # Put the source in the queue
    while not q.empty():
        current = q.get()                                       # Process the vertex at the front of the queue
        for neighbour in graph[current]:                        # Look at its neighbours
            if found[neighbour] == 0:                           # If undiscovered, update arrays and add to the queue
                found[neighbour] = 1
                distance[neighbour] = distance[current] + 1
                max_distance = distance[neighbour]
                q.put(neighbour)
    return max_distance


def print_graph_diameter():
    x_data = []

    plt.clf()
    plt.xlabel('Probability p')
    plt.ylabel('Diameter')
    plt.title('Diameter of Ring Group Graph with m=20, k=50')

    y_data = []
    for p in [x / 100 for x in range(0, 26)]:
        print("p =", p)
        graph = make_ring_group(20, 50, p, 0.002)
        diameter = find_diameter(graph)
        x_data += [p]
        y_data += [diameter]
    plt.plot(x_data, y_data, marker='+', markersize=7, linestyle='None', color='b', label="q = 0.002")

    y_data = []
    for p in [x / 100 for x in range(0, 26)]:
        print("p =", p)
        graph = make_ring_group(20, 50, p, 0.005)
        diameter = find_diameter(graph)
        y_data += [diameter]
    plt.plot(x_data, y_data, marker='x', markersize=7, linestyle='None', color='g', label="q = 0.005")

    y_data = []
    for p in [x / 100 for x in range(0, 26)]:
        print("p =", p)
        graph = make_ring_group(20, 50, p, 0.008)
        diameter = find_diameter(graph)
        y_data += [diameter]
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='r', label="q = 0.008")

    plt.legend(loc="upper right")
    plt.savefig('question1diameter.png')


if __name__ == '__main__':
    print_graph_diameter()
