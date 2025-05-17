import sqlite3
from datetime import datetime

def open_connection():
    sqliteconnection = sqlite3.connect('sql.db')
    return sqliteconnection

def close_connection(con, cur):
    cur.close()
    con.close()

def init_models():
    con = open_connection()
    cur = con.cursor()
    cur.execute(
        '''
    CREATE TABLE IF NOT EXISTS users(
        telegram_id bigint,
        username varchar(50),
        phone_number varchar(20),
        ind_id varchar(50)
    );
'''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS kargos(
            id integer primary key autoincrement,
            kod varchar(50),
            vazn decimal(10,3),
            adress text,
            user_id bigint,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        );
        '''
    )
    