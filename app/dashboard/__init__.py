from flask import Blueprint

dashboard_bp = Blueprint("dashboard", __name__)

# Import routes so decorators register
from . import routes, repos  # noqa: F401
