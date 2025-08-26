# frames/detail.py
import tkinter as tk
from tkinter import messagebox
#from database import get_person_by_id, update_person, delete_person

class DetailFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.person_id = None

        tk.Label(self, text="人物詳細", font=("Arial", 16)).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=5)

        self.name_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.memo_var = tk.StringVar()

        tk.Label(form, text="名前").grid(row=0, column=0)
        tk.Entry(form, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(form, text="職業/肩書き").grid(row=1, column=0)
        tk.Entry(form, textvariable=self.job_var).grid(row=1, column=1)

        tk.Label(form, text="出会った日").grid(row=2, column=0)
        tk.Entry(form, textvariable=self.date_var).grid(row=2, column=1)

