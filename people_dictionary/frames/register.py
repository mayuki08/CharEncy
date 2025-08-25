# frames/register.py
import tkinter as tk
from tkinter import messagebox
from database import add_person

class RegisterFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.name_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.memo_var = tk.StringVar()

        tk.Label(self, text="人物登録", font=("Arial", 16)).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=5)

        tk.Label(form, text="名前").grid(row=0, column=0)
        tk.Entry(form, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(form, text="職業/肩書き").grid(row=1, column=0)
        tk.Entry(form, textvariable=self.job_var).grid(row=1, column=1)

        tk.Label(form, text="出会った日 (YYYY-MM-DD)").grid(row=2, column=0)
        tk.Entry(form, textvariable=self.date_var).grid(row=2, column=1)

        tk.Label(form, text="メモ").grid(row=3, column=0)
        tk.Entry(form, textvariable=self.memo_var).grid(row=3, column=1)

        tk.Button(self, text="追加", command=self.add_person_gui).pack(pady=10)
        tk.Button(self, text="← メニューに戻る", command=lambda: controller.show_frame("MenuFrame")).pack()

    def add_person_gui(self):
        name = self.name_var.get()
        job = self.job_var.get()
        date = self.date_var.get()
        memo = self.memo_var.get()

        if not name:
            messagebox.showwarning("入力エラー", "名前は必須です。")
            return

        add_person(name, job, date, memo)
        self.name_var.set("")
        self.job_var.set("")
        self.date_var.set("")
        self.memo_var.set("")
        messagebox.showinfo("登録成功", "人物情報を登録しました。")
