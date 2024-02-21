import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
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

    def __del__(self):
        self.conn.close()