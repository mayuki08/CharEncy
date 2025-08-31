import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk
from database import get_task_by_id, update_task, delete_task, get_all_people
from settings import load_topicbool
from frames.set_customlabel import load_custom_field_settings

class TaskEditFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.task_id = None

        # 入力用変数
        self.task_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.partner_var = tk.StringVar()
        self.memo_text = None
        self.custom_vars = []

        # 相手候補リストを取得（peopleテーブルのnameを取得）
        self.partner_list = self.load_partner_list()

        # フォント設定
        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # 中央寄せ用フレーム
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # タイトル
        tk.Label(center_frame, text="タスク編集", font=title_font).pack(pady=20)
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=80, pady=(0, 50))

        form = tk.Frame(center_frame)
        form.pack(pady=5)

        row = 0
        # タスク名（必須）
        tk.Label(form, text="タスク名 *", font=entry_font, fg="red").grid(row=row, column=0, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.task_var, font=entry_font, width=30).grid(row=row, column=1, pady=10)
        row += 1

        # 場所（常に表示）
        tk.Label(form, text="場所", font=entry_font).grid(row=row, column=0, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.location_var, font=entry_font, width=30).grid(row=row, column=1, pady=10)
        row += 1

        # 時間（常に表示）
        tk.Label(form, text="時間", font=entry_font).grid(row=row, column=0, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.time_var, font=entry_font, width=30).grid(row=row, column=1, pady=10)
        row += 1

        # 相手（常に表示、手入力＆候補選択可）
        tk.Label(form, text="相手", font=entry_font).grid(row=row, column=0, pady=10, sticky="e")
        self.partner_combobox = ttk.Combobox(form, textvariable=self.partner_var, font=entry_font, width=28)
        self.partner_combobox['values'] = self.partner_list
        self.partner_combobox['state'] = 'normal'  # 手入力も可能に
        self.partner_combobox.grid(row=row, column=1, pady=10)
        row += 1

        # メモ（常に表示）
        tk.Label(form, text="メモ", font=entry_font).grid(row=row, column=0, pady=10, sticky="ne")
        self.memo_text = tk.Text(form, width=32, height=5, font=("Arial", 12))
        self.memo_text.grid(row=row, column=1, padx=10, pady=10)
        row += 1

        # カスタム項目（10項目すべて表示）
        self.custom_labeltitles = load_custom_field_settings()["task_custom_labels"]
        self.custom_labels = []

        for i in range(10):
            var = tk.StringVar()
            self.custom_vars.append(var)
            label = tk.Label(form, text=self.custom_labeltitles[i], font=entry_font)
            entry = tk.Entry(form, textvariable=var, font=entry_font, width=30)
            label.grid(row=row, column=0, pady=10, sticky="e")
            entry.grid(row=row, column=1, pady=10)
            self.custom_labels.append(label)
            row += 1

        # ボタンスタイル＆ホバーエフェクト
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        button_style = {"font": entry_font, "width": 20, "relief": "raised", "bd": 4, "bg": "#EEEEEE"}

        save_btn = tk.Button(center_frame, text="編集を保存", command=self.save_changes, **button_style)
        save_btn.pack(pady=5)
        save_btn.bind("<Enter>", on_enter)
        save_btn.bind("<Leave>", on_leave)

        delete_btn = tk.Button(center_frame, text="消去", command=self.delete_task_confirm, **button_style)
        delete_btn.pack(pady=5)
        delete_btn.bind("<Enter>", on_enter)
        delete_btn.bind("<Leave>", on_leave)

        back_btn = tk.Button(center_frame, text="←編集を中断",
                             command=lambda: controller.show_frame("TaskDetailFrame"), **button_style)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    def load_partner_list(self):
        try:
            people = get_all_people()  # [(id, name, ...), ...]
            return [p[1] for p in people if p[1]]  # nameのみ抽出
        except Exception as e:
            messagebox.showerror("DBエラー", f"相手リストの取得に失敗しました。\n{e}")
            return []

    def set_task_id(self, task_id):
        self.task_id = task_id
        task = get_task_by_id(task_id)
        if task:
            self.task_var.set(task[1] or "")
            self.location_var.set(task[2] or "")
            self.time_var.set(task[3] or "")
            self.partner_var.set(task[4] or "")
            if self.memo_text:
                self.memo_text.delete("1.0", tk.END)
                self.memo_text.insert("1.0", task[6] or "")

            customs = task[7:17]
            for i, val in enumerate(customs):
                self.custom_vars[i].set(val or "")
        else:
            messagebox.showerror("エラー", "タスク情報の取得に失敗しました。")

    def save_changes(self):
        if self.task_id is None:
            messagebox.showerror("エラー", "タスクが選択されていません。")
            return

        task_name = self.task_var.get().strip()
        location = self.location_var.get().strip()
        time_str = self.time_var.get().strip()
        partner = self.partner_var.get().strip()
        memo = self.memo_text.get("1.0", "end-1c") if self.memo_text else ""
        custom = [var.get().strip() for var in self.custom_vars]

        if not task_name:
            messagebox.showwarning("入力エラー", "タスク名は必須です。")
            return

        # partner_idは使用せず、partner文字列のみをDBに保存
        update_task(self.task_id, task_name, location, time_str, partner, None, memo, custom)

        messagebox.showinfo("保存完了", "タスク情報を更新しました。")

        if "TaskDetailFrame" in self.controller.frames:
            self.controller.frames["TaskDetailFrame"].set_task_id(self.task_id)
        if "TaskListFrame" in self.controller.frames:
            self.controller.frames["TaskListFrame"].refresh_list()
        self.controller.show_frame("TaskDetailFrame")

    def delete_task_confirm(self):
        if self.task_id is None:
            messagebox.showerror("エラー", "タスクが選択されていません。")
            return

        if messagebox.askyesno("確認", "このタスクを削除してもよろしいですか？"):
            delete_task(self.task_id)
            messagebox.showinfo("削除", "タスクを削除しました。")
            if "TaskListFrame" in self.controller.frames:
                self.controller.frames["TaskListFrame"].refresh_list()
            self.controller.show_frame("TaskListFrame")

