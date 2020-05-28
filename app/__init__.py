from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from config import SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS, SQL_URI, CSRF_ENABLED

@event.listens_for(Engine, "connect")
def sqlite_pragma(dbapi_con, conn_record):
    cursor = dbapi_con.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI
app.config['CSRF_ENABLED'] = CSRF_ENABLED
lm = LoginManager(app)
db = SQLAlchemy(app)

from app import views