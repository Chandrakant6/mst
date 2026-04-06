import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import cdist

def plot_mst(points,mst):
    row, col = np.nonzero(mst)
    plt.figure()
    plt.scatter(points[:,0], points[:,1])

    for i, j in zip(row, col):
        x = [points[i, 0], points[j, 0]]
        y = [points[i, 1], points[j, 1]]
        plt.plot(x, y)

    plt.savefig("mst.png", dpi=300, bbox_inches="tight")

def main():
    N = 64
    points = np.random.uniform(-N, N, (N, 2))
    dist_matrix = cdist(points, points, metric='euclidean')
    mst = minimum_spanning_tree(dist_matrix)
    plot_mst(points, mst)

if __name__ == "__main__":
    main()
