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
from frames.set_menu import SetMenuFrame
from frames.set_customlabel import CustomLabelFrame
from frames.set_topiccontrol import SetTopicControlFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("人物名鑑アプリ")
        self.geometry("600x1200")

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

        setting_menu.add_command(label="設定ウィンドウ",command=lambda: self.open_customwindow(frames_to_load=(SetMenuFrame,CustomLabelFrame,SetTopicControlFrame), 
        start_frame_class=SetMenuFrame,
        title="人物名鑑アプリ-設定-"))
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

            # Task関連 ← ここに追加！
            TaskListFrame,
            TaskRegisterFrame,
            TaskDetailFrame,
            TaskEditFrame,

            #set関連
            SetMenuFrame,
            CustomLabelFrame
        ):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuFrame")

    def open_customwindow(self, frames_to_load, start_frame_class, title):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("600x500")

        class SubController:
            def __init__(self, main_app, window):
                self.frames = {}
                self.main_app = main_app
                self.window = window  # ← Toplevel ウィンドウへの参照

            def show_frame(self, name):
                if name in self.frames:
                    self.frames[name].tkraise()
                else:
                    self.main_app.show_frame(name)

            def quit(self):
                self.window.destroy()  # ← quit ではなく destroy を使う

        controller = SubController(self, win)  # ← Toplevel を渡す

        container = tk.Frame(win)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        for F in frames_to_load:
            frame = F(container, controller)
            controller.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        controller.show_frame(start_frame_class.__name__)

    def show_frame(self, page_name):
        '''画面を切り替える'''
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    init_person_db()
    init_task_db()
    app = MainApp()
    app.mainloop()

