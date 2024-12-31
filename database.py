import sqlite3
from functions import get_last_seven_days
import pandas as pd


class Database:                        
    # конструктор класса
    def __init__(self):           
        # соединяемся с файлом базы данных
        self.conn = sqlite3.connect("data.db")  
        # создаём курсор для виртуального управления базой данных
        self.cur = self.conn.cursor()
        self.cur.execute('''
                        CREATE TABLE IF NOT EXISTS transaktions (
                        tran_id INTEGER PRIMARY KEY,
                        sum INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        categor TEXT NOT NULL,
                        comment TEXT NOT NULL
                        )
                        ''')    
        # если нужной нам таблицы в базе нет — создаём её
        self.cur.execute('''
                        CREATE TABLE IF NOT EXISTS something (
                        id INTEGER PRIMARY KEY,
                        comment TEXT NOT NULL
                        )
                        ''')
        self.conn.commit()
    def __del__(self):        
        # отключаемся от базы при завершении работы
        self.conn.close()
    
    def insert(self, sum, date, kategor, comment=''):
        # формируем запрос с добавлением новой записи в БД
        self.cur.execute("INSERT INTO transaktions VALUES (NULL,?,?,?,?)", (sum, date, kategor,comment)) 
        # сохраняем изменения
        self.conn.commit()

    def get_7_day(self):
        dates = get_last_seven_days()
        query = f"""SELECT * FROM transaktions WHERE date IN ({','.join(['?'] * len(dates))})"""
        return self.cur.execute(query, dates).fetchall()

    def export(self):
        df = pd.read_sql_query("SELECT * FROM transaktions", self.conn)
        return df.to_excel('export.xlsx')
    def is_id(self, us_id):
        return self.cur.execute('SELECT * FROM transaktions WHERE tran_id=%d' % us_id).fetchall()

    def delete_row(self, us_id):
        self.cur.execute('DELETE FROM transaktions WHERE tran_id=%d' % us_id)
        self.conn.commit()

    def change(self, us_id, new_sum, new_date, new_kategor, new_comment=''):
        self.cur.execute("UPDATE transaktions SET sum=?,date=?,categor=?,comment=? WHERE tran_id=?", (new_sum, new_date, new_kategor, new_comment, us_id))
        self.conn.commit()

    def get_sum(self, kategor):
        return self.cur.execute('SELECT SUM(sum) FROM transaktions WHERE categor=?', (kategor,)).fetchone()[0]

    def add_text(self, text):
        # формируем запрос с добавлением новой записи в БД
        self.cur.execute("INSERT INTO something VALUES (NULL,?)", (text,))
        # сохраняем изменения
        self.conn.commit()

    def delete_month(self):
        self.cur.execute("DELETE FROM 'transaktions'")
        self.conn.commit()

    def get_all_text(self):
        return self.cur.execute('SELECT * FROM something').fetchall()

    def change_text(self, id, new_text):
        self.cur.execute("UPDATE something SET comment=? WHERE id=?", (new_text, id))
        self.conn.commit()

    def delete_zametka(self, id):
        self.cur.execute('DELETE FROM something WHERE id=%s' % id)
        self.conn.commit()

    def delete_all_zametka(self):
        self.cur.execute('DELETE FROM something')
        self.conn.commit()