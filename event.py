import datetime
import sqlite3
class Event:
    def __init__(self, lesson, post_type, description, date):
        self.lesson = lesson
        self.post_type = post_type
        self.description = description
        self.strdate = date
        self.date = datetime.datetime.now()
