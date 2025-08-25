# frames/search.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import search_people, get_all_people

class SearchFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.search_var = tk.StringVar()

        tk.Label(self, text="人物検索", font=("Arial", 16)).pack(pady=10)

        search_box = tk.Frame(self)
        search_box.pack(pady=5)

        tk.Entry(search_box, textvariable=self.search_var).pack(side=tk.LEFT)
        tk.Button(search_box, text="検索", command=self.search).pack(side=tk.LEFT)
        tk.Button(search_box, text="全て表示", command=self.refresh_list).pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=("ID", "名前", "職業", "出会った日"), show="headings")
        for col in ("ID", "名前", "職業", "出会った日"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        tk.Button(self, text="選択した人物の詳細を見る", command=self.show_detail).pack(pady=5)
        tk.Button(self, text="← メニューに戻る", command=lambda: controller.show_frame("MenuFrame")).pack()

        self.refresh_list()

    def search(self):
        keyword = self.search_var.get()
        results = search_people(keyword)
        self.tree.delete(*self.tree.get_children())
        for person in results:
            self.tree.insert('', tk.END, values=person)

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for person in get_all_people():
            self.tree.insert('', tk.END, values=person)

    def show_detail(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("選択エラー", "人物を選択してください。")
            return

        person_id = self.tree.item(selected[0])['values'][0]
        self.controller.frames["DetailFrame"].set_person_id(person_id)
        self.controller.show_frame("DetailFrame")
