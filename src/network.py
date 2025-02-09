import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import math
import random

def execute():
    # Load the data
    data = pd.read_csv('data/networks_assignment.to_csv')

    # Define the nodes and their colors
    blue_nodes = ['D', 'F', 'I', 'N', 'S']
    green_nodes = ['BIH', 'GEO', 'ISR', 'MNE', 'SRB', 'CHE', 'TUR', 'UKR', 'GBR', 'AUS', 'HKG']
    yellow_nodes = ['AUT', 'BEL', 'BGR', 'HRV', 'CZE', 'EST', 'FRA', 'DEU', 'GRC', 'HUN', 'IRL', 'ITA', 'LVA', 'LUX', 'NLD', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP']

    # Create the graph
    G = nx.Graph()

    # Add nodes with their colors
    for node in blue_nodes:
        G.add_node(node, color='teal')
    for node in green_nodes:
        G.add_node(node, color='green')
    for node in yellow_nodes:
        G.add_node(node, color='yellow')

    # Add edges based on the CSV data
    for _, row in data.iterrows():
        label = row['LABELS']
        for other_node in blue_nodes + green_nodes + yellow_nodes:
            if row[other_node] > 0:
                G.add_edge(label, other_node)

    # Position the nodes
    pos = {}

    # Position the blue nodes in a pentagram shape
    center = (0, 0)
    radius = 1
    angles = [math.radians(90 + 72 * i) for i in range(5)]  # 5 angles for a pentagram
    for i, node in enumerate(blue_nodes):
        pos[node] = (center[0] + radius * math.cos(angles[i]), center[1] + radius * math.sin(angles[i]))

    # Position the green and yellow nodes randomly with constraints
    outer_radius_min = 2  # Minimum distance from center
    outer_radius_max = 3  # Maximum distance from center
    all_other_nodes = green_nodes + yellow_nodes 

    for node in all_other_nodes:
        while True:
            # Generate random radius and angle
            random_radius = random.uniform(outer_radius_min, outer_radius_max)
            random_angle = random.uniform(0, 2 * math.pi) 

            # Calculate x and y coordinates
            x = center[0] + random_radius * math.cos(random_angle)
            y = center[1] + random_radius * math.sin(random_angle)

            valid_position = True
            for existing_node in pos:
                existing_x, existing_y = pos[existing_node]
                distance = math.sqrt((x - existing_x)**2 + (y - existing_y)**2)
                if distance < 0.5: 
                    valid_position = False
                    break

            if valid_position:
                pos[node] = (x, y)
                break 


    # Extract node positions and colors
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]

    # Extract edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])  # Add None to create a gap between edges
        edge_y.extend([y0, y1, None])

    # Create the network graph
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='gray'),
        hoverinfo='none',
        mode='lines'
    )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="middle center",
        marker=dict(
            size=40,
            color=node_colors,
            line=dict(width=2, color='black')
        ),
        hoverinfo='text'
    )

    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                                   scaleanchor="y", scaleratio=1), 
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        font_size=15,
                        font_weight="bold",
                    ))

    fig.show()

    return fig