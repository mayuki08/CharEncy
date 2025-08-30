import tkinter as tk
from tkinter import ttk
from database import init_parson_db, init_task_db

from frames.menu import MenuFrame

# People関連のフレーム
from frames.peopleregister import PeopleRegisterFrame
from frames.peopledetail import PeopleDetailFrame
from frames.peopleedit import PeopleEditFrame
from frames.peoplelist import PeopleListFrame

# Task関連のフレーム
from frames.tasklist import TaskListFrame
from frames.taskregister import TaskRegisterFrame
from frames.taskdetail import TaskDetailFrame
from frames.taskedit import TaskEditFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("人物名鑑アプリ")
        self.geometry("600x700")

        # メニューバー作成
        menubar = tk.Menu(self)

        # ページ一覧
        people_menu = tk.Menu(menubar, tearoff=0)
        people_menu.add_command(label="人物登録",command=lambda: self.show_frame("PeopleRegisterFrame"))

        people_menu.add_command(label="人物一覧", command=lambda: self.show_frame("PeopleListFrame"))

        people_menu.add_command(label="タスク登録", command=lambda: self.show_frame("TaskRegisterFrame"))

        people_menu.add_command(label="タスク一覧", command=lambda: self.show_frame("TaskListFrame"))
        menubar.add_cascade(label="ページ一覧", menu=people_menu)

        #設定
        setting_menu = tk.Menu(menubar, tearoff=0)

        setting_menu.add_command(label="カスタム",command=lambda: self.open_custom_window())
        menubar.add_cascade(label="設定", menu=setting_menu)

        # ウィンドウに設定
        self.config(menu=menubar)

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
            # Task関連
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
    
    #別ウィンドウで開く
    def open_custom_window(self):
        win = tk.Toplevel(self)
        win.title("カスタム設定")
        win.geometry("550x770")

        frame = TaskEditFrame(win, self)
        frame.pack(fill="both", expand=True)

    def show_frame(self, page_name):
        """画面を切り替える"""
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    init_parson_db()
    init_task_db()
    app = MainApp()
    app.mainloop()
