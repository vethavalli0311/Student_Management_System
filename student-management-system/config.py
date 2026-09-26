import os
import pymysql

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'vethavalli-student-mgmt-key-2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MySQL Configuration variables
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'student_management_db')

    # Try connecting to MySQL; fallback to SQLite if credentials are required
    DB_CONNECTED_MYSQL = False
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            connect_timeout=2
        )
        # Create database if it does not exist
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DB}` CHARACTER SET utf8mb4;")
        conn.close()

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        )
        DB_CONNECTED_MYSQL = True
        DB_STATUS_LABEL = f"MySQL Database ({MYSQL_DB})"
    except Exception as e:
        # Fallback to local SQLite so application runs immediately without crashing
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'student_management.db')}"
        DB_CONNECTED_MYSQL = False
        DB_STATUS_LABEL = "SQLite Fallback (Configure MySQL password in config.py or .env)"
