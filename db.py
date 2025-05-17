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
            user_id int,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
        );
        '''
    )

    con.commit()
    close_connection(con,cur)


def init_obj(userho):
    con = open_connection()
    cur = con.cursor()
    cur.execute("""
    insert into users(telegram_id,username,phone_number,ind_id)
    values(?,?,?,?)


    """,(userho["telegram_id"],userho["username"],userho["phone_number"],userho["ind_id"]))
    con.commit()
    close_connection(con,cur)


def init_kargos(kargos):
    con = open_connection()
    cur = con.cursor()
    cur.execute("""
    insert into kargos(kod,vazn,adress)
    values(?,?,?)


    """,(kargos["kod"],kargos["vazn"],kargos["adress"]))
    con.commit()
    close_connection(con,cur)
    



def show_zakaz():
    conn=open_connection()
    cur=conn.cursor()
    cur.execute("select * from kargos")
    products = cur.fetchall()
    conn.commit()
    
    close_connection(conn,cur)
    return products
    
def delete_zakaz(kr_id):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM kargos WHERE id = ?", (kr_id,))
    conn.commit()
    close_connection(conn, cur)
    print("Deleted succefully")

def update_zakaz(pr_id, new_adres):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("update kargos set adress = ? where id = ?", (new_adres, pr_id))
    conn.commit()
    close_connection(conn, cur)
