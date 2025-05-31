import sqlite3
import time
import datetime
from sqlite_func import save_data_in_database


while True:
    db = sqlite3.connect('userbase.db')
    c = db.cursor()
    c.execute(f"SELECT * FROM users")
    db.commit()
    items = c.fetchall()
    db.commit()
    db.close()
    k = 0
    for i in range(len(items)):
        if int(items[i][2]) < 15:
            save_data_in_database("balance", 15, items[i][0])
            k += 1

    save_data_in_database("balance", 500, 401911274)
    now = datetime.datetime.now()
    print(str(now) + f" токены успешно пополнены. {k} людей получили токены")
    time.sleep(86400)
