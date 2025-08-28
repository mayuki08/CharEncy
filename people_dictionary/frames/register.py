# frames/register.py
import tkinter as tk
from tkinter import messagebox, font
from database import add_person
import pykakasi

class RegisterFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.kks = pykakasi.kakasi()

        # 入力用変数
        self.name_var = tk.StringVar()
        self.furigana_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()

        # 中央寄せ用フレーム
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # タイトル
        tk.Label(center_frame, text="人物登録", font=title_font).pack(pady=20)

        # 横線
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=80, pady=(0, 50))

        form = tk.Frame(center_frame)
        form.pack(pady=5)

        # 名前とふりがな
        tk.Label(form, text="名前 *", font=entry_font, fg="red").grid(row=0, column=0, pady=10)
        name_entry = tk.Entry(form, textvariable=self.name_var, font=entry_font)
        name_entry.grid(row=0, column=1, pady=10)
        name_entry.bind("<FocusOut>", self.auto_fill_furigana)

        tk.Label(form, text="ふりがな *", font=entry_font, fg="red").grid(row=1, column=0, pady=10)
        tk.Entry(form, textvariable=self.furigana_var, font=entry_font).grid(row=1, column=1, pady=10)

        # 職業
        tk.Label(form, text="職業/肩書き", font=entry_font).grid(row=2, column=0, pady=10)
        tk.Entry(form, textvariable=self.job_var, font=entry_font).grid(row=2, column=1, pady=10)

        # 出会った日（年・月・日）
        tk.Label(form, text="出会った日", font=entry_font).grid(row=3, column=0, pady=10)
        date_frame = tk.Frame(form)
        date_frame.grid(row=3, column=1, pady=10)

        tk.Entry(date_frame, textvariable=self.year_var, width=6, font=entry_font).pack(side=tk.LEFT)
        tk.Label(date_frame, text="年", font=entry_font).pack(side=tk.LEFT, padx=(2, 5))

        tk.Entry(date_frame, textvariable=self.month_var, width=4, font=entry_font).pack(side=tk.LEFT)
        tk.Label(date_frame, text="月", font=entry_font).pack(side=tk.LEFT, padx=(2, 5))

        tk.Entry(date_frame, textvariable=self.day_var, width=4, font=entry_font).pack(side=tk.LEFT)
        tk.Label(date_frame, text="日", font=entry_font).pack(side=tk.LEFT)

        # メモ欄
        tk.Label(form, text="メモ", font=entry_font).grid(row=4, column=0, pady=10)
        self.memo_text = tk.Text(form, width=32, height=5, font=("Arial", 12))
        self.memo_text.grid(row=4, column=1, padx=10, pady=10)

        # ホバーエフェクト
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        # 追加ボタン
        add_btn = tk.Button(center_frame, text="追加", command=self.add_person_gui,
                            font=entry_font, relief="raised", bd=4, bg="#EEEEEE")
        add_btn.pack(pady=10)
        add_btn.bind("<Enter>", on_enter)
        add_btn.bind("<Leave>", on_leave)

        # 戻るボタン
        back_btn = tk.Button(center_frame, text="← メニューに戻る",
                             command=lambda: controller.show_frame("MenuFrame"),
                             font=entry_font, relief="raised", bd=4, bg="#EEEEEE")
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    def auto_fill_furigana(self, event=None):
        name = self.name_var.get()
        if not name:
            return
        result = self.kks.convert(name)
        furigana = ''.join([item['hira'] for item in result])
        self.furigana_var.set(furigana)

    def add_person_gui(self):
        name = self.name_var.get()
        furigana = self.furigana_var.get()
        job = self.job_var.get()
        year = self.year_var.get()
        month = self.month_var.get().zfill(2)
        day = self.day_var.get().zfill(2)
        date = f"{year}-{month}-{day}" if year and month and day else ""
        memo = self.memo_text.get("1.0", "end-1c")

        if not name:
            messagebox.showwarning("入力エラー", "名前は必須です。")
            return
        if not furigana:
            messagebox.showwarning("入力エラー", "ふりがなは必須です。")
            return

        add_person(name, furigana, job, date, memo)

        # フィールドクリア
        self.name_var.set("")
        self.furigana_var.set("")
        self.job_var.set("")
        self.year_var.set("")
        self.month_var.set("")
        self.day_var.set("")
        self.memo_text.delete("1.0", "end")

        messagebox.showinfo("登録成功", "人物情報を登録しました。")

        # ListFrameの更新
        if "ListFrame" in self.controller.frames:
            self.controller.frames["ListFrame"].refresh_list()
