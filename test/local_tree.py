from scipy.sparse.csgraph import dijkstra
from scipy.spatial.distance import cdist
import numpy as np

from collections import defaultdict


def print_tree(tree, node, prefix="", is_last=True):
    if prefix == "":
        print("   ",node)
    else:
        connector = "└── " if is_last else "├── "
        print(prefix + connector + str(node))

    children = sorted(tree[node])

    for i, child in enumerate(children):
        last_child = (i == len(children) - 1)

        child_prefix = prefix + ("    " if is_last else "│   ")

        print_tree(tree, child, child_prefix, last_child)

def main(total_points):
    # Generate points
    np.random.seed(42)
    pts = np.random.randint(-total_points, total_points,
        size=(total_points, 2))

    # Distance matrix
    dist_mat = cdist(pts, pts, metric="sqeuclidean")

    # Find hub (minimum total distance)
    hub = int(np.argmin(dist_mat.sum(axis=1)))

    # Shortest path distances
    distances = dijkstra(dist_mat, directed=False, indices=hub)

    # Shortest path tree
    _, pred = dijkstra(dist_mat, directed=False, indices=hub, return_predecessors=True)

    tree = defaultdict(list)

    for child, parent in enumerate(pred):
        if parent >= 0:
            tree[int(parent)].append(child)

    print("Points:")
    print(pts)

    print("\nHub:", hub)

    print("\nDistances:")
    print(distances)

    print("\nTree:")
    print_tree(tree, hub)

if __name__ == "__main__":
    main(16)
