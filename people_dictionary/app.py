import tkinter as tk
from database import init_parson_db, init_task_db

from frames.menu import MenuFrame

# People関連のフレーム
from frames.peopleregister import PeopleRegisterFrame
from frames.peopledetail import PeopleDetailFrame
from frames.peopleedit import PeopleEditFrame
from frames.peoplelist import PeopleListFrame

# Task関連のフレーム（新しく追加する）
from frames.tasklist import TaskListFrame
from frames.taskregister import TaskRegisterFrame
from frames.taskdetail import TaskDetailFrame
from frames.taskedit import TaskEditFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("人物名鑑アプリ")
        self.geometry("600x700")

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
            TaskEditFrame
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
    init_parson_db()
    init_task_db()
    app = MainApp()
    app.mainloop()

