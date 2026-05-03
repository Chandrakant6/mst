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
    plt.figure(figsize=(2,2))
    plt.scatter(points[:,0], points[:,1])

    for i, j in zip(row, col):
        x = [points[i, 0], points[j, 0]]
        y = [points[i, 1], points[j, 1]]
        plt.plot(x, y)

    plt.title("mst")
    plt.savefig("mst.png", dpi=300, bbox_inches="tight")

def plot_dijkstra(points, predecessors):
    plt.figure(figsize=(2,2))
    plt.scatter(points[:,0], points[:,1])

    for i, p in enumerate(predecessors):
        if p == -9999: # source
            continue
        x = [points[i,0], points[p,0]]
        y = [points[i,1], points[p,1]]
        plt.plot(x, y)

    plt.title("dijkstra")
    plt.savefig("dijkstra.png", dpi=300, bbox_inches="tight")

def plot_diff(points, mst, predecessors):
    row, col = np.nonzero(mst)
    mst_edges = set((min(i,j), max(i,j)) for i,j in zip(row,col))

    dijk_edges = set()
    for i, p in enumerate(predecessors):
        if p != -9999:
            dijk_edges.add((min(i,p), max(i,p)))

    only_mst   = mst_edges - dijk_edges
    only_dijk  = dijk_edges - mst_edges
    common     = mst_edges & dijk_edges

    plt.figure(figsize=(2,2))
    plt.scatter(points[:,0], points[:,1])

    for i,j in common:
        plt.plot([points[i,0],points[j,0]], [points[i,1],points[j,1]], 'g')
    for i,j in only_mst:
        plt.plot([points[i,0],points[j,0]], [points[i,1],points[j,1]], 'b--')
    for i,j in only_dijk:
        plt.plot([points[i,0],points[j,0]], [points[i,1],points[j,1]], 'r:')

    plt.title("mst vs dijkstra")
    plt.savefig("diff.png", dpi=300, bbox_inches="tight")


def main(n=16):
    points = np.random.randint(-n, n-1, (n-1, 2))
    dist_matrix = cdist(points, points, metric='euclidean')

    mst = minimum_spanning_tree(dist_matrix)
    plot_mst(points, mst)

    source = get_center(points)
    dist_sq = dist_matrix**2
    dist, predecessors = dijkstra(dist_sq, directed=False,
            indices=source, return_predecessors=True)

    plot_dijkstra(points, predecessors)

    plot_diff(points, mst, predecessors)

    # debug
    print("points:" ,points, "\n")
    print("dist_matrix:", dist_matrix, "\n")
    print("mst:", mst, "\n------------\n")

    print("source:", source, "\n")
    print("dist_sq:", dist_sq, "\n")
    print("dijkstra:", dist, predecessors)

if __name__ == "__main__":
    main()
