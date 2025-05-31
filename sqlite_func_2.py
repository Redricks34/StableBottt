import sqlite3


def save_data_in_database_2(file, sett, data, user, id_user=False):
    db = sqlite3.connect(f"{file}.db")
    table = "users"
    if file == "stats_user":
        table = "user_stats"
    settt = "username"
    if id_user:
        settt = "id"
    cur = db.cursor()
    sql_update_query = f'''UPDATE {table} SET {sett} = ? WHERE {settt} = ?'''
    data_b = (data, user)
    cur.execute(sql_update_query, data_b)
    db.commit()
    db.close()


def get_items_2(file, user, id_user=False):
    db = sqlite3.connect(f"{file}.db")
    table = "users"
    if file == "stats_user":
        table = "user_stats"
    num = 1
    if id_user:
        num = 0
    c = db.cursor()
    c.execute(f"SELECT * FROM {table}")
    db.commit()
    items = c.fetchall()
    db.close()
    bool_ = False
    for i in range(len(items)):
        if str(items[i][num]) == str(user):
            bool_ = True
            break
    return [bool_, items[i]]
