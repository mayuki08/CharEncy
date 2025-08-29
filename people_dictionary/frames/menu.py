import tkinter as tk
from tkinter import font
from tkinter import ttk


class MenuFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # 親フレームをいっぱいに広げる
        self.pack(fill="both", expand=True)

        # 中央フレーム
        self.center_frame = tk.Frame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # フォント
        title_font = font.Font(family="Arial", size=35, weight="bold")
        menu_font = font.Font(family="Arial", size=25)
        button_font = font.Font(family="Arial", size=17)

        # タイトル（横も中央）
        tk.Label(self.center_frame, text="人物名鑑アプリ", font=title_font).pack(pady=(0, 20))

        # 横線
        tk.Frame(self.center_frame, height=3, bg="black").pack(fill="x", pady=(0,20))

        # メニュー見出し
        tk.Label(self.center_frame, text="▼メニュー", font=menu_font).pack(pady=(10,25))

        # ホバー用関数
        def on_enter(e):
            e.widget['background'] = '#3cb371'
        def on_leave(e):
            e.widget['background'] = '#2e8b57'
            
        # ボタン（横中央）
        pregister_btn = tk.Button(self.center_frame, text="人物登録", bg="#2e8b57", fg="white", activebackground="#3cb371", width=20, font=button_font,
                  command=lambda: self.controller.show_frame("PeopleRegisterFrame"),relief="raised",bd=4)
        
        pregister_btn.pack(pady=10)
        pregister_btn.bind("<Enter>", on_enter)
        pregister_btn.bind("<Leave>", on_leave)
        
        plist_btn = tk.Button(self.center_frame, text="人物一覧", bg="#2e8b57", fg="white", activebackground="#3cb371", width=20, font=button_font,
                  command=lambda: self.controller.show_frame("PeopleListFrame"),relief="raised",bd=4)
        
        plist_btn.pack(pady=10)
        plist_btn.bind("<Enter>", on_enter)
        plist_btn.bind("<Leave>", on_leave)

        tregister_btn = tk.Button(self.center_frame, text="タスク登録", bg="#2e8b57", fg="white", activebackground="#3cb371", width=20, font=button_font,
                  command=lambda: self.controller.show_frame("TaskRegisterFrame"),relief="raised",bd=4)
        
        tregister_btn.pack(pady=10)
        tregister_btn.bind("<Enter>", on_enter)
        tregister_btn.bind("<Leave>", on_leave)

        tlist_btn = tk.Button(self.center_frame, text="タスク一覧", bg="#2e8b57", fg="white", activebackground="#3cb371", width=20, font=button_font,
                command=lambda: self.controller.show_frame("TaskListFrame"),relief="raised",bd=4)

        tlist_btn.pack(pady=10)
        tlist_btn.bind("<Enter>", on_enter)
        tlist_btn.bind("<Leave>", on_leave)
        
        # 終了用関数
        def on_enter(e):
            e.widget['background'] = '#F1F1F1'
        def on_leave(e):
            e.widget['background'] = '#EEEEEE'
        
        end_btn = tk.Button(self.center_frame, text="終了", width=20, font=button_font,relief="raised",bd=4,
                  command=self.controller.quit)
        
        end_btn.pack(pady=10)
        end_btn.bind("<Enter>", on_enter)
        end_btn.bind("<Leave>", on_leave)

