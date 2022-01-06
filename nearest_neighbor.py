import math, sys, tsp, random
import matplotlib.pyplot as plt

def nearest_neighbor(x_coordinates, y_coordinates, s, u):
    # Get coordinates of u-node
    x = x_coordinates[u]
    y = y_coordinates[u]

    # Set state of u-node to "closed"
    s[u] = "C"

    # Initialize nearest distance
    nearest_distance = float("inf")

    # Initialize index of nearest neighbor
    nearest_neighbor = - 1

    # Browse all nodes
    for i in range(len(y_coordinates)):
        # If node is closed, move to next iteration
        if s[i] == "C":
            continue

        # Get coordinates of the node
        x2 = x_coordinates[i]
        y2 = y_coordinates[i]

        # Calculate distance between nodes
        dist = math.sqrt((x-x2)**2 + (y-y2)**2)

        # Evaluate the distance between nodes
        if dist < nearest_distance:
            nearest_distance = dist
            nearest_neighbor = i

    # If initial value of nearest distance hasn't changed  
    if nearest_distance == float("inf"):
        nearest_distance = 0

    return nearest_neighbor, nearest_distance, s

def travel_of_salesman(x_coordinates, y_coordinates):
    # Initialize starting node
    u = random.randint(0, len(x_coordinates) - 1)

    # Initialize state of nodes as "new"
    s = ["N"] * (len(x_coordinates)+1)

    # Initialize w-distance of start u-node node 
    w = 0

    # Lists of coordinates representing path
    x_coords = []
    y_coords = []

    # Repeat until node index equals -1
    while u != -1:
        # Add coordinates to path
        x_coords.append(x_coordinates[u])
        y_coords.append(y_coordinates[u])

        # Get nearest neighbor and w-distance
        u, dist, s = nearest_neighbor(x_coordinates, y_coordinates, s, u)

        # Increase total w-distance
        w += dist

    # Complete the Hamilton circle by adding first node of the path to its end    
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])
    w += math.sqrt((x_coords[len(x_coords) - 1] - x_coords[len(x_coords) - 2])**2 + (y_coords[len(x_coords) - 1] - y_coords[len(x_coords) - 2])**2)

    return w, x_coords, y_coords


# Extract coordinates from shapefile
x_coordinates, y_coordinates = tsp.extract_coordinates(sys.argv[1])

# Change node coordinates to first quadrant of new coordinate system and change units to kilometres
x_coordinates = tsp.transform_coordinates(x_coordinates, 1000)
y_coordinates = tsp.transform_coordinates(y_coordinates, 1000)

# Nearest neighbor algorithm
w, x_coords, y_coords = travel_of_salesman(x_coordinates, y_coordinates)

# Visualize algorithm results    
tsp.graph_visualization(x_coordinates, y_coordinates, x_coords, y_coords)

print("Path length w is: {} km".format(w))