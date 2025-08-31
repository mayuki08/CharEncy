# frames/people_register.py
import tkinter as tk
from tkinter import messagebox, font, filedialog,ttk
from database import add_person
import pykakasi
import os, shutil
from settings import load_topicbool  # 追加
from frames.set_customlabel import load_custom_field_settings

IMAGE_DIR = "images"

class PeopleRegisterFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.topic_control = load_topicbool()
        
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)   # フォルダがなければ作成

        self.kks = pykakasi.kakasi()

        # 入力用変数
        self.name_var = tk.StringVar()
        self.furigana_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.group_var = tk.StringVar()  # ← 追加
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.image_path_var = tk.StringVar()

        # 中央寄せ用フレーム
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # フォーム（中央寄せフレームの中に置く）
        self.form = tk.Frame(center_frame)
        self.form.pack(pady=5)

        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # タイトル
        tk.Label(center_frame, text="人物登録", font=title_font).pack(pady=20)

        # 横線
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=80, pady=(0, 50))

        # 画像選択ボタン（新規追加）
        if self.topic_control["pnormalcontrol"][0]: 
            tk.Button(self.form, text="画像選択", command=self.select_profile_image, font=entry_font).grid(row=0, column=1, pady=10, sticky="w")

        # 名前とふりがな（row を +1 ずらす）
        tk.Label(self.form, text="名前 *", font=entry_font, fg="red").grid(row=1, column=0, pady=10, sticky="e")
        name_entry = tk.Entry(self.form, textvariable=self.name_var, font=entry_font)
        name_entry.grid(row=1, column=1, pady=10)
        name_entry.bind("<FocusOut>", self.auto_fill_furigana)

        tk.Label(self.form, text="ふりがな *", font=entry_font, fg="red").grid(row=2, column=0, pady=10, sticky="e")
        tk.Entry(self.form, textvariable=self.furigana_var, font=entry_font).grid(row=2, column=1, pady=10)

        # 職業
        if self.topic_control["pnormalcontrol"][0]:
            tk.Label(self.form, text="職業/肩書き", font=entry_font).grid(row=3, column=0, pady=10, sticky="e")
            tk.Entry(self.form, textvariable=self.job_var, font=entry_font).grid(row=3, column=1, pady=10)

        # グループ
        if self.topic_control["pnormalcontrol"][1]:
            tk.Label(self.form, text="グループ", font=entry_font).grid(row=4, column=0, pady=10, sticky="e")
            group_options = ["家族", "友人", "仕事", "学校", "趣味"]
            self.group_combobox = ttk.Combobox(self.form, textvariable=self.group_var, values=group_options, font=entry_font, width=29, state="normal")
            self.group_combobox.grid(row=4, column=1, pady=10)

        # 出会った日
        if self.topic_control["pnormalcontrol"][2]:
            tk.Label(self.form, text="出会った日", font=entry_font).grid(row=5, column=0, pady=10, sticky="e")
            date_frame = tk.Frame(self.form)
            date_frame.grid(row=5, column=1, pady=10)

            tk.Entry(date_frame, textvariable=self.year_var, width=6, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="年", font=entry_font).pack(side=tk.LEFT, padx=(2, 5))
            tk.Entry(date_frame, textvariable=self.month_var, width=4, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="月", font=entry_font).pack(side=tk.LEFT, padx=(2, 5))
            tk.Entry(date_frame, textvariable=self.day_var, width=4, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="日", font=entry_font).pack(side=tk.LEFT)

        # メモ
        if self.topic_control["pnormalcontrol"][3]:
            tk.Label(self.form, text="メモ", font=entry_font).grid(row=6, column=0, pady=10, sticky="ne")
            self.memo_text = tk.Text(self.form, width=32, height=5, font=("Arial", 12))
            self.memo_text.grid(row=6, column=1, padx=10, pady=10)
        else:
            self.memo_text = None


        #カスタム項目
        self.custom_labeltitles = load_custom_field_settings()["person_custom_labels"]
        self.custom_labels = []
        self.custom_vars = []

        for i in range(10):
            var = tk.StringVar()
            self.custom_vars.append(var)
            print(self.topic_control)
            if self.topic_control["pcustomcontrol"][i]:
                label = tk.Label(self.form, text=self.custom_labeltitles[i], font=entry_font)
                entry = tk.Entry(self.form, textvariable=var, font=entry_font)

                label.grid(row=7+i, column=0, pady=10, sticky="e")
                entry.grid(row=7+i, column=1, pady=10)

                self.custom_labels.append(label)
            else:
                self.custom_labels.append(None)  # 非表示なら None を入れておく
            
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
        group = self.group_var.get()
        job = self.job_var.get()
        year = self.year_var.get()
        month = self.month_var.get().zfill(2)
        day = self.day_var.get().zfill(2)
        date = f"{year}-{month}-{day}" if year and month and day else ""
        memo = self.memo_text.get("1.0", "end-1c") if self.memo_text else ""
        image_path = self.image_path_var.get()
        custom = []
        for i in range(10):
            custom.append(self.custom_vars[i].get())

        if not name:
            messagebox.showwarning("入力エラー", "名前は必須です。")
            return
        if not furigana:
            messagebox.showwarning("入力エラー", "ふりがなは必須です。")
            return

        # グループも渡す（add_personに対応している前提）
        add_person(name, furigana, group, job, date, memo, image_path, *custom)

        # フィールドクリア
        self.name_var.set("")
        self.furigana_var.set("")
        self.job_var.set("")
        self.group_var.set("")
        self.year_var.set("")
        self.month_var.set("")
        self.day_var.set("")
        for i in range(10):
            self.custom_vars[i].set("")
        if self.memo_text:
            self.memo_text.delete("1.0", "end")
        self.image_path_var.set("")

        messagebox.showinfo("登録成功", "人物情報を登録しました。")

        # ListFrameの更新
        if "PeopleListFrame" in self.controller.frames:
            self.controller.frames["PeopleListFrame"].refresh_list()
            
    def select_profile_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg")])
        if filepath:
            if not os.path.exists(IMAGE_DIR):
                os.makedirs(IMAGE_DIR)

            filename = os.path.basename(filepath)
            dest_path = os.path.join(IMAGE_DIR, filename)

            try:
                shutil.copy(filepath, dest_path)
                self.image_path_var.set(dest_path)
                messagebox.showinfo("画像選択", f"画像をコピーして保存しました: {dest_path}")
            except Exception as e:
                messagebox.showerror("エラー", f"画像コピー失敗: {e}")

            
    def refresh_labels(self):
        new_labels = load_custom_field_settings()["person_custom_labels"]
        for i in range(10):
            self.custom_labels[i]["text"] = new_labels[i]

    def refresh_fields(self):
        # 最新の設定とラベル名を取得
        self.topic_control = load_topicbool()
        self.custom_labeltitles = load_custom_field_settings()["person_custom_labels"]

        # カスタムフィールドの表示状態・ラベルを更新
        for i in range(10):
            is_visible = self.topic_control["pcustomcontrol"][i]
            label = self.custom_labels[i]
            entry_var = self.custom_vars[i]

            if is_visible:
                if label is None:
                    # ラベルとエントリーを新規作成して配置（self.formを使う）
                    label_widget = tk.Label(self.form, text=self.custom_labeltitles[i], font=("Arial", 15))
                    entry_widget = tk.Entry(self.form, textvariable=entry_var, font=("Arial", 15))
                    label_widget.grid(row=7+i, column=0, pady=10, sticky="e")
                    entry_widget.grid(row=7+i, column=1, pady=10)

                    self.custom_labels[i] = label_widget
                else:
                    # テキスト更新と再表示
                    label.config(text=self.custom_labeltitles[i])
                    label.grid()
            else:
                if label is not None:
                    label.grid_remove()


