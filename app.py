"""
Remember to set the environment variables:
- API_PORT
- API_HOST
- DATABASE_URL
"""

import os

from flask_cors import CORS

from api import app

if __name__ == "__main__":
    import waitress

    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config["CORS_HEADERS"] = "Content-Type"

    waitress.serve(app, port=os.environ.get("API_PORT"), host=os.environ.get("API_HOST"))
