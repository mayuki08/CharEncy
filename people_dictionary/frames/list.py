# frames/list.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_people, search_people

class ListFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="人物一覧（50音順）", font=("Arial", 16)).pack(pady=10)

        # 検索バー
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)

        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT)
        tk.Button(search_frame, text="検索", command=self.search).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="全件表示", command=self.refresh_list).pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=("ID", "名前", "ふりがな", "職業"), show="headings")
        for col in ("ID", "名前", "ふりがな", "職業"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="選択した人物の詳細を見る", command=self.show_detail).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="← メニューに戻る", command=lambda: controller.show_frame("MenuFrame")).pack(side=tk.LEFT)

        self.refresh_list()


    def show_detail(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("選択エラー", "人物を選択してください。")
            return
        item = self.tree.item(selected[0])
        values = item['values']

        # グループ行は無視
        if not isinstance(values[0], int):
            messagebox.showinfo("情報", "人物を選択してください。")
            return

        person_id = values[0]
        self.controller.frames["DetailFrame"].set_person_id(person_id)
        self.controller.show_frame("DetailFrame")
    def search(self):
        keyword = self.search_var.get()
        if not keyword:
            messagebox.showinfo("検索", "キーワードを入力してください。")
            return

        people = search_people(keyword)
        self.display_grouped(people)
    
    def refresh_list(self):
        people = get_all_people()
        self.display_grouped(people)

    def display_grouped(self, people):
        self.tree.delete(*self.tree.get_children())
        people = sorted(people, key=lambda x: x[2])  # ふりがなでソート

        kana_groups = {
            "あ行": "あいうえお",
            "か行": "かがきぎくぐけげこご",
            "さ行": "さざしじすずせぜそぞ",
            "た行": "ただちぢつづてでとど",
            "な行": "なにぬねの",
            "は行": "はばぱひびぴふぶぷへべぺほぼぽ",
            "ま行": "まみむめも",
            "や行": "やゆよ",
            "ら行": "らりるれろ",
            "わ行": "わをん"
        }

        grouped = {k: [] for k in kana_groups}
        others = []

        for person in people:
            furigana = person[2]
            if not furigana:
                others.append(person)
                continue

            first = furigana[0]
            found = False
            for group, chars in kana_groups.items():
                if first in chars:
                    grouped[group].append(person)
                    found = True
                    break
            if not found:
                others.append(person)

        for group, persons in grouped.items():
            if not persons:
                continue
            self.tree.insert('', 'end', values=(f"--- {group} ---", "", "", ""), tags=("group",))
            for p in persons:
                self.tree.insert('', 'end', values=p)

        if others:
            self.tree.insert('', 'end', values=("--- その他 ---", "", "", ""), tags=("group",))
            for p in others:
                self.tree.insert('', 'end', values=p)

        self.tree.tag_configure("group", background="#f0f0f0", font=("Arial", 10, "bold"))