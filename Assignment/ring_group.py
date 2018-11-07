import random
import matplotlib.pyplot as plt


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
    m = 20
    k = 50
    p = 0.3
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

    averages = get_average_distribution(100)

    for degree in averages:
        x_data += [degree]
        y_data += [averages[degree]]

    plt.clf()
    plt.xlabel('Degree')
    plt.ylabel('Normalized Rate')
    plt.title('Degree Distribution of Ring Group Graph')
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='black')
    plt.savefig('question1.png')


if __name__ == '__main__':
    print_graph()
