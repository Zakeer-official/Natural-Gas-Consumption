import datetime
from turtle import *
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, company_id):
        self.company_id = company_id
        self.products = []

    def add_product(self, product):
        self.products.append(product)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.user_products = {}
        self.locations = {}
        self.graph = nx.Graph()

    def add_node(self, company_id):
        if company_id not in self.nodes:
            self.nodes[company_id] = Node(company_id)
            self.edges[company_id] = []

    def add_edge_pro(self, node1, node2):           #for product connection with user and company
        if node1 in self.nodes and node2 in self.nodes:
            self.edges[node1].append(node2)
            self.edges[node2].append(node1)
        
    def add_edge(self,source,destination,distance):  #for delivery location connection
        if source in self.locations and destination in self.locations:
            self.locations[source].append((destination, distance))
            self.locations[destination].append((source, distance))
            self.graph.add_edge(source, destination, weight=distance)
        
    def add_location(self, location):
        self.locations[location] = []

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

    def get_connections(self, p):
        if p in self.nodes:
            return self.edges[p]
        return self.edges

    def add_product_to_node(self, company_id, product):
        if company_id in self.nodes:
            node = self.nodes[company_id]
            node.add_product(product)
        
    def get_products_by_node(self, company_id):
        if company_id in self.nodes:
            node = self.nodes[company_id]
            return node.products
        return []

    def get_all_nodes(self):
        return list(self.nodes.keys())

    def add_user_product(self, user_id, product):
        if user_id in self.user_products:
            self.user_products[user_id].append(product)
        else:
            self.user_products[user_id] = [product]

    def get_user_products(self, user_id):
        if user_id in self.user_products:
            return self.user_products[user_id]
        return []
        
    def get_companies_by_user(self, user_id):
        companies = []
        for company_id in self.nodes:
            products = self.get_products_by_node(company_id)
            for product in products:
                if product['user_id'] == user_id:
                    companies.append(company_id)
        return companies

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
    
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, priority, item):
        self.queue.append((priority, item))

    def pop(self):
        if not self.is_empty():
            min_index = 0
            for i in range(1, len(self.queue)):
                if self.queue[i][0] < self.queue[min_index][0]:
                    min_index = i
            return self.queue.pop(min_index)[1]

    def is_empty(self):
        return len(self.queue) == 0

def validate_date(date_str):
    try:
        order_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        current_date = datetime.datetime.now().date()
        if order_date.date() <= current_date:
            return True
        else:
            print("Order date should be in the past.")
            return False
    except ValueError:
        return False

def add_product(user):
    r = {}
    print("   ")
    print("=== Add Product Details ===")
    name = input("Enter the product name: ")
    date = input("Enter the date of order (YYYY-MM-DD): ")
    priority_queue = PriorityQueue()
    priority_queue.push(0, date)  # Push the date into the priority queue
    while not priority_queue.is_empty():
        date = priority_queue.pop()
        if validate_date(date):
            break
        else:
            print("Invalid date format. Please enter a valid date in YYYY-MM-DD format.")
            date = input("Enter the date of order (YYYY-MM-DD): ")
            priority_queue.push(0, date)  # Push the new date into the priority queue
    try:
        company_id = int(input("Enter the company ID: "))
        product = {'name': name, 'date': date, 'user_id': user} #add user id to the product
        r[user]=product
        graph.add_node(company_id)
        graph.add_product_to_node(company_id, product)
        graph.add_user_product(user, product)  # Store the product for the user
        print("Product details added successfully.")
    except ValueError:
        print("Invalid company ID. Please enter a valid integer.")

def check_delivery_status():
    print("=== Delivery Status ===")
    priority_queue = PriorityQueue()
    for company_id in graph.get_all_nodes():
        products = graph.get_products_by_node(company_id)
        if products:
            order_date = datetime.datetime.strptime(products[0]['date'], "%Y-%m-%d").date()
            current_date = datetime.datetime.now().date()
            days_difference = (current_date - order_date).days
            delivery_status = ''

            if days_difference < 3:
                delivery_status = 'In-transit'
            elif 3 <= days_difference <= 5:
                delivery_status = 'Out of delivery'
            else:
                delivery_status = 'Delivered'

            print(f"Delivery status for Company {company_id}:")
            print(f"Number of products: {len(products)}")
            for product in products:
                print(f"Delivery status {product['name']} from Company {company_id} ordered on {product['date']} - {delivery_status}")
        else:
            print(f"No products found for Company {company_id}")
    else:
        print("No deliveries beyond this!")

def get_products_by_company():
    print("=== Get Products by Company ===")
    company_id = int(input("Enter the company ID: "))
    products = graph.get_products_by_node(company_id)
    if products:
        print(f"Products for Company {company_id}:")
        print(f"Number of products: {len(products)}")
        for product in products:
            print(f"Product Name: {product['name']}, Order Date: {product['date']}")
    else:
        print(f"No products found for Company {company_id}")

