from flask import Flask
from extensions import db
from flask_migrate import Migrate
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schooldb.db'
    db.init_app(app)
    migrate = Migrate(app, db)
    register_routes(app, db)
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)

