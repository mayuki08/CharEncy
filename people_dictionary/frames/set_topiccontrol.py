import tkinter as tk
from tkinter import messagebox, font
import json
from settings import load_topicbool, save_topicbool, load_custom_labels

SETTINGS_FILE = 'custom_fields.json'

class SetTopicControlFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        title_font = font.Font(family="Arial", size=30, weight="bold")
        entry_font = font.Font(family="Arial", size=15)

        self.settings = load_topicbool()
        self.custom_labels = load_custom_labels()

        tk.Label(self, text="フィールド表示設定", font=title_font).pack(pady=10)

        container = tk.Frame(self)
        container.pack()

        # チェックボックス変数辞書
        self.check_vars = {
            "pnormalcontrol": [],
            "pcustomcontrol": [],
            "tnormalcontrol": [],
            "tcustomcontrol": [],
        }

        normal_labels = {
            "pnormalcontrol": ["職業/肩書き", "グループ", "出会った日", "メモ", "画像"],
            "tnormalcontrol": ["場所", "時間", "相手", "メモ"]
        }

        for group_key in self.check_vars.keys():
            if "pnormal" in group_key:
                section_title = "人物：標準フィールド"
            elif "pcustom" in group_key:
                section_title = "人物：カスタムフィールド"
            elif "tnormal" in group_key:
                section_title = "タスク：標準フィールド"
            elif "tcustom" in group_key:
                section_title = "タスク：カスタムフィールド"
            else:
                section_title = group_key

            tk.Label(container, text=section_title, font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
            group_frame = tk.Frame(container)
            group_frame.pack(anchor="w", padx=20)

            values = self.settings.get(group_key, [])
            for i, val in enumerate(values):
                var = tk.BooleanVar(value=val)

                if "normal" in group_key:
                    label = normal_labels.get(group_key, [])[i] if i < len(normal_labels.get(group_key, [])) else f"{group_key}[{i+1}]"
                elif "pcustom" in group_key:
                    label = self.custom_labels["person_custom_labels"][i]
                elif "tcustom" in group_key:
                    label = self.custom_labels["task_custom_labels"][i]
                else:
                    label = f"{group_key}[{i+1}]"

                cb = tk.Checkbutton(group_frame, text=label, variable=var)
                cb.grid(row=i // 5, column=i % 5, sticky="w", padx=5, pady=2)
                self.check_vars[group_key].append(var)

        save_btn = tk.Button(self, text="保存", command=self.save_settings)
        save_btn.pack(pady=10)

        back_btn = tk.Button(self, text="← メニューに戻る",
                            command=lambda: controller.show_frame("SetMenuFrame"),
                            font=entry_font, relief="raised", bd=4, bg="#EEEEEE")
        back_btn.pack(pady=10)

    def save_settings(self):
        self.settings["pnormalcontrol"] = [var.get() for var in self.check_vars["pnormalcontrol"]]
        self.settings["pcustomcontrol"] = [var.get() for var in self.check_vars["pcustomcontrol"]]
        self.settings["tnormalcontrol"] = [var.get() for var in self.check_vars["tnormalcontrol"]]
        self.settings["tcustomcontrol"] = [var.get() for var in self.check_vars["tcustomcontrol"]]

        save_topicbool(self.settings)
        messagebox.showinfo("保存完了", "設定を保存しました。")

        main_app = getattr(self.controller, "main_app", None)
        if main_app:
            if "TaskRegisterFrame" in main_app.frames:
                main_app.frames["TaskRegisterFrame"].refresh_fields()
            if "PeopleRegisterFrame" in main_app.frames:
                main_app.frames["PeopleRegisterFrame"].refresh_fields()
