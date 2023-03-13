import sqlite3
from sqlite3 import Error

class SQLite:
    def __init__(self, db_file):
        self.db_file = db_file

    def connect(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)

    def execute(self, sql, params=None):
        conn = self.connect()
        cur = conn.cursor()
        if params is None:
            cur.execute(sql)
        else:
            cur.execute(sql, params)
        conn.commit()
        conn.close()
        return cur.lastrowid
