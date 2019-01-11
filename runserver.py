"""
Runs the API server.
"""

# Import api module to bind endpoints to Flask instance.
# Without this import, the endpoints declared in that module
# will not work.
from barebones import app, SERVER_IP


if __name__ == "__main__":
    app.run(host=SERVER_IP, debug=True)
