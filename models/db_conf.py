from flask_sqlalchemy import SQLAlchemy

# Define db as a global instance, but don’t bind it to an app yet
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create tables when initialized