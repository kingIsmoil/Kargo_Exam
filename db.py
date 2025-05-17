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
            telegram_id bigint
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
    insert into kargos(kod,vazn,adress,telegram_id)
    values(?,?,?,?)


    """,(kargos["kod"],kargos["vazn"],kargos["adress"],kargos['user_id']))
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
    cur.execute("DELETE FROM kargos WHERE kod = ?", (kr_id,))
    conn.commit()
    close_connection(conn, cur)
    print("Deleted succefully")

def update_kargo_full(pr_id, new_kod=None, new_vazn=None, new_adres=None):
    conn = open_connection()
    cur = conn.cursor()

    if new_kod:
        cur.execute("UPDATE kargos SET kod = ? WHERE id = ?", (new_kod, pr_id))
    if new_vazn:
        cur.execute("UPDATE kargos SET vazn = ? WHERE id = ?", (new_vazn, pr_id))
    if new_adres:
        cur.execute("UPDATE kargos SET adress = ? WHERE id = ?", (new_adres, pr_id))

    conn.commit()
    close_connection(conn, cur)
    print("Updated successfully")
