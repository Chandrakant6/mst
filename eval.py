import numpy as np

from collections import defaultdict


def build_children(predecessors):

    children = defaultdict(list)

    for child, parent in enumerate(predecessors):

        if parent >= 0:
            children[parent].append(child)

    return children


def compute_edge_lengths(
    points,
    edges
):

    return [
        np.linalg.norm(
            points[parent]
            - points[child]
        )
        for parent, child in edges
    ]


def compute_depths(
    predecessors,
    root_node
):

    children = build_children(
        predecessors
    )

    depths = np.zeros(
        len(predecessors),
        dtype=int
    )

    stack = [root_node]

    while stack:

        node = stack.pop()

        for child in children[node]:

            depths[child] = (
                depths[node] + 1
            )

            stack.append(child)

    return depths


def compute_hub_distances(
    points,
    predecessors,
    root_node
):

    children = build_children(
        predecessors
    )

    distances = np.zeros(
        len(predecessors)
    )

    stack = [root_node]

    while stack:

        node = stack.pop()

        for child in children[node]:

            edge_length = np.linalg.norm(
                points[node]
                - points[child]
            )

            distances[child] = (
                distances[node]
                + edge_length
            )

            stack.append(child)

    return distances


def compute_leaf_count(
    children,
    root_node,
    node_count
):

    return sum(
        1
        for node in range(node_count)
        if node != root_node
        and len(children[node]) == 0
    )


def compute_hub_degree(
    children,
    root_node
):

    return len(
        children[root_node]
    )


def compute_branching_factor(
    children
):

    branch_counts = [
        len(nodes)
        for nodes in children.values()
        if len(nodes) > 0
    ]

    if not branch_counts:
        return 0

    return np.mean(
        branch_counts
    )


def compute_depth_imbalance(
    depths
):

    avg_depth = np.mean(
        depths
    )

    if avg_depth == 0:
        return 0

    return (
        np.max(depths)
        / avg_depth
    )


def compute_diameter(
    points,
    edges
):

    adjacency = defaultdict(list)

    for parent, child in edges:

        weight = np.linalg.norm(
            points[parent]
            - points[child]
        )

        adjacency[parent].append(
            (child, weight)
        )

        adjacency[child].append(
            (parent, weight)
        )

    def farthest(start):

        stack = [(start, 0.0)]

        visited = set()

        best_node = start
        best_distance = 0.0

        while stack:

            node, dist = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            if dist > best_distance:

                best_node = node
                best_distance = dist

            for nxt, weight in adjacency[node]:

                stack.append(
                    (
                        nxt,
                        dist + weight
                    )
                )

        return (
            best_node,
            best_distance
        )

    node_a, _ = farthest(0)

    _, diameter = farthest(
        node_a
    )

    return diameter


def compute_stretch(
    points,
    predecessors,
    root_node
):

    route_distances = (
        compute_hub_distances(
            points,
            predecessors,
            root_node
        )
    )

    direct_distances = np.linalg.norm(
        points - points[root_node],
        axis=1
    )

    valid = (
        direct_distances > 0
    )

    stretch = (
        route_distances[valid]
        /
        direct_distances[valid]
    )

    return (
        np.mean(stretch),
        np.max(stretch)
    )


def evaluate_tree(
    points,
    tree
):

    root_node = tree["hub"]
    predecessors = tree["predecessors"]
    edges = tree["edges"]

    children = build_children(
        predecessors
    )

    edge_lengths = (
        compute_edge_lengths(
            points,
            edges
        )
    )

    depths = compute_depths(
        predecessors,
        root_node
    )

    hub_distances = (
        compute_hub_distances(
            points,
            predecessors,
            root_node
        )
    )

    avg_stretch, max_stretch = (
        compute_stretch(
            points,
            predecessors,
            root_node
        )
    )

    metrics = {

        "total_length":
            np.sum(edge_lengths),

        "avg_edge":
            np.mean(edge_lengths),

        "max_edge":
            np.max(edge_lengths),

        "avg_depth":
            np.mean(depths),

        "max_depth":
            np.max(depths),

        "avg_hub_dist":
            np.mean(hub_distances),

        "max_hub_dist":
            np.max(hub_distances),

        "leaf_count":
            compute_leaf_count(
                children,
                root_node,
                len(predecessors)
            ),

        "hub_degree":
            compute_hub_degree(
                children,
                root_node
            ),

        "branching_factor":
            compute_branching_factor(
                children
            ),

        "depth_imbalance":
            compute_depth_imbalance(
                depths
            ),

        "diameter":
            compute_diameter(
                points,
                edges
            ),

        "avg_stretch":
            avg_stretch,

        "max_stretch":
            max_stretch,
    }

    for key, value in metrics.items():

        print(
            f"{key:20}: {value:.2f}"
        )

    return metrics
