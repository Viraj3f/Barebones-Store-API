"""
Runs the API server.
"""

# Import api module to bind endpoints to Flask instance.
# Without this import, the endpoints declared in that module
# will not work.
import api
from app import app, SERVER_IP


if __name__ == "__main__":
    app.run(host=SERVER_IP)
