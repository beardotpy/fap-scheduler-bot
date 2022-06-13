import sqlite3
from random import choice

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()

def add_user(user):
    cursor.execute(f"INSERT INTO users (name, user_id) VALUES (?, ?)", (user.name, user.id))
    db.commit()
    print("added a user")

def add_fap(user):
    user_exists = cursor.execute(f"SELECT * FROM users WHERE user_id = {user.id}").fetchone()
    if not user_exists:
        add_user(user)
    cursor.execute(f"INSERT INTO faps (user_id, date) VALUES (?, datetime('now'))", (user.id,))
    db.commit()