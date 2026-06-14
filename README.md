# Hierarchical Dijkstra Pipeline

A hierarchical routing pipeline that partitions a large set of points into balanced clusters, constructs local Dijkstra trees inside each cluster, and connects those clusters through a second-level Dijkstra tree built on cluster hubs.

The project explores scalable routing structures for logistics networks, transport systems, and large game worlds.

---

# Overview

Traditional shortest-path approaches become expensive when applied directly to large complete graphs.

This project reduces the problem into two levels:

1. Local routing within clusters.
2. Global routing between cluster hubs.

The resulting hierarchy forms a transport backbone that can be used for:

* Game logistics
* Settlement supply chains
* Resource distribution
* Procedural transportation networks
* Hierarchical routing research

---

# Pipeline

```text
Points
│
├── Balanced K-Means Clustering
│
├── Cluster 0
│   └── Local Dijkstra Tree
│
├── Cluster 1
│   └── Local Dijkstra Tree
│
├── ...
│
└── Hub Points
    │
    └── Global Dijkstra Tree
```

Each cluster maintains its own routing tree.

Cluster hubs are then connected through a second Dijkstra tree, forming the global transport network.

---

# Algorithm

## 1. Point Generation

Random 2D points are generated:

```python
points.shape == (N, 2)
```

where:

```text
N = total number of points
```

---

## 2. Balanced Clustering

Points are partitioned using constrained K-Means.

Cluster count is chosen as:

```text
cluster_count = round(√N)
```

Cluster sizes are constrained to:

```text
floor(√N) ≤ cluster_size ≤ ceil(√N)
```

This keeps clusters approximately balanced.

For example:

```text
N = 255

cluster_count ≈ 16

cluster_size ≈ 15–16
```

---

## 3. Hub Selection

Each cluster selects a hub node.

A hub is defined as the node minimizing the sum of squared distances to all other nodes in the cluster:

```text
hub = argmin(sum(distance_matrix))
```

The hub acts as the local distribution center.

---

## 4. Local Dijkstra Trees

For every cluster:

1. Construct a complete graph.
2. Compute squared Euclidean distances.
3. Run Dijkstra from the cluster hub.

Distance metric:

```python
metric="sqeuclidean"
```

Squared distances intentionally penalize long connections, producing more structured trees than ordinary Euclidean distance.

Each tree is stored as:

```python
{
    "hub": int,
    "predecessors": ndarray,
    "edges": [
        (parent, child),
        ...
    ]
}
```

---

## 5. Global Dijkstra Tree

All local hubs are collected.

The hub set becomes a second-level graph.

The same process is repeated:

1. Select a global hub.
2. Build a complete graph on hubs.
3. Run Dijkstra.

The resulting tree forms the global routing backbone.

---

# Project Structure

```text
project/
├── main.py
├── tree.py
└── eval.py
```

### main.py

Contains:

* Point generation
* Clustering
* Hub selection
* Dijkstra execution
* Pipeline orchestration

### tree.py

Contains:

* Iterative tree printer

### eval.py

Contains:

* Tree evaluation metrics
* Depth calculations
* Hub-distance calculations

---

# Tree Representation

The hierarchy uses three representations:

## Predecessor Array

```python
[-9999, 0, 1, 1, 2]
```

Returned directly by Dijkstra.

---

## Edge List

```python
[
    (0, 1),
    (1, 2),
    (1, 3),
    (2, 4)
]
```

Used for evaluation and future routing logic.

---

## Printed Tree

```text
0
├── 1
│   ├── 2
│   │   └── 4
│   └── 3
```

Used for debugging and inspection.

---

# Evaluation Metrics

Each local cluster and the global network are evaluated using a collection of structural, routing, and logistics metrics.

---

## Network Metrics

| Metric       | Description                  |
| ------------ | ---------------------------- |
| Total Length | Sum of all tree edge lengths |
| Avg Edge     | Average edge length          |
| Max Edge     | Longest edge in the tree     |

These metrics estimate infrastructure cost and network footprint.

---

## Structural Metrics

| Metric           | Description                                  |
| ---------------- | -------------------------------------------- |
| Avg Depth        | Average node depth                           |
| Max Depth        | Deepest node in the tree                     |
| Leaf Count       | Number of terminal nodes                     |
| Hub Degree       | Number of direct hub children                |
| Branching Factor | Average number of children per internal node |
| Depth Imbalance  | Max Depth / Avg Depth                        |

These metrics describe the overall shape and balance of the routing tree.

---

## Logistics Metrics

| Metric       | Description                         |
| ------------ | ----------------------------------- |
| Avg Hub Dist | Average route distance from the hub |
| Max Hub Dist | Longest route distance from the hub |

Hub distance is measured along tree paths rather than straight-line distance.

These metrics are useful for evaluating distribution efficiency and service coverage.

---

## Routing Metrics

| Metric      | Description                                                             |
| ----------- | ----------------------------------------------------------------------- |
| Diameter    | Longest shortest-path distance within the tree                          |
| Avg Stretch | Average ratio between tree route distance and direct Euclidean distance |
| Max Stretch | Worst-case stretch ratio                                                |

Stretch measures the routing penalty introduced by the tree structure.

A stretch value of:

```text
1.0
```

indicates a perfectly direct route.

Higher values indicate additional travel caused by hierarchical routing.
---

# Example Output

```text
GLOBAL NETWORK

total_length       : 1432.55
avg_edge           : 95.50
max_edge           : 214.32

avg_depth          : 1.94
max_depth          : 4

avg_hub_dist       : 167.28
max_hub_dist       : 418.92

leaf_count         : 9
hub_degree         : 6
branching_factor   : 1.67
depth_imbalance    : 2.06

diameter           : 587.41

avg_stretch        : 1.29
max_stretch        : 2.84
```
---

# Complexity

Let:

```text
N = total points
K = √N clusters
```

Average cluster size:

```text
√N
```

The hierarchy processes:

```text
K local graphs
+
1 hub graph
```

instead of a single monolithic structure.

This significantly improves scalability and makes the approach practical for larger simulations.

---

# Current Limitations

* Uses complete graphs inside clusters.
* Uses complete graph between hubs.
* Clustering quality affects routing quality.
* Not guaranteed to produce globally optimal routes.
* Currently limited to two hierarchy levels.

---

# Future Work

* Edge load analysis
* Traffic simulation
* Resource-flow modelling
* Sparse graph support
* Dynamic node insertion/removal
* Multi-level hierarchies (3+ levels)
* Alternative hub-selection strategies
* Alternative clustering strategies
* Visualization improvements
* Interactive network explorer
* Route query system
* Real game-world integration
* Benchmarking against single-level Dijkstra
* Benchmarking against MST and Steiner-tree approaches
* Large-scale performance evaluation
---

# Requirements

```bash
pip install numpy scipy k-means-constrained
```

---

# Run

```bash
python main.py
```

The number of points can currently be adjusted directly in the source code.

---

# Intended Use Case

This project is primarily a routing and logistics experiment.

Potential applications include:

* Trade route generation
* Resource transport systems
* NPC logistics
* Settlement supply chains
* Procedural infrastructure generation
* Hierarchical pathfinding research
