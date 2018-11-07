import na2loadgraph
import na2degrees

citations_graph = na2loadgraph.load_graph("alg_phys-cite.txt")

in_degrees = na2degrees.compute_in_degrees(citations_graph)
print("In-degrees:")
for key in sorted(in_degrees):
    print(key, ":", in_degrees[key])

print("\nDistribution:")
distribution = na2degrees.in_degree_distribution(citations_graph)
for key in sorted(distribution):
    print(key, ":", distribution[key])
