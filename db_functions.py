import sqlite3

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()

def add_user(user, timezone):
    cursor.execute(
        ("INSERT INTO " 
         "users (name, user_id, timezone) "
         "VALUES (?, ?, ?)"),
        (user.name, user.id, timezone)
    )
    db.commit()

def get_user(user):
    return cursor.execute(
        ("SELECT * "
         "FROM users "
         f"WHERE user_id = {user.id}")
    ).fetchone()

def change_timezone(user, timezone):
    cursor.execute(
        ("UPDATE users "
         "SET timezone = ? "
         "WHERE user_id = ?"),
         (timezone, user.id)
    )
    db.commit()

def add_fap(user):
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

def get_faps(user, offset):
    hour_offset, minute_offset = offset[0]+offset[1], offset[0]+offset[2]
    if not user:
        faps = cursor.execute(
            (f"SELECT faps.fap_id, users.name, STRFTIME('%d/%m/%Y', faps.date, '{hour_offset} hours', '{minute_offset} minutes'), STRFTIME('%H:%M', faps.date, '{hour_offset} hours', '{minute_offset} minutes') "
             "FROM faps, users "
             "WHERE faps.user_id = users.user_id")
        ).fetchall()
        return faps
    faps = cursor.execute(
        (f"SELECT faps.fap_id, users.name, STRFTIME('%d/%m/%Y', faps.date, '{hour_offset} hours', '{minute_offset} minutes'), STRFTIME('%H:%M', faps.date, '{hour_offset} hours', '{minute_offset} minutes') "
         "FROM faps, users "
         "WHERE faps.user_id = ? AND users.user_id = ?"),
        (user.id, user.id)
    ).fetchall()
    return faps