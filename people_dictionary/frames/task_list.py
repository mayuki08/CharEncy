import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_tasks, search_tasks, get_person_by_id  # まとめてimport

class TaskListFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="タスク一覧（日付順）", font=("Arial", 16)).pack(pady=10)

        # 検索バー
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)

        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT)
        tk.Button(search_frame, text="検索", command=self.search).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="全件表示", command=self.refresh_list).pack(side=tk.LEFT)

        # Treeview（一覧）
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "タスク", "場所", "時間", "相手", "備考"),
            show="headings"
        )
        for col in ("ID", "タスク", "場所", "時間", "相手", "備考"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # ボタン類
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
        item = self.tree.item(selected[0])
        values = item['values']

        # グループ行は無視（ID列が文字列の場合グループ）
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
        self.display_grouped(tasks)

    def refresh_list(self):
        tasks = get_all_tasks()
        self.display_grouped(tasks)

    def display_grouped(self, tasks):
        self.tree.delete(*self.tree.get_children())
        # 日付順にソート、空の日付は末尾
        tasks.sort(key=lambda x: (x[3] if x[3] else "9999-99-99"))

        grouped = {}
        no_date = []

        for task in tasks:
            date = task[3]  # timeカラムを日付として使用
            if date:
                grouped.setdefault(date, []).append(task)
            else:
                no_date.append(task)

        # 各日付でグループ表示
        for date, group_tasks in grouped.items():
            self.tree.insert('', 'end', values=(f"--- {date} ---", "", "", "", "", ""), tags=("group",))
            for task in group_tasks:
                self.tree.insert('', 'end', values=self.format_task_row(task))

        # 日付がないタスク
        if no_date:
            self.tree.insert('', 'end', values=("--- 日付未設定 ---", "", "", "", "", ""), tags=("group",))
            for task in no_date:
                self.tree.insert('', 'end', values=self.format_task_row(task))

        self.tree.tag_configure("group", background="#f0f0f0", font=("Arial", 10, "bold"))


    def format_task_row(self, task):
        # taskは17カラムある
        task_id = task[0]
        title = task[1]
        location = task[2]
        date = task[3]  # ここはtimeカラムだと思いますが、あなたの用途に合わせて調整してください
        person_id = task[5]
        memo = task[6]

        person_name = ""
        if person_id:
            person = get_person_by_id(person_id)
            if person:
                person_name = person[1]

        return (task_id, title, location, date, person_name, memo)

