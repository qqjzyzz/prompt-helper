import mysql.connector
import hashlib
import streamlit as st

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='yuan',
        password='mima',
        database='database'
    )
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        st.success("注册成功！请登录。")
    except mysql.connector.IntegrityError:
        st.error("用户名已存在，请选择其他用户名。")
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    hashed_password = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, hashed_password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return bool(user)
