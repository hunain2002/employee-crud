from flask import Flask
from flask_mysqldb import MySQL
from config import Config
from routes.auth import auth_bp
from routes.employee import employee_bp
from routes.attendance import attendance_bp
from routes.dashboard import dashboard_bp
from routes.reports import reports_bp
from routes.chatbot import chatbot_bp

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
    app.config.from_object(Config)
    mysql = MySQL(app)
    app.mysql = mysql
    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(chatbot_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
