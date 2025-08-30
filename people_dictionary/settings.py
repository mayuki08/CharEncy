# settings.py
import json
import os

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
    data = {
        "person_custom_labels": person_labels,
        "task_custom_labels": task_labels
    }
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)