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
import datetime
from . import AppData
import logging

class Database:
    def __init__(self, db_file):
        try:
            app_data = AppData("lakshapp", db_file)
            self.database_path = app_data.get_file_path()
            self.conn = sqlite3.connect(self.database_path)
            logging.info(f"Connected to database: {self.database_path}")
        except:
            logging.critical(f"Couldn't connect to database. Please check file permissions.")
            exit(1)
        self.conn.row_factory = sqlite3.Row  # Use Row factory to fetch rows as dictionaries
        self.cursor = self.conn.cursor()

    def create_table(self):
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
        self.conn.commit()
        self.cursor.execute('''SELECT COUNT(*) FROM tasks''')
        row_count = self.cursor.fetchone()[0]
        if row_count == 0:
            today = datetime.datetime.today()
            initial_rows = [
                ("Set up your first workspace", "My Amazing Project", "Setting up LakshApp", False, "HIGH"),
                ("Create a new Project using + Button", "My Amazing Project", "Setting up LakshApp", False, "HIGH"),
                ("Edit an Existing Workspace", "My Amazing Project", "Setting up LakshApp", False, "HIGH"),
                ("View your Progress", "My Amazing Project", "Setting up LakshApp", False, "HIGH"),
                ("Create live sessions", "My Amazing Project", "More features", False, "HIGH"),
                ("Read motivational quotes", "My Amazing Project", "More features", False, "HIGH"),
                ("Listen to some ambient music", "My Amazing Project", "More features", False, "HIGH"),
                ("Ready to go! Start grinding!!!", "My Amazing Project", "More features", False, "HIGH"),
            ]
            values = [
                (*row, today.day, today.month, today.year)
                for row in initial_rows
            ]
            self.cursor.executemany("INSERT INTO tasks (task_name, project, list, status, priority, day, month, year)"
                                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
            self.conn.commit()

    def add_todo(self, task_name, mylist, project, status, priority, day, month, year):
        self.cursor.execute('''INSERT INTO tasks (task_name, list, project, status, priority, day, month, year)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (task_name, mylist, project, status, priority, day, month, year))
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_todo(self, task_id):
        self.cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def delete_list(self, project, mylist):
        self.cursor.execute('''DELETE FROM tasks WHERE project = ? AND list = ?''', (project, mylist))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def delete_project(self, project):
        self.cursor.execute('''DELETE FROM tasks WHERE project = ?''', (project,))
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_all_todos(self):
        self.cursor.execute('''DELETE FROM tasks''')
        self.conn.commit()
        return self.cursor.lastrowid
        
    def update_todo_status(self, task_id, status):
        self.cursor.execute('''UPDATE tasks SET status = ? WHERE id = ?''', (status, task_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_project_name(self, old_name, new_name):
        self.cursor.execute('''UPDATE tasks SET project = ? WHERE project = ?''', (new_name, old_name))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_list_name(self, project_name, old_name, new_name):
        self.cursor.execute('''UPDATE tasks SET list = ? WHERE list = ? AND project = ?''', (new_name, old_name, project_name))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def search_todo_by_project(self, project):
        self.cursor.execute('''SELECT * FROM tasks WHERE project = ?''', (project,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def search_todo_by_list(self, mylist, project):
        self.cursor.execute('''SELECT * FROM tasks WHERE list = ? AND project = ?''', (mylist, project))
        return [dict(row) for row in self.cursor.fetchall()]

    def search_todo_by_id(self, task_id):
        self.cursor.execute('''SELECT * FROM tasks WHERE id = ?''', (task_id,))
        return dict(self.cursor.fetchone())
    
    def check_todo_by_id(self, task_id):
        self.cursor.execute('''SELECT * FROM tasks WHERE id = ?''', (task_id,))
        return bool(self.cursor.fetchone())

    def get_completed_tasks(self):
        self.cursor.execute('''SELECT * FROM tasks WHERE status = ?''', (True,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_total_tasks(self):
        self.cursor.execute('''SELECT * FROM tasks''')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_completed_tasks_count(self):
        self.cursor.execute('''SELECT COUNT(*) FROM tasks WHERE status = ?''', (True,))
        return self.cursor.fetchone()[0]
    
    def get_total_tasks_count(self):
        self.cursor.execute('''SELECT COUNT(*) FROM tasks''')
        return self.cursor.fetchone()[0]

    def get_total_projects(self):
        dbget = self.get_total_tasks()
        projectvalues = []
        for val in dbget:
            if val['project'] not in projectvalues:
                projectvalues.append(val['project'])
        return projectvalues
                
    def __del__(self):
        self.conn.close()