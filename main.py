import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.sparse.csgraph import dijkstra
from scipy.spatial.distance import cdist
from k_means_constrained import KMeansConstrained

from math import sqrt, ceil, floor


# =========================================================
# PIPELINE FUNCTIONS
# =========================================================

def get_num_cluster(total_points):
    pts_sqrt = sqrt(total_points)
    n_cluster = round(pts_sqrt)

    size_min, size_max = floor(pts_sqrt), ceil(pts_sqrt)
    print(f"[0] Cluster Size {n_cluster}")
    return (n_cluster, size_min, size_max)


def generate_points(total_points, seed=42):
    """Step 1 — Generate random 2D integer points."""
    np.random.seed(seed)
    coords = np.random.randint(-total_points, total_points,
                               size=(total_points, 2)).astype(float)
    print(f"[1] Generated {coords.shape}")
    return coords


def cluster_points(coords, n_clusters, size_min, size_max, seed=42):
    """Step 2 — Balanced K-Means: exactly pts_per_cluster per cluster."""
    model = KMeansConstrained(
        n_clusters=n_clusters,
        size_min=size_min,
        size_max=size_max,
        random_state=seed,
    )
    labels = model.fit_predict(coords)
    sizes  = [int(np.sum(labels == c)) for c in range(n_clusters)]
    print(f"[2] Balanced K-Means ")
    return labels


def find_hub(pts):
    """Return the index of the point closest to the cluster centroid."""
    return int(np.argmin(cdist(pts, pts.mean(axis=0, keepdims=True)).ravel()))


def build_clusters(coords, labels, n_clusters):
    """Step 3 — Organise points per cluster; move each hub to index 0."""
    cluster_pts = []
    hub_coords  = []

    for c in range(n_clusters):
        pts = coords[labels == c].copy()
        hi  = find_hub(pts)
        pts[[0, hi]] = pts[[hi, 0]]   # hub → index 0
        cluster_pts.append(pts)
        hub_coords.append(pts[0])

    hub_coords = np.array(hub_coords)
    print(f"[3] Hubs identified — one per cluster")
    return cluster_pts, hub_coords


def run_local_dijkstra(cluster_pts):
    """Steps 4 — Dijkstra on every cluster's complete (sq-dist) graph."""
    results = []
    for pts in cluster_pts:
        W              = cdist(pts, pts, metric='sqeuclidean')
        dist_from_hub  = dijkstra(W, directed=False, indices=0)
        results.append(dist_from_hub)
    print(f"[4] Local Dijkstra done for all {len(cluster_pts)} clusters")
    return results


def run_global_dijkstra(hub_coords):
    """Step 5 — Dijkstra on the complete graph of all cluster hubs."""
    global_hi  = find_hub(hub_coords)
    order      = [global_hi] + [i for i in range(len(hub_coords)) if i != global_hi]
    H          = hub_coords[order]          # global hub at row 0
    orig_ids   = order

    global_W        = cdist(H, H, metric='sqeuclidean')
    global_dist_mat = dijkstra(global_W, directed=False)
    global_dist     = global_dist_mat[0]    # distances from global hub

    print(f"[5] Global Dijkstra done — global hub = original cluster {orig_ids[0]}")
    return H, orig_ids, global_W, global_dist


def get_tree_edges(W, source=0):
    """Return (u, v) edge list for the shortest-path tree rooted at source."""
    _, pred = dijkstra(W, directed=False, indices=source, return_predecessors=True)
    return [(pred[v], v) for v in range(len(pred)) if pred[v] >= 0]


