import tkinter as tk
from tkinter import messagebox, font

from database import get_task_by_id, update_task, delete_task

class TaskEditFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.task_id = None

        # --- フォント設定 ---
        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # スクロール対応（optional）
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 中央フレーム代わりにスクロールフレームを使用
        tk.Label(scroll_frame, text="タスク編集", font=title_font).pack(pady=20)
        tk.Frame(scroll_frame, height=3, bg="black").pack(fill="x", padx=120, pady=(0, 30))

        form = tk.Frame(scroll_frame)
        form.pack(pady=10)

        # --- 変数定義 ---
        self.task_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.partner_var = tk.StringVar()
        self.memo_text = None
        self.custom_vars = [tk.StringVar() for _ in range(10)]
        self.partner_id = None  # DB用（非表示）

        labels = ["タスク", "場所", "時間", "相手", "備考"]
        # 標準4項目＋備考(Text)作成
        tk.Label(form, text=labels[0], font=entry_font).grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.task_var, font=entry_font, width=30).grid(row=0, column=1, pady=5)

        tk.Label(form, text=labels[1], font=entry_font).grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.location_var, font=entry_font, width=30).grid(row=1, column=1, pady=5)

        tk.Label(form, text=labels[2], font=entry_font).grid(row=2, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.time_var, font=entry_font, width=30).grid(row=2, column=1, pady=5)

        tk.Label(form, text=labels[3], font=entry_font).grid(row=3, column=0, sticky="e", pady=5)
        tk.Entry(form, textvariable=self.partner_var, font=entry_font, width=30).grid(row=3, column=1, pady=5)

        tk.Label(form, text=labels[4], font=entry_font).grid(row=4, column=0, sticky="ne", pady=10)
        self.memo_text = tk.Text(form, width=30, height=5, font=entry_font)
        self.memo_text.grid(row=4, column=1, pady=10)

        # カスタム10項目の追加
        for i in range(10):
            tk.Label(form, text=f"カスタム{i+1}", font=entry_font).grid(row=5+i, column=0, sticky="e", pady=5)
            tk.Entry(form, textvariable=self.custom_vars[i], font=entry_font, width=30).grid(row=5+i, column=1, pady=5)

        # --- ボタンホバー処理 ---
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        button_style = {"font": entry_font, "width": 20, "relief": "raised", "bd": 4, "bg": "#EEEEEE"}

        # --- 保存ボタン ---
        save_btn = tk.Button(scroll_frame, text="編集を保存", command=self.save_changes, **button_style)
        save_btn.pack(pady=5)
        save_btn.bind("<Enter>", on_enter)
        save_btn.bind("<Leave>", on_leave)

        # --- 削除ボタン ---
        delete_btn = tk.Button(scroll_frame, text="消去", command=self.delete_task_confirm, **button_style)
        delete_btn.pack(pady=5)
        delete_btn.bind("<Enter>", on_enter)
        delete_btn.bind("<Leave>", on_leave)

        # --- 戻るボタン ---
        back_btn = tk.Button(scroll_frame, text="← 編集を中断",
                             command=self.go_back_to_detail, **button_style)
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
            self.partner_id = task[5]

            self.memo_text.delete("1.0", tk.END)
            self.memo_text.insert("1.0", task[6] or "")

            for i in range(10):
                self.custom_vars[i].set(task[7 + i] or "")

        else:
            messagebox.showerror("エラー", "タスク情報の取得に失敗しました。")

    def save_changes(self):
        if self.task_id is None:
            messagebox.showerror("エラー", "タスクが選択されていません。")
            return

        memo = self.memo_text.get("1.0", tk.END).strip()
        customs = [var.get() for var in self.custom_vars]

        update_task(
            self.task_id,
            self.task_var.get(),
            self.location_var.get(),
            self.time_var.get(),
            self.partner_var.get(),
            self.partner_id,
            memo,
            customs
        )

        messagebox.showinfo("完了", "編集内容を保存しました。")
        self.controller.frames["TaskListFrame"].refresh_list()

        # 編集終了後は詳細画面を更新して遷移
        detail_frame = self.controller.frames["TaskDetailFrame"]
        detail_frame.set_task_id(self.task_id)
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

    def go_back_to_detail(self):
        # 編集中断時に詳細画面に戻る（詳細画面もtask_idをセットして更新）
        if self.task_id:
            detail_frame = self.controller.frames["TaskDetailFrame"]
            detail_frame.set_task_id(self.task_id)
            self.controller.show_frame("TaskDetailFrame")
