# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            furigana TEXT,
            job TEXT,
            met_date TEXT,
            memo TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_person(name, furigana, job, met_date, memo):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('INSERT INTO people (name, furigana, job, met_date, memo) VALUES (?, ?, ?, ?, ?)',
              (name, furigana, job, met_date, memo))
    conn.commit()
    conn.close()

def get_all_people():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('SELECT id, name, furigana, job, met_date FROM people')
    rows = c.fetchall()
    conn.close()
    return rows

def search_people(keyword):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("SELECT id, name, job, met_date FROM people WHERE name LIKE ?", 
              ('%' + keyword + '%',))
    rows = c.fetchall()
    conn.close()
    return rows

def get_person_by_id(person_id):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("SELECT id, name, furigana, job, met_date, memo FROM people WHERE id = ?", (person_id,))
    person = c.fetchone()
    conn.close()
    return person

def update_person(person_id, name, furigana, job, met_date, memo):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("""
        UPDATE people SET name=?, furigana=?, job=?, met_date=?, memo=? WHERE id=?
    """, (name, furigana, job, met_date, memo, person_id))
    conn.commit()
    conn.close()

def delete_person(person_id):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("DELETE FROM people WHERE id=?", (person_id,))
    conn.commit()
    conn.close()