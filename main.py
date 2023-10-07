import heapq
import csv
from tkinter import filedialog


def read_in_graph_data():
    file = filedialog.askopenfile()
    reader = csv.reader(file, delimiter=',')
    return [(row[0], row[1], float(row[2])) for row in reader]


def construct_node_to_net_flow_dict(data):
    # Create and populate a dictionary of node to 'net flow'
    # Net flow: (sum of the weights of all incoming edges minus the sum of weights of all outgoing edges)
    # For every edge there will be one node that loses 'flow' and one that gains 'flow'
    node_to_net_flow = {}
    for edge in data:
        # Calculate outgoing edge
        if edge[0] in node_to_net_flow:
            node_to_net_flow[edge[0]] -= edge[2]
        else:
            node_to_net_flow[edge[0]] = -edge[2]

        # Calculate incoming edge
        if edge[1] in node_to_net_flow:
            node_to_net_flow[edge[1]] += edge[2]
        else:
            node_to_net_flow[edge[1]] = edge[2]
    return node_to_net_flow


def construct_negative_and_positive_flow_heaps(node_to_net_flow_dict):
    # Partition node into nodes that have negative ('owe') and positive (are 'owed') flow
    negative_flow_heap = []
    positive_flow_heap = []
    for key, value in node_to_net_flow_dict.items():
        if value < 0:
            heapq.heappush(negative_flow_heap, (value, key))
        elif value > 0:
            # Flip the sign of value to make min heap act like a max heap
            heapq.heappush(positive_flow_heap, (-value, key))
    return negative_flow_heap, positive_flow_heap


def construct_min_flow_graph(negative_flow_heap, positive_flow_heap):
    # Loop while until both heaps are empty
    min_flow_graph = []
    while len(negative_flow_heap) > 0 and len(positive_flow_heap) > 0:
        # Get the nodes with the greatest positive and negative flows
        max_negative_flow_node = negative_flow_heap.pop()
        max_positive_flow_node = positive_flow_heap.pop()

        transfer_amount = max(max_negative_flow_node[0], max_positive_flow_node[0])

        # Append the edge in our new min flow graph
        min_flow_graph.append((max_negative_flow_node[1], max_positive_flow_node[1], transfer_amount * -1))

        # We may have leftovers, create new nodes for these
        new_negative_flow_node = (max_negative_flow_node[0] - transfer_amount, max_negative_flow_node[1])
        new_positive_flow_node = (max_positive_flow_node[0] - transfer_amount, max_positive_flow_node[1])

        # If there are leftovers append the nodes to their respective heap
        if new_negative_flow_node[0] < 0:
            heapq.heappush(negative_flow_heap, new_negative_flow_node)

        if new_positive_flow_node[0] < 0:
            heapq.heappush(positive_flow_heap, new_positive_flow_node)
    return min_flow_graph


def main():
    # Prompt user to select csv and read it into reader
    data = read_in_graph_data()

    # Construct a dictionary of node to 'net flow'
    node_to_net_flow_dict = construct_node_to_net_flow_dict(data)

    # Partition nodes into two heaps, negative flow heap and positive flow heap
    negative_flow_heap, positive_flow_heap = construct_negative_and_positive_flow_heaps(node_to_net_flow_dict)

    # Construct our min flow graph
    min_flow_graph = construct_min_flow_graph(negative_flow_heap, positive_flow_heap)

    # For now print edges of min flow graph to console
    for edge in min_flow_graph:
        print(edge[0], "owes", edge[1], "a value of", edge[2])


if __name__ == "__main__":
    main()
