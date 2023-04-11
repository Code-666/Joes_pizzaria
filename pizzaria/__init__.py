from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "678196595f75dbba335a98c1ab3a9f6bbc25a4a9f78367c1f969c6137dc136c4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from pizzaria import routes