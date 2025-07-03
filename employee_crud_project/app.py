# app.py (Entry Point)

from flask import Flask
from flask_mysqldb import MySQL
from config import Config

# Importing all route blueprints
from routes.auth import auth_bp
from routes.employee import employee_bp
from routes.attendance import attendance_bp
from routes.dashboard import dashboard_bp
from routes.reports import reports_bp


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # MySQL init and make available app-wide
    mysql = MySQL(app)
    app.mysql = mysql

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reports_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # 🔁 Debug True for development
