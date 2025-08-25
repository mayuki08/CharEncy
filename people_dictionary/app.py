# app.py

import tkinter as tk
from database import init_db
from frames.menu import MenuFrame
from frames.register import RegisterFrame
from frames.search import SearchFrame
from frames.detail import DetailFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("人物名鑑アプリ")
        self.geometry("600x500")

        # 画面を格納するコンテナ
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # 各画面を生成して辞書に登録
        for F in (MenuFrame, RegisterFrame, SearchFrame, DetailFrame):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 最初の画面を表示
        self.show_frame("MenuFrame")

    def show_frame(self, page_name):
        '''画面を切り替える'''
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    init_db()
    app = MainApp()
    app.mainloop()
