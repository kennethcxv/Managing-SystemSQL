from flask import Blueprint
from . import main_routes, user_routes, admin_routes, book_routes

# Create the flask blueprints
main = Blueprint('main', __name__)
user = Blueprint('user', __name__)
admin = Blueprint('admin', __name__)
book = Blueprint('book', __name__)
