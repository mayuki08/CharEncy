# frames/people_edit.py
import tkinter as tk
from tkinter import messagebox, font, filedialog, ttk
from database import get_person_by_id, update_person, delete_person
import pykakasi
import os
import shutil
from settings import load_topicbool
from frames.set_customlabel import load_custom_field_settings

IMAGE_DIR = "images"

class PeopleEditFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.person_id = None

        self.topic_control = load_topicbool()

        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)

        self.kks = pykakasi.kakasi()

        # 入力用変数
        self.name_var = tk.StringVar()
        self.furigana_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.group_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.image_path_var = tk.StringVar()

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

        # 画像選択ボタン（topic_controlで制御）
        if self.topic_control["pnormalcontrol"][0]:
            tk.Button(form, text="画像選択", command=self.select_profile_image, font=entry_font).grid(row=0, column=1, pady=10, sticky="w")

        # 名前とふりがな（rowをずらす）
        tk.Label(form, text="名前 *", font=entry_font, fg="red").grid(row=1, column=0, pady=10, sticky="e")
        name_entry = tk.Entry(form, textvariable=self.name_var, font=entry_font)
        name_entry.grid(row=1, column=1, pady=10)
        name_entry.bind("<FocusOut>", self.auto_fill_furigana)

        tk.Label(form, text="ふりがな *", font=entry_font, fg="red").grid(row=2, column=0, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.furigana_var, font=entry_font).grid(row=2, column=1, pady=10)

        # 職業
        if self.topic_control["pnormalcontrol"][0]:
            tk.Label(form, text="職業/肩書き", font=entry_font).grid(row=3, column=0, pady=10, sticky="e")
            tk.Entry(form, textvariable=self.job_var, font=entry_font).grid(row=3, column=1, pady=10)

        # グループ
        if self.topic_control["pnormalcontrol"][1]:
            tk.Label(form, text="グループ", font=entry_font).grid(row=4, column=0, pady=10, sticky="e")
            group_options = ["家族", "友人", "仕事", "学校", "趣味"]
            self.group_combobox = ttk.Combobox(form, textvariable=self.group_var, values=group_options, font=entry_font, width=29, state="normal")
            self.group_combobox.grid(row=4, column=1, pady=10)

        # 出会った日
        if self.topic_control["pnormalcontrol"][2]:
            tk.Label(form, text="出会った日", font=entry_font).grid(row=5, column=0, pady=10, sticky="e")
            date_frame = tk.Frame(form)
            date_frame.grid(row=5, column=1, pady=10)

            tk.Entry(date_frame, textvariable=self.year_var, width=6, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="年", font=entry_font).pack(side=tk.LEFT, padx=(2, 5))
            tk.Entry(date_frame, textvariable=self.month_var, width=4, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="月", font=entry_font).pack(side=tk.LEFT, padx=(2, 5))
            tk.Entry(date_frame, textvariable=self.day_var, width=4, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="日", font=entry_font).pack(side=tk.LEFT)

        # メモ
        if self.topic_control["pnormalcontrol"][3]:
            tk.Label(form, text="メモ", font=entry_font).grid(row=6, column=0, pady=10, sticky="ne")
            self.memo_text = tk.Text(form, width=32, height=5, font=("Arial", 12))
            self.memo_text.grid(row=6, column=1, padx=10, pady=10)
        else:
            self.memo_text = None

        # カスタム項目（10項目すべて表示）
        self.custom_labeltitles = load_custom_field_settings()["person_custom_labels"]
        self.custom_labels = []
        self.custom_vars = []

        start_row = 7  # カスタム項目開始行

        for i in range(10):
            var = tk.StringVar()
            self.custom_vars.append(var)

            label = tk.Label(form, text=self.custom_labeltitles[i], font=entry_font)
            entry = tk.Entry(form, textvariable=var, font=entry_font)

            label.grid(row=start_row + i, column=0, pady=10, sticky="e")
            entry.grid(row=start_row + i, column=1, pady=10)

            self.custom_labels.append(label)

        # ボタンホバーエフェクト
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        button_style = {"font": entry_font, "width": 20, "relief": "raised", "bd": 4}

        save_btn = tk.Button(center_frame, text="編集を保存", command=self.save_changes, **button_style)
        save_btn.pack(pady=5)
        save_btn.bind("<Enter>", on_enter)
        save_btn.bind("<Leave>", on_leave)

        delete_btn = tk.Button(center_frame, text="消去", command=self.delete_person_confirm, **button_style)
        delete_btn.pack(pady=5)
        delete_btn.bind("<Enter>", on_enter)
        delete_btn.bind("<Leave>", on_leave)

        back_btn = tk.Button(center_frame, text="←編集を中断",
                             command=lambda: controller.show_frame("PeopleDetailFrame"), **button_style)
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    def set_person_id(self, person_id):
        self.person_id = person_id
        person = get_person_by_id(person_id)

        if person:
            self.name_var.set(person[1] or "")
            self.furigana_var.set(person[2] or "")
            self.group_var.set(person[3] or "")
            self.job_var.set(person[4] or "")

            if self.memo_text:
                self.memo_text.delete("1.0", tk.END)
                self.memo_text.insert("1.0", person[6] or "")

            date = person[5] or ""
            if "-" in date:
                parts = date.split("-")
                self.year_var.set(parts[0])
                self.month_var.set(parts[1])
                self.day_var.set(parts[2])
            else:
                self.year_var.set("")
                self.month_var.set("")
                self.day_var.set("")

            # ここで画像パスをセット
            self.image_path_var.set(person[7] or "")

            # カスタムは8〜17
            customs = person[8:18]
            for i, val in enumerate(customs):
                self.custom_vars[i].set(val or "")
        else:
            messagebox.showerror("エラー", "人物情報の取得に失敗しました。")

    def delete_person_confirm(self):
        if self.person_id is None:
            messagebox.showerror("エラー", "人物が選択されていません。")
            return

        if messagebox.askyesno("確認", "この人物を削除してもよろしいですか？"):
            delete_person(self.person_id)
            messagebox.showinfo("削除完了", "人物を削除しました。")

            # 一覧を更新してリスト画面へ戻る
            if "PeopleListFrame" in self.controller.frames:
                self.controller.frames["PeopleListFrame"].refresh_list()
            self.controller.show_frame("PeopleListFrame")

    def select_profile_image(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(title="プロフィール画像を選択", filetypes=filetypes)
        if filepath:
            filename = os.path.basename(filepath)
            dest_path = os.path.join(IMAGE_DIR, filename)
            try:
                shutil.copyfile(filepath, dest_path)
                self.image_path_var.set(dest_path)
                messagebox.showinfo("画像設定", "プロフィール画像を設定しました。")
            except Exception as e:
                messagebox.showerror("エラー", f"画像のコピーに失敗しました: {e}")

    def auto_fill_furigana(self, event=None):
        if not self.furigana_var.get():
            text = self.name_var.get()
            if text:
                result = self.kks.convert(text)
                furigana = "".join([item["hira"] for item in result])
                self.furigana_var.set(furigana)

    def refresh_labels(self):
        new_labels = load_custom_field_settings()["person_custom_labels"]
        for i in range(10):
            self.custom_labels[i]["text"] = new_labels[i]

    def save_changes(self):
        if self.person_id is None:
            messagebox.showerror("エラー", "人物が選択されていません。")
            return

        name = self.name_var.get().strip()
        furigana = self.furigana_var.get().strip()
        group = self.group_var.get().strip()
        job = self.job_var.get().strip()
        year = self.year_var.get().strip()
        month = self.month_var.get().strip().zfill(2)
        day = self.day_var.get().strip().zfill(2)
        date = f"{year}-{month}-{day}" if year and month and day else ""
        memo = self.memo_text.get("1.0", "end-1c") if self.memo_text else ""
        image_path = self.image_path_var.get().strip()
        custom = [var.get().strip() for var in self.custom_vars]

        if not name:
            messagebox.showwarning("入力エラー", "名前は必須です。")
            return
        if not furigana:
            messagebox.showwarning("入力エラー", "ふりがなは必須です。")
            return

        update_person(self.person_id, name, furigana, group, job, date, memo, image_path, *custom)

        messagebox.showinfo("保存完了", "人物情報を更新しました。")

        # 詳細画面を再読み込みして表示
        if "PeopleDetailFrame" in self.controller.frames:
            self.controller.frames["PeopleDetailFrame"].set_person_id(self.person_id)
        if "PeopleListFrame" in self.controller.frames:
            self.controller.frames["PeopleListFrame"].refresh_list()

        self.controller.show_frame("PeopleDetailFrame")

