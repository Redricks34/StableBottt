import random

from webuiapi import webuiapi
from PIL import Image
import sqlite3

def upscaler(user_id):

    api = webuiapi.WebUIApi(steps=25)
    result1 = Image.open(f'outs/{user_id}/{user_id}rd.png')
    result2 = api.extra_single_image(upscaling_resize=2, image=result1, upscaler_1='R-ESRGAN 4x+ Anime6B', upscaler_2='R-ESRGAN 4x+ Anime6B')
    result2.image.save(f'outs/{user_id}/{user_id}-upscaled.png')

    db = sqlite3.connect('userbase.db')
    c = db.cursor()
    sql_update_query_st = """UPDATE users SET status = ? WHERE id = ?"""
    data_st = (0, user_id)
    c.execute(sql_update_query_st, data_st)
    db.commit()
    db.close()

    db = sqlite3.connect('userbase.db')
    c = db.cursor()
    sql_update_query_hq = """UPDATE users SET hquality = ? WHERE id = ?"""
    data_hq = (0, user_id)
    c.execute(sql_update_query_hq, data_hq)
    db.commit()
    db.close()