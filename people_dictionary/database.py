import sqlite3

def init_parson_db():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            furigana TEXT,
            grouping TEXT,
            job TEXT,
            met_date TEXT,
            memo TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_person(name, furigana, job, grouping, met_date, memo):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('INSERT INTO people (name, furigana, grouping, job, met_date, memo) VALUES (?, ?, ?, ?, ?, ?)',
              (name, furigana, grouping, job, met_date, memo))
    conn.commit()
    conn.close()

def get_all_people():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('SELECT id, name, furigana, grouping, job, met_date, memo FROM people')
    rows = c.fetchall()
    conn.close()
    return rows

def search_people(keyword):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('SELECT id, name, job, met_date FROM people WHERE name LIKE ?', 
              ('%' + keyword + '%',))
    rows = c.fetchall()
    conn.close()
    return rows

def get_person_by_id(person_id):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('SELECT id, name, furigana, grouping, job, met_date, memo FROM people WHERE id = ?', (person_id,))
    person = c.fetchone()
    conn.close()
    return person

def update_person(person_id, name, furigana, grouping, job, met_date, memo):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("""
        UPDATE people 
        SET name=?, furigana=?, grouping=?, job=?, met_date=?, memo=? 
        WHERE id=?
    """, (name, furigana, grouping, job, met_date, memo, person_id))
    conn.commit()
    conn.close()

def delete_person(person_id):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("DELETE FROM people WHERE id=?", (person_id,))
    conn.commit()
    conn.close()


#タスクリスト関数
def init_task_db():
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            location TEXT,
            time TEXT,
            partner TEXT,
            partner_id INTEGER,
            memo TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_task(task, location="", time="", partner="", partner_id=None, note=""):
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (task, location, time, partner, partner_id, memo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (task, location, time, partner, partner_id, note))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('SELECT id, task, location, time, partner_id, memo FROM tasks')
    rows = c.fetchall()
    conn.close()
    return rows

def get_task_by_id(task_id):
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('SELECT id, task, location, time, partner, partner_id, memo FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    conn.close()
    return task

def search_tasks(keyword):
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute("""
        SELECT id, task, location, time, person_id, memo 
        FROM tasks 
        WHERE title LIKE ? OR location LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))
    rows = c.fetchall()
    conn.close()
    return rows


def update_task(task_id, task, location, time, partner, partner_id, note):
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('''
        UPDATE tasks
        SET task=?, location=?, time=?, partner=?, partner_id=?, memo=?
        WHERE id=?
    ''', (task, location, time, partner, partner_id, note, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()
    conn.close()
