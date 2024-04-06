"""
Remember to set the environment variables:
- DATABASE_URL
- USERS_DATABASE_URL
"""

from api import app
from flask_cors import CORS

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"
