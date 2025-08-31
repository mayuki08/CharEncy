import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_tasks, search_tasks, get_person_by_id

class TaskListFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="タスク一覧", font=("Arial", 16)).pack(pady=10)

        # 検索バー
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT)
        tk.Button(search_frame, text="検索", command=self.search).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="全件表示", command=self.refresh_list).pack(side=tk.LEFT)

        # Treeview & scrollbar
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", rowheight=25)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "タスク", "場所", "時間", "相手", "備考"), show="headings")
        for col in ("ID", "タスク", "場所", "時間", "相手", "備考"):
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=0, stretch=False)  # ← ID列は非表示
            else:
                self.tree.column(col, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # ボタン
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="選択したタスクの詳細を見る", command=self.show_detail).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="← メニューに戻る", command=lambda: controller.show_frame("MenuFrame")).pack(side=tk.LEFT)

        self.refresh_list()

    def show_detail(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("選択エラー", "タスクを選択してください。")
            return
        values = self.tree.item(selected[0])['values']
        if not isinstance(values[0], int):
            messagebox.showinfo("情報", "タスクを選択してください。")
            return
        task_id = values[0]
        self.controller.frames["TaskDetailFrame"].set_task_id(task_id)
        self.controller.show_frame("TaskDetailFrame")

    def search(self):
        keyword = self.search_var.get()
        if not keyword:
            messagebox.showinfo("検索", "キーワードを入力してください。")
            return
        tasks = search_tasks(keyword)
        self.display_tasks(tasks)

    def refresh_list(self):
        tasks = get_all_tasks()
        self.display_tasks(tasks)

    def display_tasks(self, tasks):
        self.tree.delete(*self.tree.get_children())
        # ID順でソート
        tasks.sort(key=lambda x: x[0])
        for t in tasks:
            self.tree.insert('', 'end', values=self.format_task_row(t))

    def format_task_row(self, task):
        task_id = task[0]
        title = task[1]
        location = task[2]
        date = task[3]  # timeカラム
        memo = task[6]
        partner_name = task[4]  # デフォルトはpartnerカラム

        person_id = task[5]
        if person_id:
            person = get_person_by_id(person_id)
            if person:
                partner_name = person[1]  # 人物名で置き換え

        return (task_id, title, location, date, partner_name or "", memo)
