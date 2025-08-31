import json
import os
from tkinter import messagebox

SETTINGS_FILE = 'custom_fields.json'

def default_person_labels():
    return [f"カスタム{i+1}" for i in range(10)]

def default_task_labels():
    return [f"タスクカスタム{i+1}" for i in range(10)]

def load_custom_labels():
    """
    カスタムラベルをファイルから読み込む。
    ファイルが無ければデフォルトラベルを返す。
    """
    if not os.path.exists(SETTINGS_FILE):
        return {
            "person_custom_labels": default_person_labels(),
            "task_custom_labels": default_task_labels()
        }
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            person_labels = data.get("person_custom_labels", default_person_labels())
            task_labels = data.get("task_custom_labels", default_task_labels())
            return {
                "person_custom_labels": person_labels,
                "task_custom_labels": task_labels
            }
    except (json.JSONDecodeError, IOError) as e:
        messagebox.showerror("読み込みエラー", f"{SETTINGS_FILE} の読み込みに失敗しました。\n{e}")
        return {
            "person_custom_labels": default_person_labels(),
            "task_custom_labels": default_task_labels()
        }

def save_custom_labels(person_labels, task_labels):
    """
    カスタムラベルをファイルに保存する。
    既存データは保持しつつラベルのみ上書き。
    """
    data = {}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}

    data["person_custom_labels"] = person_labels
    data["task_custom_labels"] = task_labels

    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        messagebox.showerror("保存エラー", f"{SETTINGS_FILE} への保存に失敗しました。\n{e}")

def load_topicbool():
    """
    表示制御用のブール値設定を読み込む。
    ファイルがなければデフォルト設定を返す。
    """
    default_settings = {
        "pnormalcontrol": [True]*5,
        "pcustomcontrol": [False]*10,
        "tnormalcontrol": [True]*4,
        "tcustomcontrol": [False]*10
    }

    if not os.path.exists(SETTINGS_FILE):
        # ファイル無いのは正常ケースなのでメッセージは出さずデフォルト返す
        return default_settings

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 不足キーはデフォルトで補完
            for key, default_value in default_settings.items():
                if key not in data:
                    data[key] = default_value
            return data
    except (json.JSONDecodeError, IOError) as e:
        messagebox.showerror("読み込みエラー", f"{SETTINGS_FILE} の読み込みに失敗しました。\n{e}")
        return default_settings

def save_topicbool(settings_dict):
    """
    表示制御用ブール値設定を保存する。
    既存設定は保持しつつ更新。
    """
    data = {}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}

    data.update(settings_dict)

    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        messagebox.showerror("保存エラー", f"{SETTINGS_FILE} への保存に失敗しました。\n{e}")
