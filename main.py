import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import minimum_spanning_tree, dijkstra
from scipy.spatial.distance import cdist

def get_center(points):
    centroid = (0,0)
    dist = np.sum((points - centroid) , axis=1) # squared distance
    return np.argmin(dist)

def plot_mst(points,mst):
    row, col = np.nonzero(mst)
    plt.figure()
    plt.scatter(points[:,0], points[:,1])

    for i, j in zip(row, col):
        x = [points[i, 0], points[j, 0]]
        y = [points[i, 1], points[j, 1]]
        plt.plot(x, y)

    plt.title("mst")
    plt.savefig("mst.png", dpi=300, bbox_inches="tight")

def plot_dijkstra(points, predecessors):
    plt.figure()
    plt.scatter(points[:,0], points[:,1])

    for i, p in enumerate(predecessors):
        if p == -9999: # source
            continue
        x = [points[i,0], points[p,0]]
        y = [points[i,1], points[p,1]]
        plt.plot(x, y)

    plt.title("dijkstra")
    plt.savefig("dijkstra.png", dpi=300, bbox_inches="tight")

def main():
    N = 64
    points = np.random.randint(-N, N+1, (N, 2))
    dist_matrix = cdist(points, points, metric='euclidean')

    # debug
    print(points)
    print(dist_matrix)

    mst = minimum_spanning_tree(dist_matrix)
    plot_mst(points, mst)

    source = get_center(points)
    dist_sq = dist_matrix**2
    dist, predecessors = dijkstra(dist_sq, directed=False,
                                    indices=source, return_predecessors=True)
    plot_dijkstra(points, predecessors)


if __name__ == "__main__":
    main()
