import sqlite3

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()

def add_user(user):
    cursor.execute(
        ("INSERT INTO " 
         "users (name, user_id) "
         "VALUES (?, ?)"),
        (user.name, user.id)
    )
    db.commit()
    print("added a user")

def add_fap(user):
    user_exists = cursor.execute(f"SELECT * FROM users WHERE user_id = {user.id}").fetchone()
    if not user_exists:
        add_user(user)
    cursor.execute(
        ("INSERT INTO "
         "faps (user_id, date) "
         "VALUES (?, datetime('now'))"),
        (user.id,))
    db.commit()

def remove_fap(user, fap_id = None):
    if not fap_id:
        cursor.execute(
            ("DELETE FROM faps "
             "WHERE user_id = ? "
             "AND fap_id = (SELECT MAX(fap_id) FROM faps WHERE user_id = ?)"),
            (user.id, user.id))
        db.commit()
    else:
        cursor.execute(
            ("DELETE FROM faps "
             "WHERE user_id = ? "
             "AND fap_id = ?"),
            (user.id, fap_id))
        db.commit()

    if cursor.rowcount == 0:
        raise Exception()

def get_faps(user=None):
    if not user:
        faps = cursor.execute(
            ("SELECT faps.fap_id, users.name, STRFTIME('%d/%m/%Y', faps.date), STRFTIME('%H:%M', faps.date) "
             "FROM faps, users "
             "WHERE faps.user_id = users.user_id")
        ).fetchall()
        return faps
    faps = cursor.execute(
        ("SELECT faps.fap_id, users.name, STRFTIME('%d/%m/%Y', faps.date), STRFTIME('%H:%M', faps.date) "
         "FROM faps, users "
         "WHERE faps.user_id = ? AND users.user_id = ?"),
        (user.id, user.id)
    ).fetchall()
    return faps