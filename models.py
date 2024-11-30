from app import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime  # Para gestionar la fecha de inicio de sesión

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)  # Nuevo campo para guardar la última sesión

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
