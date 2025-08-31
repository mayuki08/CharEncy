# settings.py
import json
import os
from tkinter import messagebox

SETTINGS_FILE = 'custom_fields.json'

def load_custom_labels():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "person_custom_labels": [f"カスタム{i+1}" for i in range(10)],
            "task_custom_labels": [f"タスクカスタム{i+1}" for i in range(10)]
        }
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_custom_labels(person_labels, task_labels):
    # 既存の設定を読み込む（なければ空辞書）
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}

    # ラベルだけ上書きし、他は残す
    data["person_custom_labels"] = person_labels
    data["task_custom_labels"] = task_labels

    # 保存
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_topicbool():
    if not os.path.exists(SETTINGS_FILE):
        messagebox.showerror("エラー", f"{SETTINGS_FILE} が見つかりません。")
        return {
            "pnormalcontrol": [False]*5,
            "pcustomcontrol": [False]*10,
            "tnormalcontrol": [False]*4,
            "tcustomcontrol": [False]*10
        }
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_topicbool(settings_dict):
    # 既存の設定を読み込む（なければ空辞書）
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # ブール値の設定だけ上書き
    data.update(settings_dict)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
