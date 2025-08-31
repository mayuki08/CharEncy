import tkinter as tk
from tkinter import messagebox, font, ttk
import sqlite3
from database import add_task
from settings import load_topicbool
from frames.set_customlabel import load_custom_field_settings

class TaskRegisterFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.topic_control = load_topicbool()
        self.custom_labeltitles = load_custom_field_settings()["task_custom_labels"]

        # 入力用変数
        self.task_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.partner_var = tk.StringVar()
        self.custom_vars = [tk.StringVar() for _ in range(10)]

        # people.db から名前リストとIDマップを読み込み
        self.people_list, self.name_to_id = self.load_people()

        # 中央寄せ用フレーム
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # タイトル
        tk.Label(center_frame, text="タスク登録", font=title_font).pack(pady=20)

        # 横線
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=80, pady=(0, 50))

        self.form_frame = tk.Frame(center_frame)
        self.form_frame.pack(pady=5)

        self.custom_labels = []
        self.memo_text = None  # 初期化

        self.refresh_fields()  # ← 初回描画

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

    def load_people(self):
        """
        people.db から (id, name) を取得して
        - 名前リスト
        - 名前→IDの辞書
        を返す
        """
        try:
            conn = sqlite3.connect('people.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM people ORDER BY name")
            rows = cursor.fetchall()
            conn.close()
            people_list = [row[1] for row in rows]
            name_to_id = {row[1]: row[0] for row in rows}
            return people_list, name_to_id
        except Exception as e:
            messagebox.showerror("DBエラー", f"people.db の読み込みに失敗しました。\n{e}")
            return [], {}

    def refresh_fields(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        self.topic_control = load_topicbool()
        self.custom_labeltitles = load_custom_field_settings()["task_custom_labels"]
        entry_font = font.Font(family="Arial", size=15)
        row = 0 

        # タスク名（常に表示）
        tk.Label(self.form_frame, text="タスク *", font=entry_font, fg="red").grid(row=row, column=0, pady=10, sticky="e")
        tk.Entry(self.form_frame, textvariable=self.task_var, font=entry_font).grid(row=row, column=1, pady=10)
        row += 1

        # 場所
        if self.topic_control["tnormalcontrol"][0]:
            tk.Label(self.form_frame, text="場所", font=entry_font).grid(row=row, column=0, pady=10, sticky="e")
            tk.Entry(self.form_frame, textvariable=self.location_var, font=entry_font).grid(row=row, column=1, pady=10)
            row += 1

        # 時間
        if self.topic_control["tnormalcontrol"][1]:
            tk.Label(self.form_frame, text="時間", font=entry_font).grid(row=row, column=0, pady=10, sticky="e")
            tk.Entry(self.form_frame, textvariable=self.time_var, font=entry_font).grid(row=row, column=1, pady=10)
            row += 1

        # 相手（コンボボックスで people.db の名前リストから選択可能）
        if self.topic_control["tnormalcontrol"][2]:
            tk.Label(self.form_frame, text="相手", font=entry_font).grid(row=row, column=0, pady=10, sticky="e")
            partner_combo = ttk.Combobox(self.form_frame, textvariable=self.partner_var, font=entry_font)
            partner_combo['values'] = self.people_list
            partner_combo.grid(row=row, column=1, pady=10)
            row += 1

        # メモ
        if self.topic_control["tnormalcontrol"][3]:
            tk.Label(self.form_frame, text="メモ", font=entry_font).grid(row=row, column=0, pady=10, sticky="ne")
            self.memo_text = tk.Text(self.form_frame, width=32, height=5, font=("Arial", 12))
            self.memo_text.grid(row=row, column=1, padx=10, pady=10)
            row += 1
        else:
            self.memo_text = None

        # カスタム項目
        self.custom_labels = []
        for i in range(10):
            if self.topic_control["tcustomcontrol"][i]:
                label = tk.Label(self.form_frame, text=self.custom_labeltitles[i], font=entry_font)
                entry = tk.Entry(self.form_frame, textvariable=self.custom_vars[i], font=entry_font)
                label.grid(row=row, column=0, pady=10, sticky="e")
                entry.grid(row=row, column=1, pady=10)
                self.custom_labels.append(label)
                row += 1
            else:
                self.custom_labels.append(None)

    def add_task_gui(self):
        task = self.task_var.get()
        location = self.location_var.get()
        time = self.time_var.get()
        partner = self.partner_var.get()
        memo = self.memo_text.get("1.0", "end-1c") if self.memo_text else ""
        custom = [var.get() for var in self.custom_vars]

        if not task:
            messagebox.showwarning("入力エラー", "タスク名は必須です。")
            return

        # partner名からpartner_idを取得（存在しなければNone）
        partner_id = self.name_to_id.get(partner, None)

        add_task(task, location, time, partner, partner_id, memo, *custom)

        # フィールドクリア
        self.task_var.set("")
        self.location_var.set("")
        self.time_var.set("")
        self.partner_var.set("")
        for var in self.custom_vars:
            var.set("")
        if self.memo_text:
            self.memo_text.delete("1.0", "end")

        messagebox.showinfo("登録成功", "タスクを登録しました。")

        if "TaskListFrame" in self.controller.frames:
            self.controller.frames["TaskListFrame"].refresh_list()
