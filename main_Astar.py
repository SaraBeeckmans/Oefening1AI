import sys
import heapq

# TODO: Check out https://www.youtube.com/watch?v=6TsL96NAZCo

class Node:
    def append_edge(self, edge):
        self.edges.append(edge)
        edge.parentNode = self

    def __init__(self, name, heuristic_value=0):
        self.edges = []
        self.name = name
        self.path_cost = int(0)
        # self.visited = False
        self.heuristic_value = int(heuristic_value)


class Edge:
    def __init__(self, ltarget_node, lcost):
        self.cost = int(lcost)
        self.target_node = ltarget_node
        self.parentNode = None


def search_path(start_node=None, goal_node=None):

    queue = [(start_node.heuristic_value, 0, start_node, [])]    # Priority queue filled with tuple containing (weight, path_cost, node, path)
    seen = {}
    paths_to_goal = {}

    # While the queue isn't empty
    while queue:
        # Pop the cost, node, path from the queue
        cost, path_cost, node, path = heapq.heappop(queue)

        if node.name in seen and seen[node.name] < cost:
            continue  # returns control to beginning of while loop

        path.append(node)

        if node == goal_node:
            paths_to_goal[cost] = path
            continue  # returns control to beginning of while loop

        for edge in node.edges:
            if edge.target_node != node:    # Reference to parent are ignored.
                target_path_cost = path_cost + edge.cost
                target_cost = target_path_cost + edge.target_node.heuristic_value
                if edge.target_node.name not in seen:
                    heapq.heappush(queue, (target_cost, target_path_cost, edge.target_node, path))

        seen[node.name] = cost

    # TODO: paths_to_goal -> sort on score. Return only lowest path
    return paths_to_goal


def main():

    all_nodes = {}

    file_object = open(sys.argv[1], "r", encoding='utf8')
    try:
        start_ln = file_object.readline()

        goal_ln = file_object.readline()

        line = file_object.readline()
        while line:

            line_split = line.split(":")
            node_and_heuristic = line_split[0].strip()
            [node_name, heuristic_value] = node_and_heuristic.split(' ')

            if node_name not in all_nodes:
                parent_node = Node(node_name, heuristic_value)
                all_nodes[node_name] = parent_node
            else:
                parent_node = all_nodes[node_name]
                parent_node.heuristic_value = int(heuristic_value)

            target_edges = line_split[1].strip()
            target_edges_split = target_edges.split(' ')

            for i in range(int(len(target_edges_split)/2)):
                target_node_name = target_edges_split[i*2]
                cost = target_edges_split[i*2+1]

                if target_node_name not in all_nodes:
                    target_node = Node(target_node_name)
                    all_nodes[target_node_name] = target_node
                else:
                    target_node = all_nodes[target_node_name]

                edge = Edge(target_node, cost)
                parent_node.append_edge(edge)

            line = file_object.readline()

    finally:
        file_object.close()

    start_ln = start_ln.replace('\n', '')
    start_node = all_nodes[start_ln]
    goal_node = all_nodes[goal_ln.rstrip('\n')]

    paths = search_path(start_node, goal_node)
    # TODO: Print path as stated in exercise
    print(paths)


if __name__ == '__main__':
    main()
