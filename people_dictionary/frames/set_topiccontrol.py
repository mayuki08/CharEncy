# frames/set_topiccontrol.py
import tkinter as tk
from tkinter import messagebox, font
import json
from settings import load_topicbool, save_topicbool, load_custom_labels

SETTINGS_FILE = 'custom_fields.json'

class SetTopicControlFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # --- フォント設定 ---
        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        # --- 中央揃え用フレーム ---
        center_frame = tk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ホバーエフェクト
        def on_enter(e): e.widget['background'] = '#F1F1F1'
        def on_leave(e): e.widget['background'] = '#EEEEEE'

        # 表示設定データとカスタムラベルを読み込む
        self.settings = load_topicbool()
        self.custom_labels = load_custom_labels()

        # チェックボックス変数
        self.check_vars = {
            "pnormalcontrol": [],
            "pcustomcontrol": [],
            "tnormalcontrol": [],
            "tcustomcontrol": [],
        }

        # normal系グループのラベル
        normal_labels = {
            "pnormalcontrol": ["職業/肩書き", "グループ", "出会った日", "メモ", "画像"],
            "tnormalcontrol": ["場所", "時間", "相手", "メモ"]
        }

        tk.Label(self, text="フィールド表示設定", font=("Arial", 16, "bold")).pack(pady=10)

        container = tk.Frame(self)
        container.pack()

        for group in self.check_vars.keys():
            # 見出しラベル（グループ名）
            if "pnormal" in group:
                section_title = "人物：標準フィールド"
            elif "pcustom" in group:
                section_title = "人物：カスタムフィールド"
            elif "tnormal" in group:
                section_title = "タスク：標準フィールド"
            elif "tcustom" in group:
                section_title = "タスク：カスタムフィールド"
            else:
                section_title = group

            tk.Label(container, text=section_title, font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
            group_frame = tk.Frame(container)
            group_frame.pack(anchor="w", padx=20)

            values = self.settings.get(group, [])
            for i, val in enumerate(values):
                var = tk.BooleanVar(value=val)

                # ラベルテキストの選択
                if "normal" in group:
                    label = normal_labels.get(group, [])[i] if i < len(normal_labels.get(group, [])) else f"{group}[{i+1}]"
                elif "pcustom" in group:
                    label = self.custom_labels["person_custom_labels"][i]
                elif "tcustom" in group:
                    label = self.custom_labels["task_custom_labels"][i]
                else:
                    label = f"{group}[{i+1}]"

                cb = tk.Checkbutton(group_frame, text=label, variable=var)
                cb.grid(row=i // 5, column=i % 5, sticky="w", padx=5, pady=2)
                self.check_vars[group].append(var)

        # 保存ボタン
        save_btn = tk.Button(self, text="保存", command=self.save_settings)
        save_btn.pack(pady=10)
        save_btn.bind("<Enter>", on_enter)
        save_btn.bind("<Leave>", on_leave)

        back_btn = tk.Button(center_frame, text="← メニューに戻る",
        command=lambda: controller.show_frame("SetMenuFrame"),
                        font=entry_font, relief="raised", bd=4, bg="#EEEEEE")
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    def save_settings(self):
        self.settings["pnormalcontrol"] = [var.get() for var in self.check_vars["pnormalcontrol"]]
        self.settings["pcustomcontrol"] = [var.get() for var in self.check_vars["pcustomcontrol"]]
        self.settings["tnormalcontrol"] = [var.get() for var in self.check_vars["tnormalcontrol"]]
        self.settings["tcustomcontrol"] = [var.get() for var in self.check_vars["tcustomcontrol"]]

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("保存完了", "設定を保存しました。")

        # 即時反映
        if "TaskRegisterFrame" in self.controller.main_app.frames:
            self.controller.main_app.frames["TaskRegisterFrame"].refresh_fields()
        if "PeopleRegisterFrame" in self.controller.main_app.frames:
            self.controller.main_app.frames["PeopleRegisterFrame"].refresh_fields()