def visualize(cluster_pts, hub_coords, H, orig_ids, global_W, out_path="main.png"):
    """Step 6 — Two-panel plot: local clusters and global hub graph."""
    n_clusters = len(cluster_pts)
    COLORS     = plt.cm.viridis(np.linspace(0, 1, n_clusters))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 9))
    fig.suptitle("Level-1 Hierarchical Dijkstra Pipeline", fontsize=14)

    # ── Panel A: local clusters ───────────────────────────
    ax1.set_title("Local clusters — complete graphs + Dijkstra trees", fontsize=11)
    ax1.set_aspect('equal')
    ax1.grid(True, linewidth=0.3, alpha=0.4)

    for c in range(n_clusters):
        pts  = cluster_pts[c]
        col  = COLORS[c]
        W    = cdist(pts, pts, metric='sqeuclidean')
        tree = get_tree_edges(W)

        # faint complete-graph edges
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                ax1.plot([pts[i, 0], pts[j, 0]], [pts[i, 1], pts[j, 1]],
                         color=col, alpha=0.07, linewidth=0.4, zorder=1)

        # Dijkstra tree edges
        for u, v in tree:
            ax1.plot([pts[u, 0], pts[v, 0]], [pts[u, 1], pts[v, 1]],
                     color=col, linewidth=1.4, alpha=0.85, zorder=2)

        ax1.scatter(pts[1:, 0], pts[1:, 1], color=col, s=40, zorder=3,
                    edgecolors='white', linewidths=0.5)
        ax1.scatter(pts[0, 0], pts[0, 1], color=col, s=160, marker='*',
                    edgecolors='black', linewidths=0.6, zorder=4)

    ax1.legend(handles=[
        mpatches.Patch(color='none',     label='★  local hub'),
        plt.Line2D([0], [0], color='gray', linewidth=1.3, alpha=0.7,
                   label='—  Dijkstra tree'),
    ], fontsize=8, loc='lower right')

    # ── Panel B: global hubs ──────────────────────────────
    ax2.set_title("Global hubs — complete graph + Dijkstra tree", fontsize=11)
    ax2.set_aspect('equal')
    ax2.grid(True, linewidth=0.3, alpha=0.4)

    global_tree = get_tree_edges(global_W)

    # faint complete-graph edges
    for i in range(n_clusters):
        for j in range(i + 1, n_clusters):
            ax2.plot([H[i, 0], H[j, 0]], [H[i, 1], H[j, 1]],
                     color='gray', alpha=0.10, linewidth=0.5, zorder=1)

    # global Dijkstra tree edges
    for u, v in global_tree:
        ax2.plot([H[u, 0], H[v, 0]], [H[u, 1], H[v, 1]],
                 color='mediumpurple', linewidth=2.2, alpha=0.9, zorder=2)

    # hub nodes
    for i in range(n_clusters):
        col  = COLORS[orig_ids[i]]
        is_g = (i == 0)
        ax2.scatter(H[i, 0], H[i, 1],
                    color='tomato' if is_g else col,
                    s=250 if is_g else 100,
                    marker='*' if is_g else 'o',
                    edgecolors='black', linewidths=0.8, zorder=3)
        ax2.annotate(str(orig_ids[i]), (H[i, 0], H[i, 1]),
                     fontsize=7, ha='center', va='center',
                     color='white', fontweight='bold', zorder=4)

    ax2.legend(handles=[
        mpatches.Patch(color='tomato',    label='★  global hub'),
        mpatches.Patch(color='steelblue', label='●  local hub'),
        plt.Line2D([0], [0], color='mediumpurple', linewidth=2,
                   label='—  global Dijkstra tree'),
        plt.Line2D([0], [0], color='gray', linewidth=0.8, alpha=0.5,
                   label='—  complete graph'),
    ], fontsize=8, loc='lower right')

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"[6] Saved → {out_path}")


# =========================================================
# MAIN
# =========================================================

def main():
    RANDOM_SEED=42
    TOTAL_POINTS = 289

    n_cluster, size_min, size_max = get_num_cluster(TOTAL_POINTS)
    coords      = generate_points(TOTAL_POINTS, RANDOM_SEED)
    labels      = cluster_points(coords, n_cluster, size_min, size_max, RANDOM_SEED)
    cluster_pts, hub_coords = build_clusters(coords, labels, n_cluster)
    _           = run_local_dijkstra(cluster_pts)
    H, orig_ids, global_W, _ = run_global_dijkstra(hub_coords)
    visualize(cluster_pts, hub_coords, H, orig_ids, global_W)

if __name__ == "__main__":
    main()
