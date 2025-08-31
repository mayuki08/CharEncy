#frames/people_list.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
from database import get_all_people, search_people

class PeopleListFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        tk.Label(self, text="人物一覧（50音順）", font=("Arial", 16)).pack(pady=10)

        self.image_refs = []  # 保持用リストを初期化

        # 検索バー
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)

        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT)
        tk.Button(search_frame, text="検索", command=self.search).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="全件表示", command=self.refresh_list).pack(side=tk.LEFT)

        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.style = ttk.Style()
        self.style.theme_use("clam")  # "clam"はrowheight反映しやすいテーマの1つ

        self.style.configure("Custom.Treeview",
                            rowheight=120,
                            font=("Arial", 12))



        self.tree = ttk.Treeview(tree_frame, columns=("ID", "名前", "ふりがな", "グループ", "職業"), show="tree headings")
        self.tree.column("ID", width=0, stretch=False)  # ← 非表示
        self.tree.heading("ID", text="ID")
        self.tree.heading("#0", text="写真")
        self.tree.column("#0", width=60, anchor="center")  # 画像列

        for col in ("名前", "ふりがな", "グループ", "職業"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.configure(style="Custom.Treeview")

        scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

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
        self.controller.frames["PeopleDetailFrame"].set_person_id(person_id)
        self.controller.show_frame("PeopleDetailFrame")

    def search(self):
        keyword = self.search_var.get()
        if not keyword:
            messagebox.showinfo("検索", "キーワードを入力してください。")
            return

        people = search_people(keyword)
        self.display_grouped(people)
    
    def load_profile_image(self, path, size=(60, 60)):
        if not path or not os.path.exists(path):
            # ファイルが存在しないときはグレーのプレースホルダー画像
            return ImageTk.PhotoImage(Image.new("RGB", size, color="gray"))
        try:
            img = Image.open(path)
            img.thumbnail(size)
            return ImageTk.PhotoImage(img)
        except Exception:
            return ImageTk.PhotoImage(Image.new("RGB", size, color="gray"))

    def refresh_list(self):
        people = get_all_people()
        self.display_grouped(people)

    def display_grouped(self, people):
        self.image_refs.clear()  # ← 追加：古い画像参照をクリア
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
            self.tree.insert('', 'end', values=("", f"--- {group} ---", "", "", "", ""), tags=("group",))
            for p in persons:
                img = self.load_profile_image(p[7])
                self.image_refs.append(img)
                self.tree.insert('', 'end', image=img, values=(p[0], p[1], p[2], p[3], p[4]))

        if others:
            self.tree.insert('', 'end', values=("", "--- その他 ---", "", "", "", ""), tags=("group",))
            for p in others:
                img = self.load_profile_image(p[7])
                self.image_refs.append(img)
                self.tree.insert('', 'end', image=img, values=(p[0], p[1], p[2], p[3], p[4]))

#        for p in persons:
#            img = self.load_profile_image(p[7])  # p[7] が画像パスだと仮定
#            self.image_refs.append(img)  # GC対策
#            self.tree.insert('', 'end', image=img, values=(p[0], p[1], p[2], p[3], p[4]))

        self.tree.tag_configure("group", background="#f0f0f0", font=("Arial", 10, "bold"))
