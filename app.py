from flask import Flask
from extensions import db, login_manager, csrf


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'flasksocial-dev-secret-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasksocial.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'გთხოვთ შეხვიდეთ სისტემაში.'
    login_manager.login_message_category = 'warning'

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.posts import posts_bp
    from routes.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
