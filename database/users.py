import sqlite3
from init_db import Database

class User_db(Database):
    def __init__(self):
        super().__init__()
    
    def add_user(self, nickname: str, tg_id: int) -> None:
        try:
            self.cursor.execute("INSERT INTO users (nickname, tg_id) VALUES (?, ?)", (nickname, tg_id))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("User already exists")
    
    def user_exists(self, tg_id: int) -> bool:
        self.cursor.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
        return True if self.cursor.fetchone() else False