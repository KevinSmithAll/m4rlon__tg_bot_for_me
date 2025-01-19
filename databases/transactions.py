import sqlite3
from databases.init_db import Database
import pandas as pd
from functions import get_last_seven_days, get_last_three_days

class Transaction_db(Database):
    def __init__(self):
        super().__init__()
    
    def add_transaction(self, 
                        tg_id: int, 
                        date: str, 
                        value: int, 
                        category: str, 
                        comment='') -> None:
        self.cursor.execute("INSERT INTO transactions VALUES (NULL, (SELECT user_id FROM users WHERE tg_id=?), ?, ?, ?, ?)", (tg_id, date, value, category, comment))
        self.conn.commit()

    def get_7_day(self, tg_id: int):
        dates = get_last_seven_days()
        query = f"""SELECT value, date, category, comment FROM transactions WHERE user_id=(SELECT user_id FROM users WHERE tg_id={tg_id}) AND date IN ({','.join(['?'] * len(dates))})"""
        return self.cursor.execute(query, dates).fetchall()

    def get_3_day(self, tg_id: int):
        dates = get_last_three_days()
        query = f"""SELECT value, date, category, comment FROM transactions WHERE user_id=(SELECT user_id FROM users WHERE tg_id={tg_id}) AND date IN ({','.join(['?'] * len(dates))})"""
        return self.cursor.execute(query, dates).fetchall()
        
    def export_transactions(self):
        df = pd.read_sql_query("SELECT * FROM transactions", self.conn)
        return df.to_excel('export.xlsx')
