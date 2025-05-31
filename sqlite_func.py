import sqlite3


def get_all_user_id():
    info_id = []
    database = sqlite3.connect("userbase.db")
    cur = database.cursor()
    cur.execute("SELECT * FROM users")
    all_id_info = cur.fetchall()
    for id_i in all_id_info:
        info_id.append(id_i[0])

    return info_id


def save_data_in_database(sett, data, user_id):
    db = sqlite3.connect("userbase.db")
    cur = db.cursor()
    sql_update_query = f'''UPDATE users SET {sett} = ? WHERE id = ?'''
    data_b = (data, user_id)
    cur.execute(sql_update_query, data_b)
    db.commit()
    db.close()


def get_items(user_id):
    db = sqlite3.connect('userbase.db')
    c = db.cursor()
    c.execute(f"SELECT * FROM users")
    db.commit()
    items = c.fetchall()
    db.close()
    for i in range(len(items)):
        if str(items[i][0]) == str(user_id):
            break
    return items[i]
