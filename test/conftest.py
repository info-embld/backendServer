import pytest
from flask import Flask
from flask_mailman import Mail
from flask_login import LoginManager
from models.db_conf import db, init_db  
from werkzeug.security import generate_password_hash
from models.licenses import License
from models.users import User
from datetime import datetime, timedelta
import os

login_manager = LoginManager()
mail = {}
@pytest.fixture
def app():
    test_app = Flask(__name__)
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'JWT_SECRET_KEY': 'test-jwt-secret-key',
        'MAIL_USERNAME': 'test@example.com',
        'MAIL_PASSWORD': 'testpassword',
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': 587,
        'MAIL_USE_TLS': True,
    })
    mail = Mail()
    mail.init_app(test_app)
    login_manager.init_app(test_app)
    login_manager.login_view = 'user_routes.login_route'
    init_db(test_app)  
    
    from routes.user_routes import user_bp
    from routes.payments_routes import payments_bp
    from routes.license_routes import license_bp
    from routes.email_route import email_bp
    test_app.register_blueprint(user_bp, url_prefix='/')
    test_app.register_blueprint(payments_bp, url_prefix='/')
    test_app.register_blueprint(license_bp, url_prefix='/')
    test_app.register_blueprint(email_bp, url_prefix='/')
    
    yield test_app
    with test_app.app_context():
        db.drop_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_test_db(app):
    with app.app_context():
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=generate_password_hash("testpass"),
            newsletter_sub=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Add a license for the user to satisfy NOT NULL constraint
        license = License(
            user_id=user.id,
            license_key="test-license-key",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=365)
        )
        db.session.add(license)
        db.session.commit()
        
        yield user
        db.session.remove()

@pytest.fixture
def authenticated_client(client, init_test_db):
    with client:
        client.post('/login', json={'email': 'test@example.com', 'password': 'testpass'})
        yield client

@pytest.fixture
def mail(app):
    """Provice the Flask-Mail instance for testing"""
    return app.extensions['mail']

@pytest.fixture
def mock_smtp(mocker):
    mock = mocker.patch('smtplib.SMTP')
    mock.return_value.starttls.return_value = None
    mock.return_value.login.return_value = None
    mock.return_value.sendmail.return_value = None
    mock.return_value.quit.return_value = None
    return mock