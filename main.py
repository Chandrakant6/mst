import numpy as np

from math import sqrt
from math import floor
from math import ceil

from scipy.spatial.distance import cdist
from scipy.sparse.csgraph import dijkstra

from k_means_constrained import (
    KMeansConstrained
)

from tree import print_tree

from eval import (
    evaluate_tree
)


def run_dijkstra(points):

    distance_matrix = cdist(
        points,
        points,
        metric="sqeuclidean"
    )

    hub_index = int(
        np.argmin(
            distance_matrix.sum(axis=1)
        )
    )

    _, predecessors = dijkstra(
        distance_matrix,
        directed=False,
        indices=hub_index,
        return_predecessors=True
    )

    edges = [
        (parent, child)
        for child, parent in enumerate(
            predecessors
        )
        if parent >= 0
    ]

    return {
        "hub": hub_index,
        "predecessors": predecessors,
        "edges": edges
    }


def hierarchical_dijkstra(
    all_points
):

    total_points = len(
        all_points
    )

    cluster_count = round(
        sqrt(total_points)
    )

    cluster_labels = (
        KMeansConstrained(
            n_clusters=cluster_count,
            size_min=floor(
                sqrt(total_points)
            ),
            size_max=ceil(
                sqrt(total_points)
            ),
            random_state=42
        )
        .fit_predict(all_points)
    )

    local_trees = []

    hub_points = []

    for cluster_id in range(
        cluster_count
    ):

        cluster_points = all_points[
            cluster_labels == cluster_id
        ]

        tree = run_dijkstra(
            cluster_points
        )

        local_trees.append(
            (
                cluster_points,
                tree
            )
        )

        hub_points.append(
            cluster_points[
                tree["hub"]
            ]
        )

    hub_points = np.array(
        hub_points
    )

    global_tree = run_dijkstra(
        hub_points
    )

    return (
        local_trees,
        hub_points,
        global_tree
    )


def main():

    total_points = 255

    np.random.seed(42)

    all_points = np.random.randint(
        -total_points,
        total_points,
        size=(
            total_points,
            2
        )
    ).astype(float)

    (
        local_trees,
        hub_points,
        global_tree
    ) = hierarchical_dijkstra(
        all_points
    )

    print(
        "\nGLOBAL NETWORK"
    )

    evaluate_tree(
        hub_points,
        global_tree
    )

    print(
        "\nGLOBAL TREE"
    )

    print_tree(
        global_tree["predecessors"],
        global_tree["hub"]
    )

    for cluster_id, (
        cluster_points,
        tree
    ) in enumerate(
        local_trees
    ):

        print(
            f"\nCLUSTER {cluster_id}"
        )

        evaluate_tree(
            cluster_points,
            tree
        )

        print_tree(
            tree["predecessors"],
            tree["hub"]
        )


if __name__ == "__main__":
    main()
