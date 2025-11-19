from dash import html, dcc
from app import MAX_POINTS

# Left column
left_column = html.Div([
    html.Div([
        html.Div("Plot", className="section-title"),
        dcc.Graph(id="montecarlo-plot", style={"height": "550px"})
    ], className="plot-container"),

    html.Div([
        html.Label("Number of Points:", style={"fontWeight": "600", "marginBottom": "10px", "display": "block"}),

        # Slider stuff
        dcc.Slider(
            id="points-slider",
            min=0,
            max=MAX_POINTS,
            step=MAX_POINTS // 20,
            value=0,
            marks={i: str(i) for i in range(0, MAX_POINTS + 1, MAX_POINTS // 10)},
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode="drag"
        )
    ], className="plot-container")
], className="left-column")

# Right column
right_column = html.Div([
    html.Div([
        html.Div("Function Input", className="section-title"),
        dcc.Input(id="function-input", type="text", value="np.cos(np.pi*x)", style={"width": "100%", "padding": "8px"})
    ], className="section-container"),

    html.Div([
        html.Div("Area Convergence", className="section-title"),
        dcc.Graph(id="area-plot", style={"height": "320px"}),
        html.Div(id="area-info", className="info-box")
    ], className="section-container")
], className="right-column")

# Full layout
app_layout = html.Div([
    html.Div("Monte Carlo Integrator", className="header"),
    html.Div([left_column, right_column], className="container-flex")
])
