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
            steamapikey TEXT,
            preset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            preset_name TEXT UNIQUE,
            items TEXT NOT NULL,
            UNIQUE(username,preset_name)
            );
        ''')
        conn.commit()

def add_userdata(username, password, steam_api_key):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO userstable(username, password, steamapikey) VALUES (?, ?, ?)', (username, password, steam_api_key))
        conn.commit()

def login_user(username, password):
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password)).fetchone()
        return user

def update_steam_api_key(username, steam_api_key):
    with get_db_connection() as conn:
        conn.execute('UPDATE userstable SET steamapikey = ? WHERE username = ?', (steam_api_key, username))
        conn.commit()

def is_steam_api_key_zero(username):
    with get_db_connection() as conn:
        api_key = conn.execute('SELECT steamapikey FROM userstable WHERE username = ?', (username,)).fetchone()
        if api_key and api_key['steamapikey'] == '0':
            return True
        else:
            return False
 
