"""
LakshApp - Stay Focused and Motivated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced TO-DOs and Project Management integrated with Live Sessions, Music and more for Focus and Productivity

Author: DevInfinix
Copyright: (c) 2024-present DevInfinix
License: Apache-2.0
Version: 1.0.1
"""

import sqlite3
import logging

class Database:
    def __init__(self, db_file):
        self.cursor = self.conn.cursor()

    def create_todo_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                task_name TEXT,
                                list TEXT,
                                project TEXT,
                                status BOOLEAN,
                                priority TEXT,
                                day INTEGER,
                                month INTEGER,
                                year INTEGER
                            )''')
        
            
    def create_pomodoro_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pomodoro (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                day INTEGER,
                                month INTEGER,
                                year INTEGER
                            )''')
        self.conn.commit()
