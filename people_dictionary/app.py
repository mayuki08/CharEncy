#app.py
import tkinter as tk
from database import init_person_db, init_task_db

from frames.menu import MenuFrame

# People関連のフレーム
from frames.people_register import PeopleRegisterFrame
from frames.people_detail import PeopleDetailFrame
from frames.people_edit import PeopleEditFrame
from frames.people_list import PeopleListFrame

# Task関連のフレーム（新しく追加する）
from frames.task_list import TaskListFrame
from frames.task_register import TaskRegisterFrame
from frames.task_detail import TaskDetailFrame
from frames.task_edit import TaskEditFrame

#Setting関連のフレーム
from frames.customfieldsetting import CustomFieldSettingFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("人物名鑑アプリ")
        self.geometry("600x1200")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        # 各画面（Frame）を登録
        for F in (
            MenuFrame,

            # People関連
            PeopleRegisterFrame,
            PeopleDetailFrame,
            PeopleEditFrame,
            PeopleListFrame,

            # Task関連 ← ここに追加！
            TaskListFrame,
            TaskRegisterFrame,
            TaskDetailFrame,
            TaskEditFrame,

            #setting関連
            CustomFieldSettingFrame

        ):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuFrame")

    def show_frame(self, page_name):
        '''画面を切り替える'''
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    init_person_db()
    init_task_db()
    app = MainApp()
    app.mainloop()

