# frames/menu.py
import tkinter as tk

class MenuFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        
        # ボタンをまとめるフレームを作る
        button_frame = tk.Frame(self)
        button_frame.place(relx=0.5, rely=0.5, anchor='center')  # ここで縦横中央に配置

        tk.Label(self, text="人物名鑑アプリ メニュー", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="人物登録", width=50,
                  command=lambda: controller.show_frame("RegisterFrame")).pack(pady=10)
        tk.Button(self, text="人物検索", width=20,
                  command=lambda: controller.show_frame("SearchFrame")).pack(pady=10)
        tk.Button(self, text="終了", width=20, command=controller.quit).pack(pady=10)
