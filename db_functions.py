import sqlite3
import discord

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()

def add_user(user):
    sql = "INSERT INTO users (name, id) VALUES (?, ?)"
    val = (user.name, user.id)
    cursor.execute(sql, val)
    db.commit()