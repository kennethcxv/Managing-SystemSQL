from flask import Flask
from models import db
from config import Config

# Importing Blueprints
from controllers.main_routes import main
from controllers.user_routes import user
from controllers.admin_routes import admin
from controllers.book_routes import book_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(book_routes)
    app.register_blueprint(main)

    return app


if __name__ == '__main__':
    bookstore_app = create_app()
    with bookstore_app.app_context():
        db.create_all()
    bookstore_app.run(debug=True)
