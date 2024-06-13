import heapq
import networkx as nx

# Prompt the user to enter required details.
print("Enter the number of delivery locations: ")
num_locations = int(input())

# Created a graph to represent the delivery locations and their connections.
graph = nx.Graph()

# Add nodes to the graph for each delivery location.
for i in range(num_locations):
    graph.add_node(i)

# Add edges to the graph for the connections between delivery locations.
for i in range(num_locations):
    for j in range(i + 1, num_locations):
        dist = int(input("Enter the distance between location {} and location {}: ".format(i, j)))
        graph.add_edge(i, j, weight=dist)

# Visualize the graph showing the locations user entered.
nx.draw(graph, with_labels=True)

# Display the shortest path (based on parameters like traffic, order number, restaurant number).
# Create a min-heap to store the delivery locations yet to be visited.
min_heap = []

# Initialize the min-heap with the start location.
heapq.heappush(min_heap, (0, 0))

# While the min-heap is not empty, do the following:
while min_heap:

    # Pop the top element from the min-heap and get the current location.
    (cost, current_location) = heapq.heappop(min_heap)

    # If the current location is the destination, then stop.
    if current_location == num_locations - 1:
        break

    # For each neighbor of the current location, do the following:
    for neighbor in graph.neighbors(current_location):

        # Calculate the new cost of the path from the start location to the neighbor.
        new_cost = cost + float(graph.get_edge_data(current_location, neighbor)['weight'])

        # If the min-heap is empty, push the new cost and neighbor to the heap.
        if not min_heap:
            heapq.heappush(min_heap, (new_cost, neighbor))
        else:
            # If the new cost is less than the cost of the path from the start location to the neighbor in the min-heap, then update the min-heap.
            if new_cost < min_heap[0][0]:
                heapq.heappush(min_heap, (new_cost, neighbor))

# Print the shortest path.
path = []
current_location = num_locations - 1
while current_location != 0:
    path.append(current_location)
    current_location = min_heap[0][1]

print("The shortest path is: ")
for location in path[::-1]:
    print(location + 1)

# Display the next delivery location.
next_location = min_heap[0][1]
print("The next delivery location is:", next_location + 1)
