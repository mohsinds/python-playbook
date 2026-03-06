import mysql.connector
from app.config.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn