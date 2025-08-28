import tkinter as tk
from tkinter import messagebox, font
from database import get_person_by_id, update_person, delete_person

class DetailFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.person_id = None

        # --- フォント設定 ---
        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # --- 中央揃え用フレーム ---
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="人物詳細", font=title_font).pack(pady=20)
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=120, pady=(0, 30))

        form = tk.Frame(center_frame)
        form.pack(pady=10)

        # --- 変数 ---
        self.name_var = tk.StringVar()
        self.furigana_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.memo_var = tk.StringVar()

        # --- 名前 ---
        tk.Label(form, text="名前", font=entry_font).grid(row=0, column=0, sticky="e")
        tk.Entry(form, textvariable=self.name_var, font=entry_font, width=30).grid(row=0, column=1, pady=5)

        # --- ふりがな ---
        tk.Label(form, text="ふりがな", font=entry_font).grid(row=1, column=0, sticky="e")
        tk.Entry(form, textvariable=self.furigana_var, font=entry_font, width=30).grid(row=1, column=1, pady=5)

        # --- 職業 ---
        tk.Label(form, text="職業/肩書き", font=entry_font).grid(row=2, column=0, sticky="e")
        tk.Entry(form, textvariable=self.job_var, font=entry_font, width=30).grid(row=2, column=1, pady=5)

        # --- 出会った日 ---
        tk.Label(form, text="出会った日", font=entry_font).grid(row=3, column=0, sticky="e")

        date_frame = tk.Frame(form)
        date_frame.grid(row=3, column=1, sticky="w")

        tk.Entry(date_frame, textvariable=self.year_var, width=6, font=entry_font).pack(side=tk.LEFT)
        tk.Label(date_frame, text="年", font=entry_font).pack(side=tk.LEFT)

        tk.Entry(date_frame, textvariable=self.month_var, width=4, font=entry_font).pack(side=tk.LEFT)
        tk.Label(date_frame, text="月", font=entry_font).pack(side=tk.LEFT)

        tk.Entry(date_frame, textvariable=self.day_var, width=4, font=entry_font).pack(side=tk.LEFT)
        tk.Label(date_frame, text="日", font=entry_font).pack(side=tk.LEFT)

        # --- メモ ---
        tk.Label(form, text="備考", font=entry_font).grid(row=4, column=0, sticky="ne", pady=10)
        self.memo_text = tk.Text(form, width=30, height=5, font=entry_font)
        self.memo_text.grid(row=4, column=1, pady=10)

        # --- ボタンホバー関数 ---
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        # --- ボタン類 ---
        button_style = {"font": entry_font, "width": 20, "relief": "raised", "bd": 4}

        save_btn = tk.Button(center_frame, text="編集を保存", command=self.save_changes, **button_style)
        save_btn.pack(pady=5)
        save_btn.bind("<Enter>", on_enter)
        save_btn.bind("<Leave>", on_leave)

        delete_btn = tk.Button(center_frame, text="消去", command=self.delete_person_confirm, **button_style)
        delete_btn.pack(pady=5)
        delete_btn.bind("<Enter>", on_enter)
        delete_btn.bind("<Leave>", on_leave)

        back_btn = tk.Button(center_frame, text="← 一覧に戻る",
                             command=lambda: controller.show_frame("ListFrame"), **button_style)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    def set_person_id(self, person_id):
        self.person_id = person_id
        person = get_person_by_id(person_id)

        if person:
            self.name_var.set(person[1] or "")
            self.furigana_var.set(person[2] or "")
            self.job_var.set(person[3] or "")
            self.memo_text.delete("1.0", tk.END)
            self.memo_text.insert("1.0", person[5] or "")

            date = person[4] or ""
            if "-" in date:
                parts = date.split("-")
                self.year_var.set(parts[0])
                self.month_var.set(parts[1])
                self.day_var.set(parts[2])
            else:
                self.year_var.set("")
                self.month_var.set("")
                self.day_var.set("")
        else:
            messagebox.showerror("エラー", "人物情報の取得に失敗しました。")

    def save_changes(self):
        if self.person_id is None:
            messagebox.showerror("エラー", "人物が選択されていません。")
            return

        year = self.year_var.get().zfill(4)
        month = self.month_var.get().zfill(2)
        day = self.day_var.get().zfill(2)
        date = f"{year}-{month}-{day}"

        memo = self.memo_text.get("1.0", tk.END).strip()

        update_person(
            self.person_id,
            self.name_var.get(),
            self.furigana_var.get(),
            self.job_var.get(),
            date,
            memo
        )

        messagebox.showinfo("完了", "編集内容を保存しました。")
        self.controller.frames["ListFrame"].refresh_list()
        self.controller.show_frame("ListFrame")

    def delete_person_confirm(self):
        if self.person_id is None:
            messagebox.showerror("エラー", "人物が選択されていません。")
            return

        if messagebox.askyesno("確認", "この人物を削除してもよろしいですか？"):
            delete_person(self.person_id)
            messagebox.showinfo("削除", "人物を削除しました。")
            self.controller.frames["ListFrame"].refresh_list()
            self.controller.show_frame("ListFrame")


