from dash import Dash

# Maximum value of slider
MAX_POINTS = 2000

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

server = app.server