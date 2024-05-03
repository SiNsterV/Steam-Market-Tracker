import streamlit as st
import hashlib
import sqlite3

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_usertable():
    with get_db_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS userstable(
            username TEXT UNIQUE, 
            password TEXT, 
            preset_name TEXT UNIQUE,
            items TEXT,
            );
        ''')
        conn.commit()

def add_userdata(username, password):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, password))
        conn.commit()

def login_user(username, password):
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password)).fetchone()
        return user
