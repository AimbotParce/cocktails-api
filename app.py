"""
Remember to set the environment variables:
- API_PORT
- API_HOST
- DATABASE_URL
- USERS_DATABASE_URL
"""

import os

from api import app
from flask_cors import CORS

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

if __name__ == "__main__":
    import waitress

    waitress.serve(app, port=os.environ.get("API_PORT"), host=os.environ.get("API_HOST"))
