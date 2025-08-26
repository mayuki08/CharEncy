import tkinter as tk
from frames.menu import MenuFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("人物名鑑アプリ")
        self.geometry("600x500")

        # コンテナを grid に
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        # ウィンドウ全体を grid で伸ばす
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # MenuFrame を生成
        menu = MenuFrame(container, self)
        menu.grid(row=0, column=0)  # コンテナの中央に置く

        # コンテナの行・列を中央に揃えるため余白
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
