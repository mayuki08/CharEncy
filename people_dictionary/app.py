import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# DB初期化
def init_db():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            job TEXT,
            met_date TEXT,
            memo TEXT
        )
    ''')
    conn.commit()
    conn.close()

# DBに人物追加
def add_person(name, job, met_date, memo):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('INSERT INTO people (name, job, met_date, memo) VALUES (?, ?, ?, ?)',
              (name, job, met_date, memo))
    conn.commit()
    conn.close()

# DBから全データ取得
def get_all_people():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('SELECT id, name, job, met_date FROM people')
    rows = c.fetchall()
    conn.close()
    return rows

# DBで名前検索
def search_people(keyword):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("SELECT id, name, job, met_date FROM people WHERE name LIKE ?", ('%' + keyword + '%',))
    rows = c.fetchall()
    conn.close()
    return rows

# アプリクラス
class PeopleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("人物名鑑アプリ")

        # 入力フィールド
        self.name_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.memo_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        # 入力フォーム
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="名前").grid(row=0, column=0)
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(form_frame, text="職業/肩書き").grid(row=1, column=0)
        tk.Entry(form_frame, textvariable=self.job_var).grid(row=1, column=1)

        tk.Label(form_frame, text="出会った日 (YYYY-MM-DD)").grid(row=2, column=0)
        tk.Entry(form_frame, textvariable=self.date_var).grid(row=2, column=1)

        tk.Label(form_frame, text="メモ").grid(row=3, column=0)
        tk.Entry(form_frame, textvariable=self.memo_var).grid(row=3, column=1)

        tk.Button(form_frame, text="追加", command=self.add_person_gui).grid(row=4, columnspan=2, pady=5)

        # 検索バー
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT)
        tk.Button(search_frame, text="検索", command=self.search).pack(side=tk.LEFT)
        tk.Button(search_frame, text="全て表示", command=self.refresh_list).pack(side=tk.LEFT)

        # 一覧表示（ツリービュー）
        self.tree = ttk.Treeview(self.root, columns=("ID", "名前", "職業", "出会った日"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("名前", text="名前")
        self.tree.heading("職業", text="職業")
        self.tree.heading("出会った日", text="出会った日")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def add_person_gui(self):
        name = self.name_var.get()
        job = self.job_var.get()
        date = self.date_var.get()
        memo = self.memo_var.get()

        if not name:
            messagebox.showwarning("入力エラー", "名前は必須です。")
            return

        add_person(name, job, date, memo)
        self.clear_inputs()
        self.refresh_list()

    def clear_inputs(self):
        self.name_var.set("")
        self.job_var.set("")
        self.date_var.set("")
        self.memo_var.set("")

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for person in get_all_people():
            self.tree.insert('', tk.END, values=person)

    def search(self):
        keyword = self.search_var.get()
        results = search_people(keyword)
        self.tree.delete(*self.tree.get_children())
        for person in results:
            self.tree.insert('', tk.END, values=person)

# 実行
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = PeopleApp(root)
    root.mainloop()