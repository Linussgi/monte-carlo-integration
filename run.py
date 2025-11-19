from app import app
import layout
import app_updater

app.layout = layout.app_layout

app.run(debug=False, port=8052)