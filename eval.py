import numpy as np

from collections import defaultdict


def compute_depths(
    predecessors,
    root_node
):

    children = defaultdict(list)

    for child, parent in enumerate(predecessors):
        if parent >= 0:
            children[parent].append(child)

    depths = {
        root_node: 0
    }

    stack = [root_node]

    while stack:

        node = stack.pop()

        for child in children[node]:

            depths[child] = (
                depths[node] + 1
            )

            stack.append(child)

    return list(
        depths.values()
    )


def compute_hub_distances(
    points,
    tree
):

    children = defaultdict(list)

    for parent, child in tree["edges"]:
        children[parent].append(child)

    distances = {
        tree["hub"]: 0.0
    }

    stack = [tree["hub"]]

    while stack:

        node = stack.pop()

        for child in children[node]:

            edge_length = np.linalg.norm(
                points[node] - points[child]
            )

            distances[child] = (
                distances[node]
                + edge_length
            )

            stack.append(child)

    return list(
        distances.values()
    )


def evaluate_tree(
    points,
    tree
):

    edge_lengths = [
        np.linalg.norm(
            points[parent] - points[child]
        )
        for parent, child in tree["edges"]
    ]

    depths = compute_depths(
        tree["predecessors"],
        tree["hub"]
    )

    hub_distances = compute_hub_distances(
        points,
        tree
    )


    print(
        f"Total Length  : {sum(edge_lengths):.2f}"
    )

    print(
        f"Avg Edge      : {np.mean(edge_lengths):.2f}"
    )

    print(
        f"Max Edge      : {np.max(edge_lengths):.2f}"
    )

    print(
        f"Avg Depth     : {np.mean(depths):.2f}"
    )

    print(
        f"Max Depth     : {np.max(depths)}"
    )

    print(
        f"Avg Hub Dist  : {np.mean(hub_distances):.2f}"
    )

    print(
        f"Max Hub Dist  : {np.max(hub_distances):.2f}"
    )
