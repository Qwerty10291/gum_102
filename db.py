import sqlite3
from datetime import datetime as dt


class Database:
    def __init__(self, db):
        self.db = db

    def check_user(self, login):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            result = cursor.execute('SELECT * FROM `users` WHERE `login` = ?', (login,)).fetchall()
            return bool(len(result))


    def add_user(self, login, password, edu_login, edu_pass, id):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO `users` VALUES (?, ?, ?, ?, ?)', (id, login, password, edu_login, edu_pass))

    def get_id(self, login):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            return list(cursor.execute('SELECT `id` FROM `users` WHERE `login` = ?', (login,)).fetchone())[0]

    def get_password(self, login):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            return str(list(cursor.execute('SELECT `password` FROM `users` WHERE `login` = ?', (login,)).fetchone())[0])

    def get_edu(self, id):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            login = list(cursor.execute('SELECT `edu_login` FROM `users` WHERE `id` = ?', (id, )).fetchone())[0]
            password = list(cursor.execute('SELECT `edu_pass` FROM `users` WHERE `id` = ?', (id, )).fetchone())[0]
            return [login, password]

    def get_login(self, id):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            return list(cursor.execute('SELECT `login` FROM `users` WHERE `id` = ?', (id, )).fetchone())[0]

    def count_users(self):
        with sqlite3.connect(self.db) as db:
            cursor = db.cursor()
            return len(cursor.execute('SELECT * FROM `users`').fetchall())
    



