from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mkojil8809@localhost:5432/capim_limao'

app.config["SECRET_KEY"] = "bddfaa05e05bcd560b8f8a239352802b"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'fotos_prod')

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from Capim import routes #this import must happen after app is created