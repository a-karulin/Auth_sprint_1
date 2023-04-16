from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from api.v1.auth import auth
from api.v1.roles import roles
from api.v1.users import users
from config import POSTGRES_CONN_STR

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_CONN_STR

Swagger(app, template_file="swagger/openapi.yaml")
SQLAlchemy(app)

app.register_blueprint(auth, url_prefix="/api/v1/auth")
app.register_blueprint(roles, url_prefix="/api/v1/roles")
app.register_blueprint(users, url_prefix="/api/v1/users")


@app.route('/')
def get_status():
    return {'status': 'ok'}


if __name__ == '__main__':
    app.run()
