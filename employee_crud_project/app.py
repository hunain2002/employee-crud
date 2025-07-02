# app.py (entry point)
from flask import Flask
from flask_mysqldb import MySQL
from config import Config
from routes.auth import auth_bp
from routes.employee import employee_bp
from routes.attendance import attendance_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(dashboard_bp)

# Provide db access globally
app.mysql = mysql

if __name__ == '__main__':
    app.run(debug=False)
