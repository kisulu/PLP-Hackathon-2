from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_required, current_user
from models import db, User
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.flashcard_routes import flashcard_bp
    from routes.suggestion_routes import suggestion_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(flashcard_bp, url_prefix='/flashcards')
    app.register_blueprint(suggestion_bp, url_prefix='/suggestions')
    
    # Main routes
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return render_template('index.html')
        return redirect(url_for('auth.login'))
    
    @app.route('/premium')
    @login_required
    def premium():
        return render_template('premium.html')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)