def calculate_average_delivery_time():
    print("=== Calculate Average Delivery Time ===")
    total_delivery_time = 0
    count = 0
    for company_id in graph.get_all_nodes():
        products = graph.get_products_by_node(company_id)
        if products:
            for product in products:
                order_date = datetime.datetime.strptime(product['date'], "%Y-%m-%d").date()
                current_date = datetime.datetime.now().date()
                days_difference = (current_date - order_date).days
                total_delivery_time += days_difference
                count += 1
    if count > 0:
        average_delivery_time = total_delivery_time / count
        print(f"The average delivery time for {count} products is: {average_delivery_time:.2f} days")
    else:
        print("No products found.")

def search_product_by_name():
    print("=== Search Product by Name ===")
    product_name = input("Enter the product name to search: ")
    found = False
    for company_id in graph.get_all_nodes():
        products = graph.get_products_by_node(company_id)
        for product in products:
            if product['name'] == product_name:
                print(f"Product found in Company {company_id}:")
                print(f"Product Name: {product['name']}, Order Date: {product['date']}")
                found = True
    if not found:
        print(f"No products found with the name '{product_name}'.")

def get_companies_by_user():
    print("=== Get Companies by User ===")
    user_id = input("Enter the user name : ")
    companies = graph.get_companies_by_user(user_id)
    if companies:
        print(f"Companies with User {user_id}:")
        for company_id in companies:
            print(f"Company ID: {company_id}")
    else:
        print(f"No companies found for User {user_id}")

def main():
    n = int(input("No. of Users: "))
    names = []
    for i in range(n):
        names.append(input(f"Username {i+1} : " ))
        
    while True:
        print("   ")
        print("============     *** Product Management Menu ***    ============")
        print("1. Add Product Details")
        print("2. Delivery Services")
        print("3. Check Delivery Status")
        print("4. Get Products by Company")
        print("5. Calculate Average Delivery Time")
        print("6. Get product names by user")
        print("7. Search Product by Name")
        print("8. Get Companies by users")
        print("9. Show Company IDs")
        print("10. Show the Companies using edges connected with users")
        print("11. Exit")
        choice = input("Enter your choice (1-11): ")
        if choice == '1':
            for user in names:
                add_product(user)
        elif choice == '2':
            while True:
                print("1. Add Location")
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
        elif choice == '3':
            check_delivery_status()
        elif choice == '4':
            get_products_by_company()
        elif choice == '5':
            calculate_average_delivery_time()
        elif choice == '6':
            for i in names:
                user = i
                products = graph.get_user_products(user)
                print(f"Products for user {user}:")
                print(f"Number of products: {len(products)}")
                for product in products:
                    print(f"Product Name: {product['name']}, Order Date: {product['date']}")
        elif choice == '7':
            search_product_by_name()
        elif choice == '8':
            get_companies_by_user()
        elif choice == '9':
            x = graph.get_all_nodes()
            print(x)
        elif choice == '10':
            x = graph.get_all_nodes()
            for i in range(n):
                for j in x:
                    graph.add_edge_pro(i, j)
                connections = graph.get_connections(i)
                # Print the connected companies
                print(f"User {names[i]} is connected to the following companies:")
                print(connections)
                # for k in connections:
                #     print(k)
        elif choice == '11':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    graph = Graph()
    delivery_service = DeliveryService()
    main()


# Set up the turtle screen
screen = turtle.Screen()
screen.setup(1200, 600)

# Create the turtle objects
t1 = turtle.Turtle()
t2 = turtle.Turtle()
t1.speed(20)
t2.speed(20)

# Define colors for the circles
circle_colors = ['red', 'blue']

# Draw the central circle for the first output
radius = 50
t1.penup()
t1.goto(-300, -radius)
t1.pendown()
t1.color(circle_colors[0])
t1.begin_fill()
t1.circle(radius)
t1.end_fill()

# Draw the outer circles and connecting lines for the first output
num_shapes = 7
angle = 360 / num_shapes

for i in range(num_shapes):
    t1.penup()
    t1.goto(-320, 0)
    t1.pendown()
    t1.setheading(i * angle)
    t1.forward(radius * 2)

    # Draw the square for the first output
    t1.color(circle_colors[1])
    t1.begin_fill()
    for _ in range(4):
        t1.forward(radius)
        t1.right(90)
    t1.end_fill()

# Draw the central circle for the second output
t2.penup()
t2.goto(200, 0)
t2.pendown()
t2.color(circle_colors[0])
t2.begin_fill()
t2.circle(radius)
t2.end_fill()

# Connect the second output circle with adjacent two blue squares in the first output
for i in range(2):
    # Connect each side of the second output circle with the corresponding blue square
    t2.penup()
    t2.goto(175, 0)
    t2.pendown()
    t2.setheading((i+0.25) * angle)
    t2.color('red')
    t2.pensize(5)
    t2.forward(radius)
    t2.goto(-259 + radius, 0 + (radius * 2 * i))

# Hide the turtle cursors
t1.hideturtle()
t2.hideturtle()

# Close the turtle graphics window
turtle.done()
