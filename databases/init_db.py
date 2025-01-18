import sqlite3


class Database():
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()