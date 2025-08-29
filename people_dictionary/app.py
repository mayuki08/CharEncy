import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import sqlite3
import os
from PIL import Image, ImageTk

# ------------------ DB初期化 ------------------
def init_db():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    # peopleテーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            job TEXT,
            met_date TEXT,
            memo TEXT,
            profile_image TEXT
        )
    ''')
    # albumsテーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            image_path TEXT,
            caption TEXT,
            FOREIGN KEY(person_id) REFERENCES people(id)
        )
    ''')
    conn.commit()
    conn.close()

# DBに人物追加
def add_person(name, job, met_date, memo, image_path):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('INSERT INTO people (name, job, met_date, memo, profile_image) VALUES (?, ?, ?, ?, ?)',
              (name, job, met_date, memo, image_path))
    conn.commit()
    conn.close()

# DBから全データ取得
def get_all_people():
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute('SELECT id, name, job, met_date, profile_image FROM people')
    rows = c.fetchall()
    conn.close()
    return rows

# 名前検索
def search_people(keyword):
    conn = sqlite3.connect('people.db')
    c = conn.cursor()
    c.execute("SELECT id, name, job, met_date, profile_image FROM people WHERE name LIKE ?", ('%' + keyword + '%',))
    rows = c.fetchall()
    conn.close()
    return rows

# ------------------ メインアプリ ------------------
class PeopleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("人物名鑑アプリ")
        self.images = {}  # Treeview用の画像保持

        # 入力フィールド
        self.name_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.memo_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.image_path_var = tk.StringVar()

        self.build_ui()
        self.refresh_list()

    # ------------------ UI構築 ------------------
    def build_ui(self):
        # スタイル設定
        style = ttk.Style()
        style.configure("Treeview", rowheight=60)

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
        tk.Label(form_frame, text="プロフィール画像").grid(row=4, column=0)
        tk.Button(form_frame, text="画像選択", command=self.select_profile_image).grid(row=4, column=1)
        tk.Button(form_frame, text="追加", command=self.add_person_gui).grid(row=5, columnspan=2, pady=5)

        # 検索バー
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT)
        tk.Button(search_frame, text="検索", command=self.search).pack(side=tk.LEFT)
        tk.Button(search_frame, text="全て表示", command=self.refresh_list).pack(side=tk.LEFT)

        # 一覧表示
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "名前", "職業", "出会った日"),
            show="tree headings",
            yscrollcommand=scrollbar.set
        )

        self.tree.heading("#0", text="プロフィール画像")
        self.tree.heading("ID", text="ID")
        self.tree.heading("名前", text="名前")
        self.tree.heading("職業", text="職業")
        self.tree.heading("出会った日", text="出会った日")

        self.tree.column("#0", width=60, anchor="center")
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("名前", width=120, anchor="w")
        self.tree.column("職業", width=100, anchor="w")
        self.tree.column("出会った日", width=100, anchor="center")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        tk.Button(self.root, text="アルバムを見る", command=self.open_album).pack(pady=5)

    # ------------------ データ操作 ------------------
    def select_profile_image(self):
        path = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg")])
        if path:
            self.image_path_var.set(path)

    def add_person_gui(self):
        name = self.name_var.get()
        job = self.job_var.get()
        date = self.date_var.get()
        memo = self.memo_var.get()
        image_path = self.image_path_var.get()
        if not name:
            messagebox.showwarning("入力エラー", "名前は必須です。")
            return
        add_person(name, job, date, memo, image_path)
        self.clear_inputs()
        self.refresh_list()

    def clear_inputs(self):
        self.name_var.set("")
        self.job_var.set("")
        self.date_var.set("")
        self.memo_var.set("")
        self.image_path_var.set("")

    # ------------------ Treeview更新 ------------------
    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        self.images = {}
        people = get_all_people()
        for pid, name, job, date, image_path in people:
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail((60, 60))
                photo = ImageTk.PhotoImage(img)
                self.images[pid] = photo
                self.tree.insert('', tk.END, image=photo, text="", values=(pid, name, job, date))
            else:
                self.tree.insert('', tk.END, text="", values=(pid, name, job, date))

    def search(self):
        keyword = self.search_var.get()
        self.tree.delete(*self.tree.get_children())
        self.images = {}
        people = search_people(keyword)
        for pid, name, job, date, image_path in people:
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail((30, 30))
                photo = ImageTk.PhotoImage(img)
                self.images[pid] = photo
                self.tree.insert('', tk.END, image=photo, values=(pid, name, job, date, ""))
            else:
                self.tree.insert('', tk.END, values=(pid, name, job, date, "なし"))

    # ------------------ アルバム ------------------
    def open_album(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("選択エラー", "人物を選択してください。")
            return
        person_id = self.tree.item(selected[0], "values")[0]
        album_win = tk.Toplevel(self.root)
        album_win.title("アルバム")
        tk.Button(album_win, text="写真追加", command=lambda: self.add_photo(person_id, album_win)).pack()
        self.show_photos(person_id, album_win)

    def add_photo(self, person_id, win):
        filepath = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg")])
        if filepath:
            conn = sqlite3.connect('people.db')
            c = conn.cursor()
            c.execute("INSERT INTO albums (person_id, image_path) VALUES (?, ?)", (person_id, filepath))
            conn.commit()
            conn.close()
            self.show_photos(person_id, win)
    def show_photos(self, person_id, win):
        # 既存の画像ラベルを削除
        for widget in win.pack_slaves():
            if isinstance(widget, tk.Label) and hasattr(widget, "image"):
                widget.destroy()

        conn = sqlite3.connect('people.db')
        c = conn.cursor()
        c.execute("SELECT image_path FROM albums WHERE person_id=?", (person_id,))
        photos = c.fetchall()
        conn.close()

        for path, in photos:
            try:
                img = Image.open(path)
                img.thumbnail((200, 200))  # 少し大きめに表示してもOK
                photo = ImageTk.PhotoImage(img)

                lbl = tk.Label(win, image=photo)
                lbl.image = photo  # 参照保持しないと消える

                # 🔽 これでウィンドウの中央に表示
                lbl.place(relx=0.5, rely=0.5, anchor="center")

            except Exception as e:
                print("画像読み込み失敗:", e)

  

# ------------------ 実行 ------------------
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = PeopleApp(root)
    root.mainloop()
