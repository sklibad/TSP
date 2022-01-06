import math, sys, tsp, random

def best_insertion(x_coordinates, y_coordinates):
    # Initialize path
    path = []

    # Initialize Hamilton circle
    nodes = list(range(len(x_coordinates) - 1))
    for i in range(3):
        u = random.choice(nodes)
        nodes.remove(u)
        path.append(u)
    path.append(path[0])

    # Initialize w-distance
    w = 0

    # Calculate w-distance of initial Hamilton circle
    for k in range(3):
        w_k = math.sqrt((x_coordinates[path[k]] - x_coordinates[path[k + 1]])**2 + (y_coordinates[path[k]] - y_coordinates[path[k + 1]])**2)
        w += w_k
    
    # Set random order of nodes
    random.shuffle(nodes)

    # For each u-node, that's not in initial Hamilton circle
    for u in nodes:
        # Get coordinates of the node
        x_u = x_coordinates[u]
        y_u = y_coordinates[u]

        # Calculate dw(s,u)-distance of triangle inequality
        w1 = math.sqrt((x_coordinates[path[0]] - x_u)**2 + (y_coordinates[path[0]] - y_u)**2)

        # Inicialization of updated w-distance after adding next node to the path 
        new_w = float("inf")

        # Inicialization of index to assign next node to the path
        insert_index = -1

        # s-node of triangle inequality
        s = path[0]

        # For v-node of triangle inequality
        for v in range(1,len(path)):
            # Get coordinates of the node
            x_v = x_coordinates[path[v]]
            y_v = y_coordinates[path[v]]

            # Calculate dw(u,v)-distance of triangle inequality
            w2 = math.sqrt((x_v - x_u)**2 + (y_v - y_u)**2)

            # Calculate dw(s,v)-distance of triangle inequality
            edge_w = math.sqrt((x_v - x_coordinates[s])**2 + (y_v - y_coordinates[s])**2)

            # Calculate new w-distance using relaxation
            potencial_w = w + w1 + w2 - edge_w
            if potencial_w < new_w:
                new_w = potencial_w
                insert_index = v

            # dw(s,u)-distance = dw(u,v)-distance     
            w1 = w2

            # s-node = v_node
            s = path[v]

        # Insert u-node to the path    
        path.insert(insert_index, u)

        # Update w-distance
        w = new_w

    # Lists of coordinates representing path
    x_coords = []
    y_coords = []

    # Browse nodes in path
    for u in path:
        # Add coordinates of node to lists
        x_coords.append(x_coordinates[u])
        y_coords.append(y_coordinates[u])

    return w, x_coords, y_coords


# Extract coordinates from shapefile
x_coordinates, y_coordinates = tsp.extract_coordinates(sys.argv[1])

# Change node coordinates to first quadrant of new coordinate system and change units to kilometres
x_coordinates = tsp.transform_coordinates(x_coordinates, 1000)
y_coordinates = tsp.transform_coordinates(y_coordinates, 1000)

# Best insertion algorithm
w, x_coords, y_coords = best_insertion(x_coordinates, y_coordinates)

# Visualize algorithm results
tsp.graph_visualization(x_coordinates, y_coordinates, x_coords, y_coords)

print("Path length w is: {} km".format(w))