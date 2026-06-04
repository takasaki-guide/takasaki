import os
import tkinter as tk
from tkinter import filedialog, messagebox


def select_folder():
    selected = filedialog.askdirectory()
    if selected:
        folder_path_var.set(selected)


def rename_files():
    folder_path = folder_path_var.get()
    new_name = new_name_var.get().strip()

    # 入力チェック
    if not folder_path:
        messagebox.showerror("エラー", "フォルダを選択してください。")
        return

    if not new_name:
        messagebox.showerror("エラー", "新しいファイル名を入力してください。")
        return

    try:
        # フォルダ内のファイル一覧取得
        files = os.listdir(folder_path)

        # 対象拡張子
        valid_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".webp",
        )

        # 画像ファイルのみ抽出
        image_files = [
            f for f in files
            if f.lower().endswith(valid_extensions)
        ]

        # ファイル名順でソート
        image_files.sort()

        if not image_files:
            messagebox.showinfo(
                "情報",
                "選択されたフォルダに画像ファイルが見つかりませんでした。"
            )
            return

        # 仮ファイル名の存在チェック
        for f in os.listdir(folder_path):
            if f.startswith("__temp__"):
                messagebox.showerror(
                    "エラー",
                    "__temp__で始まるファイルが存在します。\n削除または名前変更してから再実行してください。"
                )
                return

        confirm = messagebox.askyesno(
            "確認",
            f"{len(image_files)}個の画像ファイルをリネームしますか？"
        )

        if not confirm:
            return

        # =========================
        # 第1段階：仮名へ変更
        # =========================
        temp_files = []

        for index, filename in enumerate(image_files, start=1):
            ext = os.path.splitext(filename)[1]

            temp_filename = f"__temp__{index}{ext}"

            old_path = os.path.join(folder_path, filename)
            temp_path = os.path.join(folder_path, temp_filename)

            os.rename(old_path, temp_path)

            temp_files.append(temp_filename)

        # =========================
        # 第2段階：最終名へ変更
        # =========================
        for index, temp_filename in enumerate(temp_files, start=1):
            ext = os.path.splitext(temp_filename)[1]

            final_filename = f"{new_name}{index}{ext}"

            temp_path = os.path.join(folder_path, temp_filename)
            final_path = os.path.join(folder_path, final_filename)

            os.rename(temp_path, final_path)

        messagebox.showinfo(
            "完了",
            f"{len(temp_files)}個の画像ファイルをリネームしました。"
        )

    except Exception as e:
        messagebox.showerror(
            "エラー",
            f"エラーが発生しました。\n\n{str(e)}"
        )


# =========================
# UI設定
# =========================

root = tk.Tk()
root.title("画像ファイル一括リネームツール")
root.geometry("500x200")
root.resizable(False, False)

folder_path_var = tk.StringVar()
new_name_var = tk.StringVar()

# フォルダ選択
lbl_folder = tk.Label(
    root,
    text="1. 書き換えるフォルダを選択してください"
)
lbl_folder.pack(anchor="w", padx=20, pady=(15, 2))

frame_folder = tk.Frame(root)
frame_folder.pack(fill="x", padx=20)

entry_folder = tk.Entry(
    frame_folder,
    textvariable=folder_path_var,
    width=45,
    state="readonly"
)
entry_folder.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5)
)

btn_browse = tk.Button(
    frame_folder,
    text="参照...",
    command=select_folder
)
btn_browse.pack(side="right")

# 新しいファイル名
lbl_name = tk.Label(
    root,
    text="2. 新しいファイル名（後ろに1からの連番がつきます）"
)
lbl_name.pack(anchor="w", padx=20, pady=(15, 2))

entry_name = tk.Entry(
    root,
    textvariable=new_name_var,
    width=50
)
entry_name.pack(fill="x", padx=20)

# 空白
tk.Label(root, text="").pack(pady=2)

# 実行ボタン
btn_execute = tk.Button(
    root,
    text="一括リネームを実行する",
    bg="#1f77b4",
    fg="white",
    font=("Arial", 10, "bold"),
    command=rename_files
)
btn_execute.pack(
    fill="x",
    padx=20,
    ipady=5
)

# 起動
root.mainloop()