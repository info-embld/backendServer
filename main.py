from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from models.db_conf import db, init_db
import os

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_routes.login_route'  # Update if needed
mail = Mail(app)  # Initialize Flask-Mail

from models.users import User
from models.licenses import License
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

init_db(app)

from routes.user_routes import user_bp
from routes.payments_routes import payments_bp
from routes.license_routes import license_bp
from routes.email_route import email_bp

app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(payments_bp, url_prefix='/')
app.register_blueprint(license_bp, url_prefix='/')
app.register_blueprint(email_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)