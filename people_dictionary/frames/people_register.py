import tkinter as tk
from tkinter import messagebox, font, filedialog, ttk
import os
import shutil
import pykakasi
from database import add_person
from settings import load_topicbool, load_custom_labels

IMAGE_DIR = "images"

class PeopleRegisterFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.kks = pykakasi.kakasi()

        # 初期設定読み込み
        self.topic_control = load_topicbool()
        self.custom_labels = load_custom_labels()

        # 入力変数
        self.name_var = tk.StringVar()
        self.furigana_var = tk.StringVar()
        self.job_var = tk.StringVar()
        self.group_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.image_path_var = tk.StringVar()
        self.custom_vars = [tk.StringVar() for _ in range(10)]

        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # 中央寄せフレーム
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="人物登録", font=title_font).pack(pady=20)
        tk.Frame(center_frame, height=3, bg="black").pack(fill="x", padx=80, pady=(0, 50))

        self.form = tk.Frame(center_frame)
        self.form.pack(pady=5)

        # 画像選択ボタン（pnormalcontrol[4]想定）
        if len(self.topic_control.get("pnormalcontrol", [])) > 4 and self.topic_control["pnormalcontrol"][4]:
            btn_img = tk.Button(self.form, text="画像選択", font=entry_font, command=self.select_profile_image)
            btn_img.grid(row=0, column=1, pady=10, sticky="w")

        # 名前とふりがな（必須）
        tk.Label(self.form, text="名前 *", font=entry_font, fg="red").grid(row=1, column=0, sticky="e", pady=10)
        entry_name = tk.Entry(self.form, textvariable=self.name_var, font=entry_font)
        entry_name.grid(row=1, column=1, pady=10)
        entry_name.bind("<FocusOut>", self.auto_fill_furigana)

        tk.Label(self.form, text="ふりがな *", font=entry_font, fg="red").grid(row=2, column=0, sticky="e", pady=10)
        tk.Entry(self.form, textvariable=self.furigana_var, font=entry_font).grid(row=2, column=1, pady=10)

        # 職業/肩書き (pnormalcontrol[0])
        if len(self.topic_control.get("pnormalcontrol", [])) > 0 and self.topic_control["pnormalcontrol"][0]:
            tk.Label(self.form, text="職業/肩書き", font=entry_font).grid(row=3, column=0, sticky="e", pady=10)
            tk.Entry(self.form, textvariable=self.job_var, font=entry_font).grid(row=3, column=1, pady=10)

        # グループ (pnormalcontrol[1])
        if len(self.topic_control.get("pnormalcontrol", [])) > 1 and self.topic_control["pnormalcontrol"][1]:
            tk.Label(self.form, text="グループ", font=entry_font).grid(row=4, column=0, sticky="e", pady=10)
            group_options = ["家族", "友人", "仕事", "学校", "趣味"]
            self.group_cb = ttk.Combobox(self.form, textvariable=self.group_var, values=group_options,
                                         font=entry_font, width=29, state="normal")
            self.group_cb.grid(row=4, column=1, pady=10)

        # 出会った日 (pnormalcontrol[2])
        if len(self.topic_control.get("pnormalcontrol", [])) > 2 and self.topic_control["pnormalcontrol"][2]:
            tk.Label(self.form, text="出会った日", font=entry_font).grid(row=5, column=0, sticky="e", pady=10)
            date_frame = tk.Frame(self.form)
            date_frame.grid(row=5, column=1, pady=10)
            tk.Entry(date_frame, textvariable=self.year_var, width=6, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="年", font=entry_font).pack(side=tk.LEFT, padx=(2, 5))
            tk.Entry(date_frame, textvariable=self.month_var, width=4, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="月", font=entry_font).pack(side=tk.LEFT, padx=(2, 5))
            tk.Entry(date_frame, textvariable=self.day_var, width=4, font=entry_font).pack(side=tk.LEFT)
            tk.Label(date_frame, text="日", font=entry_font).pack(side=tk.LEFT)

        # メモ (pnormalcontrol[3])
        if len(self.topic_control.get("pnormalcontrol", [])) > 3 and self.topic_control["pnormalcontrol"][3]:
            tk.Label(self.form, text="メモ", font=entry_font).grid(row=6, column=0, sticky="ne", pady=10)
            self.memo_text = tk.Text(self.form, width=32, height=5, font=entry_font)
            self.memo_text.grid(row=6, column=1, padx=10, pady=10)
        else:
            self.memo_text = None

        # カスタム項目 (pcustomcontrol)
        start_row = 7
        self.custom_entries = []
        for i in range(10):
            visible = False
            if "pcustomcontrol" in self.topic_control:
                if i < len(self.topic_control["pcustomcontrol"]):
                    visible = self.topic_control["pcustomcontrol"][i]
            if visible:
                label_text = self.custom_labels.get("person_custom_labels", [f"custom{i+1}"]*10)[i]
                lbl = tk.Label(self.form, text=label_text, font=entry_font)
                lbl.grid(row=start_row + i, column=0, sticky="e", pady=10)
                entry = tk.Entry(self.form, textvariable=self.custom_vars[i], font=entry_font)
                entry.grid(row=start_row + i, column=1, pady=10)
                self.custom_entries.append((lbl, entry))
            else:
                self.custom_entries.append((None, None))

        # ホバーエフェクト関数
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        # 追加ボタン
        add_btn = tk.Button(center_frame, text="追加", font=entry_font, relief="raised", bd=4, bg="#EEEEEE",
                            command=self.add_person_gui)
        add_btn.pack(pady=10)
        add_btn.bind("<Enter>", on_enter)
        add_btn.bind("<Leave>", on_leave)

        # 戻るボタン
        back_btn = tk.Button(center_frame, text="← メニューに戻る", font=entry_font, relief="raised", bd=4, bg="#EEEEEE",
                             command=lambda: self.controller.show_frame("MenuFrame"))
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

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
        group = self.group_var.get()
        year = self.year_var.get()
        month = self.month_var.get().zfill(2)
        day = self.day_var.get().zfill(2)
        date = f"{year}-{month}-{day}" if year and month and day else ""
        memo = self.memo_text.get("1.0", "end-1c") if self.memo_text else ""
        image_path = self.image_path_var.get()
        custom = [var.get() for var in self.custom_vars]

        if not name:
            messagebox.showwarning("エラー", "名前は必須です。")
            return
        if not furigana:
            messagebox.showwarning("エラー", "ふりがなは必須です。")
            return

        add_person(name, furigana, group, job, date, memo, image_path, *custom)

        # フィールドクリア
        self.name_var.set("")
        self.furigana_var.set("")
        self.job_var.set("")
        self.group_var.set("")
        self.year_var.set("")
        self.month_var.set("")
        self.day_var.set("")
        self.image_path_var.set("")
        for var in self.custom_vars:
            var.set("")
        if self.memo_text:
            self.memo_text.delete("1.0", "end")

        messagebox.showinfo("追加完了", "人物を追加しました。")

        # 一覧画面に切り替え＆最新データ読み込み
        self.controller.frames["PeopleListFrame"].refresh_list()

    def select_profile_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            if not os.path.exists(IMAGE_DIR):
                os.makedirs(IMAGE_DIR)
            filename = os.path.basename(file_path)
            dest_path = os.path.join(IMAGE_DIR, filename)
            shutil.copy(file_path, dest_path)
            self.image_path_var.set(dest_path)

    def refresh_fields(self):
        """表示設定やラベル名変更があった時に呼び出し、表示を再構築する"""
        # 再読み込み
        self.topic_control = load_topicbool()
        self.custom_labels = load_custom_labels()
        self.build_ui()
