import random
import matplotlib.pyplot as plt

def make_random_graph(vertices, p):
    graph = {}

    for i in range(1, vertices + 1):
        graph[i] = []

    for vertex in graph:
        for neighbour in range(vertex + 1, vertices + 1):
            if random.random() < p:
                graph[vertex].append(neighbour)
                graph[neighbour].append(vertex)
        random.shuffle(graph[vertex])
    return graph


def random_search(graph, start, end):
    queries = 0
    current = start
    while True:
        if current == end:
            return queries

        neighbours = graph[current]
        n = len(neighbours)
        queried = []

        if n > 20:  # n = 0 gave 1304, 3 game 1268, 5 gave 1302. More experimentation needed perhaps.
            while len(queried) < n:
                selection = random.choice(range(n))
                while selection in queried:
                    selection = random.choice(range(n))
                queried.append(selection)
                queries += 1
                if selection == end:
                    return queries
            current = random.choice(neighbours)
        else:
            current = random.choice(neighbours)
            queries += 1


def average_search_time(graph):
    vertices = len(graph)
    pairs = [(start, end) for start in range(1, vertices + 1) for end in range(start, vertices + 1) if start != end]
    total = 0
    for start, target in pairs:
        search_time = random_search(graph, start, target)
        total += search_time
        # print("Search time from", start, "to", target, "is", search_time)
    return total // len(pairs)


def print_random_graph():
    x_data = []
    y_data = []

    distribution = {}

    for i in range(50):
        random_graph = make_random_graph(100, 0.1)
        avg_search_time = average_search_time(random_graph)
        print("Search time for graph", i, "is", avg_search_time)
        if avg_search_time in distribution:
            distribution[avg_search_time] += 1
        else:
            distribution[avg_search_time] = 1

    for time in distribution:
        x_data += [time]
        y_data += [distribution[time]]

    plt.clf()
    plt.xlabel('Search Time')
    plt.ylabel('Number of Instances')
    plt.title('Instances of random graphs achieving search times')
    plt.plot(x_data, y_data, marker='.', markersize=5, linestyle='None', color='black')
    plt.savefig('question3random.png')


if __name__ == '__main__':
    print_random_graph()
