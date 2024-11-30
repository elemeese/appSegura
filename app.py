from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

# Crear la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'  # Cambia esto por algo más seguro
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Inicializar extensiones
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configuración de Flask-Limiter
limiter = Limiter(get_remote_address, app=app)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Importar rutas
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
