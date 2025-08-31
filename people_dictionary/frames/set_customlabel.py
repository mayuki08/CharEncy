import tkinter as tk
from tkinter import font, messagebox
import json
import os

SETTINGS_FILE = "custom_fields.json"

def load_custom_field_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "person_custom_labels": [f"custom{i+1}" for i in range(10)],
            "task_custom_labels": [f"custom{i+1}" for i in range(10)],
            "pnormalcontrol": [True, True, True, True, True],
            "pcustomcontrol": [False]*10,
            "tnormalcontrol": [True, True, True, True],
            "tcustomcontrol": [False]*10,
        }

def save_custom_field_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

class CustomLabelFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.people_fields_vars = [tk.StringVar() for _ in range(10)]
        self.task_fields_vars = [tk.StringVar() for _ in range(10)]

        self.build_ui()

        # Load saved settings
        self.load_settings()

    def build_ui(self):
        title_font = font.Font(family="Arial", size=24, weight="bold")
        label_font = font.Font(family="Arial", size=14)

        tk.Label(self, text="カスタム項目名の設定", font=title_font).pack(pady=20)

        content = tk.Frame(self)
        content.pack()

        # --- 人物用 ---
        people_frame = tk.LabelFrame(content, text="人物カスタム項目", font=label_font, padx=10, pady=10)
        people_frame.grid(row=0, column=0, padx=20)

        for i, var in enumerate(self.people_fields_vars):
            tk.Label(people_frame, text=f"custom{i+1}", font=label_font).grid(row=i, column=0, sticky="e", padx=5, pady=3)
            tk.Entry(people_frame, textvariable=var, width=25).grid(row=i, column=1, padx=5, pady=3)

        # --- タスク用 ---
        task_frame = tk.LabelFrame(content, text="タスクカスタム項目", font=label_font, padx=10, pady=10)
        task_frame.grid(row=0, column=1, padx=20)

        for i, var in enumerate(self.task_fields_vars):
            tk.Label(task_frame, text=f"custom{i+1}", font=label_font).grid(row=i, column=0, sticky="e", padx=5, pady=3)
            tk.Entry(task_frame, textvariable=var, width=25).grid(row=i, column=1, padx=5, pady=3)

        # 保存ボタン
        save_btn = tk.Button(self, text="保存する", font=label_font, width=20, command=self.save_settings)
        save_btn.pack(pady=20)

        # 戻るボタン
        back_btn = tk.Button(self, text="← メニューに戻る", font=label_font, command=lambda: self.controller.show_frame("SetMenuFrame"))
        back_btn.pack()

    def load_settings(self):
        data = load_custom_field_settings()
        for i, name in enumerate(data.get("person_custom_labels", [])):
            if i < 10:
                self.people_fields_vars[i].set(name)
        for i, name in enumerate(data.get("task_custom_labels", [])):
            if i < 10:
                self.task_fields_vars[i].set(name)

    def save_settings(self):
        data = load_custom_field_settings()  # 現状の全データを読み込み

        # 更新する項目だけ差し替え
        data["person_custom_labels"] = [var.get().strip() or f"custom{i+1}" for i, var in enumerate(self.people_fields_vars)]
        data["task_custom_labels"] = [var.get().strip() or f"custom{i+1}" for i, var in enumerate(self.task_fields_vars)]

        save_custom_field_settings(data)
        messagebox.showinfo("保存完了", "カスタム項目名を保存しました。")

        # 即時反映
        main_app = getattr(self.controller, "main_app", None)
        if main_app:
            if "PeopleRegisterFrame" in main_app.frames:
                main_app.frames["PeopleRegisterFrame"].refresh_fields()
            if "PeopleEditFrame" in main_app.frames:
                main_app.frames["PeopleEditFrame"].refresh_fields()