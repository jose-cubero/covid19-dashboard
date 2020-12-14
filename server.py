import os
import covid19_dashboard.dash_main as dm

app = dm.get_dash_app()
# app.run_server(debug=False)

if __name__ == "__main__":
    # Get port and debug mode from environment variables
    port = os.environ.get('dash_port') or 8050
    debug = os.environ.get('dash_debug')=="True"
    app.run_server(debug=debug, host="0.0.0.0", port=port)
