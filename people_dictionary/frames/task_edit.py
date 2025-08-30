#frames/task_edit.py
import tkinter as tk
from tkinter import messagebox, font, ttk
from database import get_task_by_id, update_task, delete_task

class TaskEditFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.task_id = None

        # --- フォント設定 ---
        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="タスク編集", font=title_font).pack(pady=20)
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=120, pady=(0, 30))

        form = tk.Frame(center_frame)
        form.pack(pady=10)

        # --- 変数定義 ---
        self.task_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.partner_var = tk.StringVar()
        self.memo_var = tk.StringVar()
        self.partner_id = None  # DB用（非表示）

        # --- タスク名 ---
        tk.Label(form, text="タスク", font=entry_font).grid(row=0, column=0, sticky="e")
        tk.Entry(form, textvariable=self.task_var, font=entry_font, width=30).grid(row=0, column=1, pady=5)

        # --- 場所 ---
        tk.Label(form, text="場所", font=entry_font).grid(row=1, column=0, sticky="e")
        tk.Entry(form, textvariable=self.location_var, font=entry_font, width=30).grid(row=1, column=1, pady=5)

        # --- 時間 ---
        tk.Label(form, text="時間", font=entry_font).grid(row=2, column=0, sticky="e")
        tk.Entry(form, textvariable=self.time_var, font=entry_font, width=30).grid(row=2, column=1, pady=5)

        # --- 相手（名前） ---
        tk.Label(form, text="相手", font=entry_font).grid(row=3, column=0, sticky="e")
        tk.Entry(form, textvariable=self.partner_var, font=entry_font, width=30).grid(row=3, column=1, pady=5)

        # --- 備考（メモ） ---
        tk.Label(form, text="備考", font=entry_font).grid(row=4, column=0, sticky="ne", pady=10)
        self.memo_text = tk.Text(form, width=30, height=5, font=entry_font)
        self.memo_text.grid(row=4, column=1, pady=10)

        # --- ボタンホバー処理 ---
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        button_style = {"font": entry_font, "width": 20, "relief": "raised", "bd": 4}

        # --- 保存ボタン ---
        save_btn = tk.Button(center_frame, text="編集を保存", command=self.save_changes, **button_style)
        save_btn.pack(pady=5)
        save_btn.bind("<Enter>", on_enter)
        save_btn.bind("<Leave>", on_leave)

        # --- 削除ボタン ---
        delete_btn = tk.Button(center_frame, text="消去", command=self.delete_task_confirm, **button_style)
        delete_btn.pack(pady=5)
        delete_btn.bind("<Enter>", on_enter)
        delete_btn.bind("<Leave>", on_leave)

        # --- 戻るボタン ---
        back_btn = tk.Button(center_frame, text="← 編集を中断",
                             command=lambda: controller.show_frame("TaskDetailFrame"), **button_style)
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
            self.partner_id = task[5]  # DBから読み込み（非表示）

            self.memo_text.delete("1.0", tk.END)
            self.memo_text.insert("1.0", task[6] or "")
        else:
            messagebox.showerror("エラー", "タスク情報の取得に失敗しました。")

    def save_changes(self):
        if self.task_id is None:
            messagebox.showerror("エラー", "タスクが選択されていません。")
            return

        memo = self.memo_text.get("1.0", tk.END).strip()

        update_task(
            self.task_id,
            self.task_var.get(),
            self.location_var.get(),
            self.time_var.get(),
            self.partner_var.get(),
            self.partner_id,
            memo
        )

        messagebox.showinfo("完了", "編集内容を保存しました。")
        self.controller.frames["TaskListFrame"].refresh_list()
        self.controller.show_frame("TaskDetailFrame")

    def delete_task_confirm(self):
        if self.task_id is None:
            messagebox.showerror("エラー", "タスクが選択されていません。")
            return

        if messagebox.askyesno("確認", "このタスクを削除してもよろしいですか？"):
            delete_task(self.task_id)
            messagebox.showinfo("削除", "タスクを削除しました。")
            self.controller.frames["TaskListFrame"].refresh_list()
            self.controller.show_frame("TaskListFrame")
