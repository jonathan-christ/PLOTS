import pandas as pd
import plotly.graph_objects as go

def execute():

    # Load the data
    data = pd.read_csv('data/sankey_assignment.csv')

    # Define the entities, labels, and categories
    entities = ['PS', 'OMP', 'CNP', 'NRP', 'NMCCC', 'PEC', 'NCDM', 'RGS']
    labels = data['LABEL'].unique()
    categories = ['Reg', 'Aca', 'Oth']

    # Create a mapping for source and target indices
    node_labels = entities + list(labels) + categories
    node_indices = {label: i for i, label in enumerate(node_labels)}

    # Define specific colors for nodes
    node_colors = [
        'salmon',  # PS
        'darkcyan',  # OMP
        'orange',  # CNP 1f77b4
        'hotpink',  # NRP
        'lightgreen',  # NMCCC
        'cyan',  # PEC
        'yellow',  # NCDM
        'magenta',  # RGS
        'skyblue',  # S
        'dodgerblue',  # F
        'teal',  # D
        'deepskyblue',  # N
        'aqua',  # I
        'darkgreen',  # Reg 2ca02c
        'lightgreen',  # Aca 98df8a
        'green',  # Oth
    ]

    # Map node indices to their colors
    node_color_map = {i: node_colors[i] for i in range(len(node_labels))}

    # Prepare the Sankey data
    sources = []
    targets = []
    values = []
    link_colors = []

    # Step 1: Connect entities to labels
    for _, row in data.iterrows():
        label = row['LABEL']
        for entity in entities:
            value = row[entity]
            if value > 0:
                sources.append(node_indices[entity])
                targets.append(node_indices[label])
                values.append(value)
                # Assign the color of the source node to the link
                link_colors.append(node_color_map[node_indices[entity]])

    # Step 2: Connect labels to categories
    for _, row in data.iterrows():
        label = row['LABEL']
        for category in categories:
            value = row[category]
            if value > 0:
                sources.append(node_indices[label])
                targets.append(node_indices[category])
                values.append(value)
                # Assign the color of the source node to the link
                link_colors.append(node_color_map[node_indices[label]])

    # Create the Sankey Diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=node_colors  # Assign specific colors to nodes
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors  # Assign colors to links based on source nodes
        )
    ))

    # Update layout
    fig.update_layout(title_text="Sankey Diagram", font_size=10)

    fig.show()
    return fig