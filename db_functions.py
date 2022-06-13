import sqlite3
from random import choice

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()

def add_user(user):
    cursor.execute(f"INSERT INTO users (name, id) VALUES (?, ?)", (user.name, user.id))
    db.commit()
    print("added a user")

def generate_fap_id():
    chars = "0123456789abcdef"
    hex_string = ""
    for i in range(6):
        hex_string += choice(chars)
    return hex_string

def add_fap(user):
    user_exists = cursor.execute(f"SELECT * FROM users WHERE id = {user.id}").fetchone()
    if not user_exists:
        add_user(user)
    hex_string = generate_fap_id()
    cursor.execute(f"INSERT INTO faps (id, user, date) VALUES (?, ?, datetime('now'))", (hex_string, user.id))
    db.commit()