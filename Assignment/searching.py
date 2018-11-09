import random
import matplotlib.pyplot as plt


def make_random_graph(vertices, p):
    graph = {}
    edges = 0

    for i in range(1, vertices + 1):
        graph[i] = []

    for vertex in graph:
        for neighbour in range(vertex + 1, vertices + 1):
            if random.random() < p:
                graph[vertex].append(neighbour)
                graph[neighbour].append(vertex)
                edges += 1
        random.shuffle(graph[vertex])

    print("Made a random graph with", vertices, "vertices and", edges, "edges.")
    return graph


def random_search(graph, start, end):
    # The commented out code was for a different algorithm, which turned out to be worse.
    queries = 0
    current = start
    while True:
        neighbours = graph[current]
        degree = len(neighbours)
        if current == end:
            return queries
        if degree > 13:
            queried = []
            while len(queried) < degree:
                options = set(neighbours).difference(set(queried))
                options = list(options)
                selection = random.choice(options)
                queried.append(selection)
                queries += 1
                if selection == end:
                    return queries
            current = random.choice(queried)
        else:
            current = random.choice(graph[current])
            queries += 1


def average_search_time_random(graph):
    vertices = len(graph)
    total = 0
    pairs = 0

    # Calculate the search time for each pair of vertices and average the result
    for start in range(1, vertices + 1):
        for target in range(start + 1, vertices + 1):
            try:
                search_time = random_search(graph, start, target)
                total += search_time
                pairs += 1
            except KeyboardInterrupt:
                print("nice")
                pass
            # print("Search time from", start, "to", target, "is", search_time)
    return total // pairs


def print_random_graph():
    x_data = []
    y_data = []

    distribution = {}

    # Create n graphs, getting their average search time and adding the result to the distribution
    graphs = 250
    for i in range(graphs):
        random_graph = make_random_graph(100, 0.1)
        avg_search_time = average_search_time_random(random_graph)
        print("Search time for graph", i, "is", avg_search_time)
        if avg_search_time in distribution:
            distribution[avg_search_time] += 1
        else:
            distribution[avg_search_time] = 1

    for time in distribution:
        x_data += [time]
        y_data += [distribution[time] / graphs]

    plt.clf()
    plt.xlabel('Search Time')
    plt.ylabel('Number of Instances (Normalised)')
    plt.title('Instances of Random Graphs achieving search times')
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='black')
    plt.savefig('question3random.png')


def ring_set_to_list(graph):
    # Just a helper function that converts the sets in a graph to lists
    new_graph = {}
    for vertex in graph:
        new_graph[vertex] = list(graph[vertex])
    return new_graph


def distance_between_groups(a, b, k):
    # Finds the distance between two groups in a ring group graph
    normal = abs(a - b)
    if a < b:
        looping = a + k - b
    else:
        looping = b + k - a
    return min(normal, looping)


def ring_search(graph, start, end, k):
    queries = 0
    current = start
    target_group = end // k
    current_group = current // k
    while True:
        if current == end:
            return queries

        neighbours = graph[current]
        n = len(neighbours)
        queried = []

        # Query all neighbours
        while len(queried) < n:
            selection = random.choice(list(set(neighbours).difference(set(queried))))
            queried.append(selection)
            queries += 1
            selection_group = selection // k

            # If we stumble across the target, end here
            if selection == end:
                return queries
            # If we can move into an adjacent group, end here
            elif distance_between_groups(current_group, target_group, k) > 1 >= distance_between_groups(selection_group, target_group, k):
                current = selection
                break

        # The list of neighbours that are in adjacent groups to the target
        close_enough = [x for x in queried if distance_between_groups((x // k), target_group, k) <= 1]

        # If already adjacent, try to stay there
        if distance_between_groups(current_group, target_group, k) <= 1 and len(close_enough) > 0:
            current = random.choice(close_enough)
        else:
            # Move as close to the target group as possible
            min_distance = k
            current = random.choice(queried)
            for vertex in queried:
                distance = distance_between_groups((vertex // k), target_group, k)
                if distance < min_distance:
                    min_distance = distance
                    current = vertex


def average_search_time_ring():
    from Assignment.ring_group import make_ring_group

    m = 10
    k = 10
    p = 0.3
    q = 0.05
    ring_graph = ring_set_to_list(make_ring_group(m, k, p, q))
    vertices = m * k

    # Get every pair of vertices...
    pairs = [(start, end) for start in range(0, vertices) for end in range(start, vertices) if start != end]

    # ... and calculate the search time between them. Return the average.
    total = 0
    for start, target in pairs:
        search_time = ring_search(ring_graph, start, target, k)
        total += search_time
        # print("Search time from", start, "to", target, "is", search_time)
    return total // len(pairs)


def print_ring_graph():
    x_data = []
    y_data = []

    distribution = {}

    # Create n graphs, and add their average search times to a distribution which we can display.
    graphs = 300
    for i in range(graphs):
        avg_search_time = average_search_time_ring()
        print("Search time for graph", i, "is", avg_search_time)
        if avg_search_time in distribution:
            distribution[avg_search_time] += 1
        else:
            distribution[avg_search_time] = 1

    for time in distribution:
        x_data += [time]
        y_data += [distribution[time] / graphs]

    plt.clf()
    plt.xlabel('Search Time')
    plt.ylabel('Number of Instances (Normalised)')
    plt.title('Instances of Ring Group Graphs achieving search times')
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='black')
    plt.savefig('question3ring.png')


if __name__ == '__main__':
    print_random_graph()
