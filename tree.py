from collections import defaultdict


def print_tree(predecessors, root_node):

    children = defaultdict(list)

    for child, parent in enumerate(predecessors):
        if parent >= 0:
            children[parent].append(child)

    stack = [(root_node, "", True)]

    while stack:

        node, prefix, is_last = stack.pop()

        if prefix:
            connector = "└── " if is_last else "├── "
            print(prefix + connector + str(node))
        else:
            print("   ", node)

        child_nodes = sorted(children[node])

        for index in range(
            len(child_nodes) - 1,
            -1,
            -1
        ):

            child = child_nodes[index]

            is_child_last = (
                index == len(child_nodes) - 1
            )

            child_prefix = prefix + (
                "    " if is_last else "│   "
            )

            stack.append(
                (
                    child,
                    child_prefix,
                    is_child_last
                )
            )
