from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_app.api.v1.auth import auth
from flask_app.api.v1.roles import roles
from flask_app.api.v1.users import users


app = Flask(__name__)

Swagger(app, template_file="project-description/openapi.yaml")
SQLAlchemy(app)

app.register_blueprint(auth, url_prefix="/api/v1/auth")
app.register_blueprint(roles, url_prefix="/api/v1/roles")
app.register_blueprint(users, url_prefix="/api/v1/users")
