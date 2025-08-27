# frames/detail.py
import tkinter as tk
from tkinter import messagebox
from database import get_person_by_id, update_person, delete_person

class DetailFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.person_id = None

        tk.Label(self, text="人物詳細", font=("Arial", 16)).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=5)

        self.name_var = tk.StringVar()
        self.furigana_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.memo_var = tk.StringVar()

        tk.Label(form, text="名前").grid(row=0, column=0)
        tk.Entry(form, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(form, text="ふりがな").grid(row=1, column=0)
        tk.Entry(form, textvariable=self.furigana_var).grid(row=1, column=1)

        tk.Label(form, text="職業/肩書き").grid(row=2, column=0)
        tk.Entry(form, textvariable=self.job_var).grid(row=2, column=1)

        tk.Label(form, text="出会った日").grid(row=3, column=0)
        tk.Entry(form, textvariable=self.date_var).grid(row=3, column=1)

        tk.Label(form, text="備考").grid(row=4, column=0)
        tk.Entry(form, textvariable=self.memo_var).grid(row=4, column=1)

        tk.Button(self, text="編集を保存", width=20, command=self.save_changes).pack(pady=10)
        tk.Button(self, text="消去", width=20, command=self.delete_person_confirm).pack(pady=10)

        tk.Button(self, text="一覧に戻る", width=20,
                  command=lambda: controller.show_frame("ListFrame")).pack(pady=10)

    def set_person_id(self, person_id):
        """人物IDをセットし、その人物の詳細を表示"""
        self.person_id = person_id
        person = get_person_by_id(person_id)

        if person:
            # person = (id, name, job, met_date, memo)
            self.name_var.set(person[1] or "")
            self.furigana_var.set(person[2] or "")
            self.job_var.set(person[3] or "")
            self.date_var.set(person[4] or "")
            self.memo_var.set(person[5] or "")
        else:
            # 取得失敗時
            self.name_var.set("")
            self.furigana_var.set("")
            self.job_var.set("")
            self.date_var.set("")
            self.memo_var.set("")
            tk.messagebox.showerror("エラー", "人物情報の取得に失敗しました。")
    
    def save_changes(self):
        if self.person_id is None:
            messagebox.showerror("エラー", "人物が選択されていません。")
            return

        update_person(
            self.person_id,
            self.name_var.get(),
            self.furigana_var.get(),
            self.job_var.get(),
            self.date_var.get(),
            self.memo_var.get()
        )

        messagebox.showinfo("完了", "編集内容を保存しました。")
        self.controller.frames["ListFrame"].refresh_list()
        self.controller.show_frame("ListFrame")

    def delete_person_confirm(self):
        if self.person_id is None:
            messagebox.showerror("エラー", "人物が選択されていません。")
            return

        confirm = messagebox.askyesno("確認", "この人物を削除してもよろしいですか？")
        if confirm:
            delete_person(self.person_id)
            messagebox.showinfo("削除", "人物を削除しました。")
            self.controller.frames["ListFrame"].refresh_list()
            self.controller.show_frame("ListFrame")

