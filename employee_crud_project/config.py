import os

class Config:
    SECRET_KEY = 'secretkey'

    # MySQL Database Config
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'employee_crud'

    # Static file upload paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    QR_FOLDER = os.path.join('static', 'qrcodes')
import os

class Config:
    SECRET_KEY = 'secretkey'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'employee_crud'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    QR_FOLDER = os.path.join(BASE_DIR, 'static', 'qrcodes')
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
