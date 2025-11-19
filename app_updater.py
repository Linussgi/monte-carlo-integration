from dash import Input, Output
import plotly.graph_objects as go
import numpy as np
from app import app, MAX_POINTS 

@app.callback(
    [
        Output("montecarlo-plot", "figure"),
        Output("area-plot", "figure"),
        Output("area-info", "children")
    ],
    [
        Input("points-slider", "value"),
        Input("function-input", "value")
    ]
)
def update_montecarlo(n_points, func_str):
    rng = np.random.RandomState(200)

    x_range = rng.uniform(-1, 1, MAX_POINTS)
    y_range = rng.uniform(-1, 1, MAX_POINTS)

    # Convert function string to python function (could do more work here ot make this more flexible)
    try:
        func_vals_all = np.array([eval(func_str, {"np": np, "x": x_val}) for x_val in x_range])
    except Exception:
        func_vals_all = np.zeros_like(x_range)

    # True integral by trapezium rule
    x_curve = np.linspace(-1, 1, 1000)
    try:
        y_curve = np.array([eval(func_str, {"np": np, "x": x_val}) for x_val in x_curve])
    except Exception:
        y_curve = np.zeros_like(x_curve)

    true_integral = np.trapz(y_curve, x_curve)

    # Monte Carlo scatter plot
    x = x_range[:n_points]
    y = y_range[:n_points]
    func_vals = func_vals_all[:n_points]

    # First condition is for positive area, second condition is for negative area
    pos_mask = (y >= 0) & (y <= func_vals)
    neg_mask = (y < 0) & (y >= func_vals)

    colors = np.where(pos_mask, "green", np.where(neg_mask, "red", "grey"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode="lines", line=dict(color="blue", width=3), name="Function"))
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(color=colors, size=8, opacity=0.7, line=dict(width=0.5, color='white')), name="Points"))
    
    fig.update_layout(
        xaxis=dict(range=[-1, 1], title="x"),
        yaxis=dict(range=[-1, 1], title="y"),
        template="plotly_white",
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Inter, sans-serif", size=12, color="#495057")
    )

    # Area convergence, calculated every MAX_POINTS // 50 points
    step = MAX_POINTS // 50

    if n_points < step:
        sample_counts = np.array([], dtype=int)
        estimates = np.array([])
    else:
        sample_counts = np.arange(step, n_points + 1, step)
        estimates = []

        # To procedually build the convergence graph p to the current number of points, we only look at the first k values
        for k in sample_counts:
            point_y_ords = y_range[:k]
            func_y_ords = func_vals_all[:k]

            pg = np.sum((point_y_ords >= 0) & (point_y_ords <= func_y_ords))
            pr = np.sum((point_y_ords < 0) & (point_y_ords >= func_y_ords))

            # The chart space is x in [-1, 1] and y in [-1, 1] so the total area of the square is 4.0
            integral_estimate = 4.0 * (pg/k - pr/k) if k > 0 else 0.0

            estimates.append(integral_estimate)

        estimates = np.array(estimates)

    # Area convergence plot
    area_fig = go.Figure()

    if sample_counts.size > 0:
        area_fig.add_trace(go.Scatter(x=sample_counts, y=estimates, mode="lines", name="Monte Carlo Estimate"))

    area_fig.add_trace(go.Scatter(x=[0, MAX_POINTS], y=[true_integral, true_integral], mode="lines", name="True Integral", line=dict(color="red", dash="dot", width=2)))

    area_fig.update_layout(
        xaxis=dict(title="Number of Points", range=[0, max(10, n_points)]),
        yaxis=dict(title="Integral (area)"),
        template="plotly_white",
        margin=dict(l=40, r=20, t=30, b=40),
        font=dict(family="Inter, sans-serif", size=11, color="#495057"),
        showlegend=False
    )

    # Area error
    if n_points > 0:
        current_area = 4.0 * (np.sum(pos_mask) / n_points - np.sum(neg_mask) / n_points)
    else:
        current_area = 0.0

    info_text = f"Current area error: {current_area - true_integral:.4f}"

    return fig, area_fig, info_text
