#frames/task_register.py
import tkinter as tk
from tkinter import messagebox, font, ttk
from database import add_task

class TaskRegisterFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # 入力用変数
        self.task_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.partner_var = tk.StringVar()
        
        # 中央寄せ用フレーム
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # タイトル
        tk.Label(center_frame, text="タスク登録", font=title_font).pack(pady=20)

        # 横線
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=80, pady=(0, 50))

        form = tk.Frame(center_frame)
        form.pack(pady=5)

        # タスク名
        tk.Label(form, text="タスク *", font=entry_font, fg="red").grid(row=0, column=0, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.task_var, font=entry_font).grid(row=0, column=1, pady=10)

        # 場所
        tk.Label(form, text="場所", font=entry_font).grid(row=1, column=0, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.location_var, font=entry_font).grid(row=1, column=1, pady=10)

        # 時間
        tk.Label(form, text="時間", font=entry_font).grid(row=2, column=0, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.time_var, font=entry_font).grid(row=2, column=1, pady=10)

        # 相手
        tk.Label(form, text="相手", font=entry_font).grid(row=3, column=0, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.partner_var, font=entry_font).grid(row=3, column=1, pady=10)

        # メモ欄
        tk.Label(form, text="メモ", font=entry_font).grid(row=4, column=0, pady=10, sticky="ne")
        self.memo_text = tk.Text(form, width=32, height=5, font=("Arial", 12))
        self.memo_text.grid(row=4, column=1, padx=10, pady=10)

        # ホバーエフェクト
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        # 追加ボタン
        add_btn = tk.Button(center_frame, text="追加", command=self.add_task_gui,
                            font=entry_font, relief="raised", bd=4, bg="#EEEEEE")
        add_btn.pack(pady=10)
        add_btn.bind("<Enter>", on_enter)
        add_btn.bind("<Leave>", on_leave)

        # 戻るボタン
        back_btn = tk.Button(center_frame, text="← メニューに戻る",
                             command=lambda: controller.show_frame("MenuFrame"),
                             font=entry_font, relief="raised", bd=4, bg="#EEEEEE")
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    def add_task_gui(self):
        task = self.task_var.get()
        location = self.location_var.get()
        time = self.time_var.get()
        partner = self.partner_var.get()
        memo = self.memo_text.get("1.0", "end-1c")

        if not task:
            messagebox.showwarning("入力エラー", "タスク名は必須です。")
            return

        # DBに追加（add_task関数は引数がこの順番・内容である前提）
        add_task(task, location, time, partner, memo)

        # フィールドクリア
        self.task_var.set("")
        self.location_var.set("")
        self.time_var.set("")
        self.partner_var.set("")
        self.memo_text.delete("1.0", "end")

        messagebox.showinfo("登録成功", "タスクを登録しました。")

        # ListFrameの更新
        if "TaskListFrame" in self.controller.frames:
            self.controller.frames["TaskListFrame"].refresh_list()
