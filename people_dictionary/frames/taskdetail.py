import tkinter as tk
from tkinter import messagebox, font
from database import get_task_by_id, delete_task

class TaskDetailFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.task_id = None

        # --- フォント設定 ---
        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # --- 中央揃え用フレーム ---
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="タスク詳細", font=title_font).pack(pady=20)
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=120, pady=(0, 30))

        form = tk.Frame(center_frame)
        form.pack(pady=10)

        # --- 変数定義 ---
        self.task_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.partner_var = tk.StringVar()

        # --- タスク名（表示専用） ---
        tk.Label(form, text="タスク", font=entry_font).grid(row=0, column=0, sticky="e")
        tk.Entry(form, textvariable=self.task_var, font=entry_font, width=30, state="readonly").grid(row=0, column=1, pady=5)

        # --- 場所 ---
        tk.Label(form, text="場所", font=entry_font).grid(row=1, column=0, sticky="e")
        tk.Entry(form, textvariable=self.location_var, font=entry_font, width=30, state="readonly").grid(row=1, column=1, pady=5)

        # --- 時間 ---
        tk.Label(form, text="時間", font=entry_font).grid(row=2, column=0, sticky="e")
        tk.Entry(form, textvariable=self.time_var, font=entry_font, width=30, state="readonly").grid(row=2, column=1, pady=5)

        # --- 相手名（表示専用） ---
        tk.Label(form, text="相手", font=entry_font).grid(row=3, column=0, sticky="e")
        tk.Entry(form, textvariable=self.partner_var, font=entry_font, width=30, state="readonly").grid(row=3, column=1, pady=5)

        # --- 備考（Textウィジェット） ---
        tk.Label(form, text="備考", font=entry_font).grid(row=4, column=0, sticky="ne", pady=10)
        self.memo_text = tk.Text(form, width=30, height=5, font=entry_font, state="disabled")
        self.memo_text.grid(row=4, column=1, pady=10)

        # --- ボタンホバー処理 ---
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        button_style = {"font": entry_font, "width": 20, "relief": "raised", "bd": 4, "bg": "#EEEEEE"}

        # --- 編集ボタン ---
        edit_btn = tk.Button(center_frame, text="← 編集", command=self.go_to_edit_frame, **button_style)
        edit_btn.pack(pady=5)
        edit_btn.bind("<Enter>", on_enter)
        edit_btn.bind("<Leave>", on_leave)

        # --- 削除ボタン ---
        delete_btn = tk.Button(center_frame, text="削除", command=self.delete_task_confirm, **button_style)
        delete_btn.pack(pady=5)
        delete_btn.bind("<Enter>", on_enter)
        delete_btn.bind("<Leave>", on_leave)

        # --- 戻るボタン ---
        back_btn = tk.Button(center_frame, text="← 一覧に戻る",
                             command=lambda: controller.show_frame("TaskListFrame"), **button_style)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    def set_task_id(self, task_id):
        self.task_id = task_id
        task = get_task_by_id(task_id)

        if task:
            self.task_var.set(task[1] or "")
            self.location_var.set(task[2] or "")
            self.time_var.set(task[3] or "")
            self.partner_var.set(task[4] or "")

            # 備考の表示
            self.memo_text.config(state="normal")
            self.memo_text.delete("1.0", tk.END)
            self.memo_text.insert("1.0", task[6] or "")
            self.memo_text.config(state="disabled")
        else:
            messagebox.showerror("エラー", "タスク情報の取得に失敗しました。")

    def go_to_edit_frame(self):
        if self.task_id is None:
            messagebox.showerror("エラー", "タスクが選択されていません。")
            return

        edit_frame = self.controller.frames["TaskEditFrame"]
        edit_frame.set_task_id(self.task_id)
        self.controller.show_frame("TaskEditFrame")

    def delete_task_confirm(self):
        if self.task_id is None:
            messagebox.showerror("エラー", "タスクが選択されていません。")
            return

        if messagebox.askyesno("確認", "このタスクを削除してもよろしいですか？"):
            delete_task(self.task_id)
            messagebox.showinfo("削除", "タスクを削除しました。")
            self.controller.frames["TaskListFrame"].refresh_list()
            self.controller.show_frame("TaskListFrame")
