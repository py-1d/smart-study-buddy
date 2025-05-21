import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploaded_pdfs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')

    # extensions
    db.init_app(app)

    # blueprints
    from app.routes import main
    app.register_blueprint(main)

    # logs
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('App startup')

    # initializing db
    @app.cli.command('init-db')
    @with_appcontext
    def init_db():
        db.create_all()
        click.echo("Initialized the database.")

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
