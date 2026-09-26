import plotly.graph_objects as go

def build_graph_figure(nodes, edges):
    pos = {
        "Supplier": (0, 0.5),
        "Component": (1, 0.5),
        "Manufacturer": (2, 0.5),
        "Product": (3, 0.5),
        "Market": (4, 0.5),
    }
    node_map = {n["id"]: n for n in nodes}
    edge_x, edge_y = [], []
    for a, b in edges:
        x0, y0 = pos[a]
        x1, y1 = pos[b]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=3),
        hoverinfo="none"
    ))

    xs, ys, labels, scores = [], [], [], []
    for n in nodes:
        x, y = pos[n["id"]]
        xs.append(x); ys.append(y)
        labels.append(n["label"])
        scores.append(n["score"])

    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers+text",
        text=labels, textposition="bottom center",
        marker=dict(size=42, color=scores, colorscale="RdYlGn_r",
                    cmin=0, cmax=100, colorbar=dict(title="Exposure")),
        hovertemplate="<b>%{text}</b><br>Exposure: %{marker.color:.0f}/100<extra></extra>"
    ))
    fig.update_layout(
        height=420, margin=dict(l=20, r=20, t=20, b=80),
        xaxis=dict(visible=False, range=[-0.5, 4.5]),
        yaxis=dict(visible=False, range=[0, 1]),
        showlegend=False,
    )
    return fig
