import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.locations = {}
        self.graph = nx.Graph()

    def add_location(self, location):
        self.locations[location] = []

    def add_edge(self, source, destination, distance):
        if source in self.locations and destination in self.locations:
            self.locations[source].append((destination, distance))
            self.locations[destination].append((source, distance))
            self.graph.add_edge(source, destination, weight=distance)

    def visualize_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color='lightblue', edge_color='gray')
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.show()

    def get_shortest_path(self, start_location, end_location):
        path = nx.shortest_path(self.graph, start_location, end_location, weight='weight')
        return path

    def get_next_delivery_location(self, current_location):
        heap = []
        for location in self.locations:
            if location != current_location:
                heapq.heappush(heap, (float('inf'), location))
        heapq.heappush(heap, (0, current_location))

        while heap:
            cost, location = heapq.heappop(heap)
            if cost == float('inf'):
                break
            if location != current_location:
                return location

            for neighbor, edge_distance in self.locations[location]:
                new_cost = cost + edge_distance
                for i in range(len(heap)):
                    if heap[i][1] == neighbor:
                        if new_cost < heap[i][0]:
                            heap[i] = (new_cost, neighbor)
                            heapq.heapify(heap)
                        break

        return None


class DeliveryService:
    def __init__(self):
        self.graph = Graph()

    def add_location(self):
        location = input("Enter location: ")
        self.graph.add_location(location)

    def add_edge(self):
        source = input("Enter source location: ")
        destination = input("Enter destination location: ")
        distance = float(input("Enter distance: "))
        self.graph.add_edge(source, destination, distance)

    def visualize_graph(self):
        self.graph.visualize_graph()

    def get_shortest_delivery_path(self):
        start_location = input("Enter start location: ")
        end_location = input("Enter end location: ")
        shortest_path = self.graph.get_shortest_path(start_location, end_location)
        return shortest_path

    def get_next_delivery_location(self):
        current_location = input("Enter current location: ")
        next_location = self.graph.get_next_delivery_location(current_location)
        return next_location


# usage
delivery_service = DeliveryService()

while True:
    print("\n1. Add Location")
    print("2. Add Edge")
    print("3. Visualize Graph")
    print("4. Get Shortest Delivery Path")
    print("5. Get Next Delivery Location")
    print("6. Exit")

    choice = int(input("\nEnter your choice: "))

    if choice == 1:
        delivery_service.add_location()
    elif choice == 2:
        delivery_service.add_edge()
    elif choice == 3:
        delivery_service.visualize_graph()
    elif choice == 4:
        shortest_delivery_path = delivery_service.get_shortest_delivery_path()
        print("Shortest Delivery Path:", shortest_delivery_path)
    elif choice == 5:
        next_delivery_location = delivery_service.get_next_delivery_location()
        print("Next Delivery Location:", next_delivery_location)
    elif choice == 6:
        break
    else:
        print("Invalid choice. Please try again.")
