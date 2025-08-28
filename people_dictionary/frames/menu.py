# frames/menu.py
import tkinter as tk
from tkinter import font

class MenuFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # 親フレーム全体を grid 管理
        #self.pack(fill="both", expand=True)
        #for i in range(3):
            #self.rowconfigure(i, weight=1)
            #self.columnconfigure(i, weight=1)
        
        # 親フレームをいっぱいに広げる
        self.pack(fill="both", expand=True)

        # 中央フレーム
        self.center_frame = tk.Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # フォント
        title_font = font.Font(family="Arial", size=24, weight="bold")
        menu_font = font.Font(family="Arial", size=18)
        button_font = font.Font(family="Arial", size=14)

        # タイトル（横も中央）
        tk.Label(self.center_frame, text="人物名鑑アプリ", font=title_font).pack(pady=(0, 20))

        # 横線
        tk.Frame(self.center_frame, height=3, bg="black").pack(fill="x", pady=(0,20))

        # メニュー見出し
        tk.Label(self.center_frame, text="メニュー", font=menu_font).pack(pady=(0,20))

        # ボタン（横中央）
        tk.Button(self.center_frame, text="人物登録", width=20, font=button_font,
                  command=lambda: self.controller.show_frame("RegisterFrame")).pack(pady=10)
        tk.Button(self.center_frame, text="人物一覧", width=20, font=button_font,
                  command=lambda: self.controller.show_frame("ListFrame")).pack(pady=10)
        tk.Button(self.center_frame, text="終了", width=20, font=button_font,
                  command=self.controller.quit).pack(pady=10)