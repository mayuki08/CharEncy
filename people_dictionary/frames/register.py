# frames/register.py
import tkinter as tk
from tkinter import messagebox
from database import get_all_people,add_person
import pykakasi

class RegisterFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.kks = pykakasi.kakasi()  # ← 初期化ここで一度だけ

        self.name_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.memo_var = tk.StringVar()
        self.furigana_var = tk.StringVar()

        tk.Label(self, text="人物登録", font=("Arial", 16)).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=5)

        tk.Label(form, text="名前").grid(row=0, column=0)
        name_entry = tk.Entry(form, textvariable=self.name_var)
        name_entry.grid(row=0, column=1)
        name_entry.bind("<FocusOut>", self.auto_fill_furigana)  # ← イベントバインド

        tk.Label(form, text="ふりがな").grid(row=1, column=0)
        tk.Entry(form, textvariable=self.furigana_var).grid(row=1, column=1)

        tk.Label(form, text="職業/肩書き").grid(row=2, column=0)
        tk.Entry(form, textvariable=self.job_var).grid(row=2, column=1)

        tk.Label(form, text="出会った日 (YYYY-MM-DD)").grid(row=3, column=0)
        tk.Entry(form, textvariable=self.date_var).grid(row=3, column=1)

        tk.Label(form, text="メモ").grid(row=4, column=0)
        tk.Entry(form, textvariable=self.memo_var).grid(row=4, column=1)

        tk.Button(self, text="追加", command=self.add_person_gui).pack(pady=10)
        tk.Button(self, text="← メニューに戻る", command=lambda: controller.show_frame("MenuFrame")).pack()

    def add_person_gui(self):
        name = self.name_var.get()
        furigana = self.furigana_var.get()
        job = self.job_var.get()
        date = self.date_var.get()
        memo = self.memo_var.get()

        if not name:
            messagebox.showwarning("入力エラー", "名前は必須です。")
            return
        if not furigana:
            messagebox.showwarning("入力エラー", "ふりがなは必須です。")
            return


        add_person(name, furigana, job, date, memo)

        # 入力欄クリア
        self.clear_inputs()

        # ✅ ListFrame を取得してリストを更新
        self.controller.frames["ListFrame"].refresh_list()
    
    def auto_fill_furigana(self, event=None):
        name = self.name_var.get()
        if not name:
            return
        result = self.kks.convert(name)
        furigana = ''.join([item['hira'] for item in result])
        self.furigana_var.set(furigana)

    def clear_inputs(self):
        self.name_var.set("")
        self.furigana_var.set("")
        self.job_var.set("")
        self.date_var.set("")
        self.memo_var.set("")

    def refresh_list(self):
        people = get_all_people()

