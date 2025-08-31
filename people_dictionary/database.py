#database.py
import sqlite3

# ----------------------------
# 人物テーブル（people）関連
# ----------------------------

def init_person_db():
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
            memo TEXT,
            profile_image TEXT,
            custom1 TEXT,
            custom2 TEXT,
            custom3 TEXT,
            custom4 TEXT,
            custom5 TEXT,
            custom6 TEXT,
            custom7 TEXT,
            custom8 TEXT,
            custom9 TEXT,
            custom10 TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_person(name, furigana, grouping, job, met_date, memo, image_path, *customs):
    customs = customs or [""] * 10
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO people (
            name, furigana, grouping, job, met_date, memo, profile_image,
              custom1, custom2, custom3, custom4, custom5,
              custom6, custom7, custom8, custom9, custom10
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, furigana, grouping, job, met_date, memo, image_path, *customs))
    conn.commit()
    conn.close()

def get_all_people():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, name, furigana, grouping, job, met_date, memo, profile_image,
               custom1, custom2, custom3, custom4, custom5,
               custom6, custom7, custom8, custom9, custom10
        FROM people
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def get_person_by_id(person_id):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, name, furigana, grouping, job, met_date, memo, profile_image,
               custom1, custom2, custom3, custom4, custom5,
               custom6, custom7, custom8, custom9, custom10
        FROM people WHERE id = ?
    ''', (person_id,))
    person = c.fetchone()
    conn.close()
    return person

def update_person(person_id, name, furigana, grouping, job, met_date, memo, image_path, *customs):
    customs = customs or [""] * 10
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        UPDATE people SET
            name=?, furigana=?, grouping=?, job=?, met_date=?, memo=?, profile_image=?,
            custom1=?, custom2=?, custom3=?, custom4=?, custom5=?,
            custom6=?, custom7=?, custom8=?, custom9=?, custom10=?
        WHERE id=?
    ''', (name, furigana, grouping, job, met_date, memo, image_path, *customs, person_id))
    conn.commit()
    conn.close()

def delete_person(person_id):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('DELETE FROM people WHERE id=?', (person_id,))
    conn.commit()
    conn.close()

def search_people(keyword):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, name, job, met_date FROM people
        WHERE name LIKE ? OR job LIKE ? OR memo LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    rows = c.fetchall()
    conn.close()
    return rows

# ----------------------------
# タスクテーブル（tasks）関連
# ----------------------------

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
            memo TEXT,
            custom1 TEXT,
            custom2 TEXT,
            custom3 TEXT,
            custom4 TEXT,
            custom5 TEXT,
            custom6 TEXT,
            custom7 TEXT,
            custom8 TEXT,
            custom9 TEXT,
            custom10 TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_task(task, location="", time="", partner="", partner_id=None, memo="", *customs):
    customs = customs or [""] * 10
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (
            task, location, time, partner, partner_id, memo,
            custom1, custom2, custom3, custom4, custom5,
            custom6, custom7, custom8, custom9, custom10
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (task, location, time, partner, partner_id, memo, *customs))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, task, location, time, partner, partner_id, memo,
               custom1, custom2, custom3, custom4, custom5,
               custom6, custom7, custom8, custom9, custom10
        FROM tasks
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def get_task_by_id(task_id):
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, task, location, time, partner, partner_id, memo,
               custom1, custom2, custom3, custom4, custom5,
               custom6, custom7, custom8, custom9, custom10
        FROM tasks WHERE id = ?
    ''', (task_id,))
    task = c.fetchone()
    conn.close()
    return task

def update_task(task_id, task, location, time, partner, partner_id, memo, customs=None):
    customs = customs or [""] * 10
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('''
        UPDATE tasks SET
            task=?, location=?, time=?, partner=?, partner_id=?, memo=?,
            custom1=?, custom2=?, custom3=?, custom4=?, custom5=?,
            custom6=?, custom7=?, custom8=?, custom9=?, custom10=?
        WHERE id=?
    ''', (task, location, time, partner, partner_id, memo, *customs, task_id))
    conn.commit()
    conn.close()
def delete_task(task_id):
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()
    conn.close()

def search_tasks(keyword):
    conn = sqlite3.connect('tasklist.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, task, location, time, partner, partner_id, memo,
               custom1, custom2, custom3, custom4, custom5,
               custom6, custom7, custom8, custom9, custom10
        FROM tasks
        WHERE task LIKE ? OR location LIKE ? OR memo LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    rows = c.fetchall()
    conn.close()
    return rows

