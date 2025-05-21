from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploaded_pdfs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    app.config['SECRET_KEY'] = 'supersecretkey'

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app