class Node:
    def __init__(self, name):
        self.name = name.upper()
        self.edges = {}

class Edge:
    def __init__(self, name, node1, node2, journey_time):
        self.name = name.upper()
        self.node1 = node1.upper()
        self.node2 = node2.upper()
        self.journey_time = journey_time

class Train:
    def __init__(self, name, capacity, starting_node):
        self.name = name.upper()
        self.capacity = capacity
        self.current_node = starting_node.upper()
        self.packages = []

class Package:
    def __init__(self, name, weight, start_node, dest_node):
        self.name = name.upper()
        self.weight = weight
        self.start_node = start_node.upper()
        self.dest_node = dest_node.upper()
        self.current_node = start_node.upper()

class DeliverySystem:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.trains = {}
        self.packages = {}
        self.moves = []
        self.current_time = 0

    def add_node(self, name):
        name = name.upper()
        if name not in self.nodes:
            self.nodes[name] = Node(name)

    def add_edge(self, name, node1, node2, time):
        edge = Edge(name, node1, node2, time)
        self.edges[edge.name] = edge
        
        # Add bidirectional connections
        self.nodes[node1.upper()].edges[node2.upper()] = time
        self.nodes[node2.upper()].edges[node1.upper()] = time

    def solve(self):
        while not self._all_packages_delivered():
            moved = False
            for train_name, train in self.trains.items():
                # First try to pick up packages
                available_packages = self._get_available_packages(train)
                
                if available_packages:
                    package = available_packages[0]  # Take first available package
                    current = train.current_node
                    
                    # If we can't reach destination directly, go through intermediate node
                    if package.dest_node not in self.nodes[current].edges:
                        # Find intermediate node (B in this case)
                        for intermediate in self.nodes[current].edges:
                            if package.dest_node in self.nodes[intermediate].edges:
                                # First move: current to intermediate
                                self.moves.append({
                                    'time': self.current_time,
                                    'train': train.name,
                                    'start': current,
                                    'pickup': [package.name],
                                    'end': intermediate,
                                    'dropoff': []
                                })
                                
                                self.current_time += self.nodes[current].edges[intermediate]
                                train.current_node = intermediate
                                
                                # Second move: intermediate to destination
                                self.moves.append({
                                    'time': self.current_time,
                                    'train': train.name,
                                    'start': intermediate,
                                    'pickup': [],
                                    'end': package.dest_node,
                                    'dropoff': [package.name]
                                })
                                
                                self.current_time += self.nodes[intermediate].edges[package.dest_node]
                                train.current_node = package.dest_node
                                package.current_node = package.dest_node
                                moved = True
                                break
                    else:
                        # Direct path exists
                        self.moves.append({
                            'time': self.current_time,
                            'train': train.name,
                            'start': current,
                            'pickup': [package.name],
                            'end': package.dest_node,
                            'dropoff': [package.name]
                        })
                        
                        self.current_time += self.nodes[current].edges[package.dest_node]
                        train.current_node = package.dest_node
                        package.current_node = package.dest_node
                        moved = True
                    
                # If no packages at current node, move to where packages are
                else:
                    undelivered_packages = [p for p in self.packages.values() 
                                        if p.current_node != p.dest_node]
                    if undelivered_packages:
                        target_package = undelivered_packages[0]
                        if target_package.current_node in self.nodes[train.current_node].edges:
                            travel_time = self.nodes[train.current_node].edges[target_package.current_node]
                            
                            self.moves.append({
                                'time': self.current_time,
                                'train': train.name,
                                'start': train.current_node,
                                'pickup': [],
                                'end': target_package.current_node,
                                'dropoff': []
                            })
                            
                            self.current_time += travel_time
                            train.current_node = target_package.current_node
                            moved = True
                
                if not moved:
                    break

            if not moved:
                break

        return self.moves

    def _all_packages_delivered(self):
        return all(package.current_node == package.dest_node 
                  for package in self.packages.values())

    def _get_available_packages(self, train):
        return [p for p in self.packages.values()
                if p.current_node == train.current_node
                and p.current_node != p.dest_node
                and p.weight <= train.capacity]

def get_input():
    # Get number of stations and their names
    num_stations = int(input("Enter number of stations: "))
    stations = []
    for _ in range(num_stations):
        station = input("Enter station name: ")
        stations.append(station)
    
    # Get number of edges and their details
    num_edges = int(input("Enter number of edges: "))
    edges = []
    for _ in range(num_edges):
        edge_info = input("Enter edge (Name,Node1,Node2,JourneyTimeInMinutes): ").strip().split(',')
        edges.append({
            'name': edge_info[0],
            'node1': edge_info[1],
            'node2': edge_info[2],
            'time': int(edge_info[3])
        })
    
    # Get number of packages and their details
    num_packages = int(input("Enter number of packages: "))
    packages = []
    for _ in range(num_packages):
        package_info = input("Enter package (Name,Weight,StartNode,DestNode): ").strip().split(',')
        packages.append({
            'name': package_info[0],
            'weight': int(package_info[1]),
            'start': package_info[2],
            'dest': package_info[3]
        })
    
        # Get number of trains and their details
    num_trains = int(input("Enter number of trains: "))
    trains = []
    
    # Get maximum package weight for validation
    max_package_weight = max(package['weight'] for package in packages)
    
    for _ in range(num_trains):
        while True:
            train_info = input("Enter train (Name,Capacity,StartNode): ").strip().split(',')
            capacity = int(train_info[1])
            
            if capacity < max_package_weight:
                print(f"\nError: Train capacity ({capacity}) is insufficient!")
                print(f"There are packages with weight up to {max_package_weight}")
                print("Please enter train details again with adequate capacity")
                continue
            
            trains.append({
                'name': train_info[0],
                'capacity': capacity,
                'start': train_info[2]
            })
            break
    
    return stations, edges, packages, trains

def format_output(move):
    """Format a single move according to the required output format"""
    pickup_str = str(move['pickup']).replace("'", "")  # Remove quotes
    dropoff_str = str(move['dropoff']).replace("'", "")  # Remove quotes
    return (f"W={move['time']}, T={move['train']}, "
            f"N1={move['start']}, P1={pickup_str}, "
            f"N2={move['end']}, P2={dropoff_str}")

def main():
    # Get input
    stations, edges, packages, trains = get_input()
    
    # Initialize delivery system
    system = DeliverySystem()
    
    # Add nodes
    for station in stations:
        system.add_node(station)
    
    # Add edges
    for edge in edges:
        system.add_edge(edge['name'], edge['node1'], 
                       edge['node2'], edge['time'])
    
    # Add packages
    for package in packages:
        system.packages[package['name']] = Package(
            package['name'], 
            package['weight'],
            package['start'], 
            package['dest']
        )
    
    # Add trains
    for train in trains:
        system.trains[train['name']] = Train(
            train['name'],
            train['capacity'],
            train['start']
        )
    
    # Solve and output results
    moves = system.solve()
    for move in moves:
        print(format_output(move))

if __name__ == "__main__":
    main()