from src import bar 
from src import sankey 
from src import network 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

bar_graph = bar.execute()
sankey_graph = sankey.execute()
network_graph = network.execute()

fig = make_subplots(rows=2, cols=2, 
                    subplot_titles=("Bar Chart", "Network Plot", "Sankey", ""),
                    specs=[[{"type": "bar"}, {"rowspan": 2, "type": "scatter"}],
                    [{"type": "sankey"}, None]],)

# Add figures to subplots
for trace in bar_graph.data:
    fig.add_trace(trace, row=1, col=1)
fig.update_layout(barmode='stack')

# Add network graph
for trace in network_graph.data:
    fig.add_trace(trace, row=1, col=2)

# Add Sankey diagram
for trace in sankey_graph.data:
    fig.add_trace(trace, row=2, col=1)

# Update layout

fig.update_layout(
    title_text="Combined Plots",
    showlegend=False,
    margin=dict(l=50, r=50, b=50, t=100),
    font_weight="bold"
)

fig.show()