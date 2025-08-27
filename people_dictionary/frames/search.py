# frames/search.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import search_people, get_all_people

class SearchFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.search_var = tk.StringVar()

        tk.Label(self, text="人物検索", font=("Arial", 16)).pack(pady=10)

        search_box = tk.Frame(self)
        search_box.pack(pady=5)

        tk.Entry(search_box, textvariable=self.search_var).pack(side=tk.LEFT)
        tk.Button(search_box, text="検索", command=self.search).pack(side=tk.LEFT)
        tk.Button(search_box, text="全て表示", command=self.refresh_list).pack(side=tk.LEFT)
        
        index_frame = tk.Frame(self)
        index_frame.pack(pady=5)

        tk.Label(index_frame, text="並び替え:").pack(side=tk.LEFT)

        # 数字
        tk.Button(index_frame, text="0-9", width=3,
                command=lambda: self.sort_by_prefix_group("0-9")).pack(side=tk.LEFT, padx=1)

        # 英字 A〜Z
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            tk.Button(index_frame, text=char, width=2,
                    command=lambda c=char: self.sort_by_prefix_group(c)).pack(side=tk.LEFT, padx=1)
        
        kana_frame = tk.Frame(self)
        kana_frame.pack(pady=5)

        for kana in ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ"]:
            tk.Button(kana_frame, text=kana + "行", width=4,
                    command=lambda k=kana: self.sort_by_prefix_group(k)).pack(side=tk.LEFT, padx=2)



        self.tree = ttk.Treeview(self, columns=("ID", "名前", "職業", "出会った日"), show="headings")
        for col in ("ID", "名前", "職業", "出会った日"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        tk.Button(self, text="選択した人物の詳細を見る", command=self.show_detail).pack(pady=5)
        tk.Button(self, text="← メニューに戻る", command=lambda: controller.show_frame("MenuFrame")).pack()

        self.refresh_list()

    def search(self):
        keyword = self.search_var.get()
        results = search_people(keyword)
        self.tree.delete(*self.tree.get_children())
        for person in results:
            self.tree.insert('', tk.END, values=person)

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for person in get_all_people():
            self.tree.insert('', tk.END, values=person)

    def show_detail(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("選択エラー", "人物を選択してください。")
            return

        person_id = self.tree.item(selected[0])['values'][0]
        self.controller.frames["DetailFrame"].set_person_id(person_id)
        self.controller.show_frame("DetailFrame")
        
    def sort_by_prefix_group(self, group):
        """名前の先頭文字によるグループソート（50音・英字・数字）"""
        group_map = {
            "0-9": "0123456789",
            "A": "Aa",
            "B": "Bb",
            "C": "Cc",
            "D": "Dd",
            "E": "Ee",
            "F": "Ff",
            "G": "Gg",
            "H": "Hh",
            "I": "Ii",
            "J": "Jj",
            "K": "Kk",
            "L": "Ll",
            "M": "Mm",
            "N": "Nn",
            "O": "Oo",
            "P": "Pp",
            "Q": "Qq",
            "R": "Rr",
            "S": "Ss",
            "T": "Tt",
            "U": "Uu",
            "V": "Vv",
            "W": "Ww",
            "X": "Xx",
            "Y": "Yy",
            "Z": "Zz",
            "あ": "あいうえお",
            "か": "かがきぎくぐけげこご",
            "さ": "さざしじすずせぜそぞ",
            "た": "ただちぢつづてでとど",
            "な": "なにぬねの",
            "は": "はばぱひびぴふぶぷへべぺほぼぽ",
            "ま": "まみむめも",
            "や": "やゆよ",
            "ら": "らりるれろ",
            "わ": "わをん"
        }

        prefix_chars = group_map.get(group, "")
        people = get_all_people()

        def sort_key(person):
            name = person[1]
            if not name:
                return (2, "")  # 空白名は最下位
            return (0 if name[0] in prefix_chars else 1, name)

        sorted_people = sorted(people, key=sort_key)

        self.tree.delete(*self.tree.get_children())
        for person in sorted_people:
            self.tree.insert('', tk.END, values=person)
