# Train Delivery System - BigPay Technical Assessment

First and foremost, I would like to express my sincere gratitude to BigPay for shortlisting me as a candidate for the Backend Developer position. I am excited about the opportunity to potentially join your innovative team.

## Project Overview
This project implements an optimized train delivery system that manages the transportation of packages between different stations through a railway network. The system calculates efficient routes for trains to pick up and deliver packages while considering various constraints like train capacity and journey times.

## Features
- Graph-based railway network representation
- Multiple trains with different capacities
- Package delivery optimization
- Support for both direct and indirect (multi-hop) deliveries
- Real-time tracking of package locations and train movements

## Technical Implementation
The system is built using Python and implements the following key components:

### Core Classes
- `Node`: Represents railway stations
- `Edge`: Represents connections between stations
- `Train`: Manages train properties and current location
- `Package`: Handles package details and tracking
- `DeliverySystem`: Main system orchestrator

### Key Functionalities
- Bidirectional railway connections
- Package pickup and delivery scheduling
- Optimal route calculation
- Time-based movement tracking

## How to Use

### Input Format
The system accepts input in the following format:

1. Number of stations followed by station names
2. Number of edges followed by edge details (Name,Node1,Node2,JourneyTime)
3. Number of packages followed by package details (Name,Weight,StartNode,DestNode)
4. Number of trains followed by train details (Name,Capacity,StartNode)

Example:

Enter number of stations: 3
Enter station name: A
Enter station name: B
Enter station name: C
Enter number of edges: 2
Enter edge (Name,Node1,Node2,JourneyTime): E1,A,B,30
Enter edge (Name,Node1,Node2,JourneyTime): E2,B,C,10
Enter number of packages: 1
Enter package (Name,Weight,StartNode,DestNode): K1,5,A,C
Enter number of trains: 1
Enter train (Name,Capacity,StartNode): Q1,6,A

### Output Format
W=<time>, T=<train_name>, N1=<start_node>, P1=<pickup_packages>, N2=<end_node>, P2=<dropoff_packages>

Example:
W=0, T=Q1, N1=B, P1=[], N2=A, P2=[]
W=30, T=Q1, N1=A, P1=[K1], N2=B, P2=[]
W=60, T=Q1, N1=B, P1=[], N2=C, P2=[K1]


## Algorithm
The system uses a greedy approach to solve the delivery problem:
1. Identifies available packages at current train location
2. Determines optimal route (direct or via intermediate stations)
3. Executes movements while tracking time and updating positions
4. Continues until all packages are delivered or no further moves are possible

## Installation
1. Clone the repository
2. Ensure Python is installed
3. No additional dependencies required

## Running the Program
1. Run this command in the terminal:
```python bigpay.py```
2. Follow the prompts to input the required data
3. The program will output the optimal delivery schedule

## License
This project is created as part of BigPay's technical assessment process.

---
Thank you again to BigPay for this opportunity. I look forward to discussing this implementation and potential improvements during our technical discussion. If you have any questions or need further clarification, please don't hesitate to reach out.
