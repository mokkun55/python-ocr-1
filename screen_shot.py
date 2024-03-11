# システムの利用を宣言する
import os
import sys

# PyOCRを読み込む
from PIL import Image
import pyocr
from pyocr.builders import TextBuilder
import tkinter as tk
import time
import pyautogui

# Tesseractのインストール場所をOSに教える
tesseract_path = "C:\Program Files\Tesseract-OCR"
if tesseract_path not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + tesseract_path

# OCRエンジンを取得する
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("OCRエンジンが指定されていません")
    sys.exit(1)
else:
    tool = tools[0]

def ocr(img_path):
    img = Image.open(img_path)

    # 文字を読み取る
    builder = TextBuilder(tesseract_layout=6)
    result = tool.image_to_string(img, lang="jpn", builder=builder)

    return result

def select_window_region():
    root = tk.Tk()
    root.attributes('-alpha', 0.5)  # ウィンドウを半透明に設定

    def on_click_apply():
        global x, y, w, h
        x = root.winfo_x()
        y = root.winfo_y()
        w = root.winfo_width()
        h = root.winfo_height()

    button = tk.Button(root, text="適応", command=on_click_apply)
    button.pack()

    root.mainloop()

# 範囲選択ウィンドウを表示
select_window_region()

# 指定した範囲のスクリーンショットを取得する
timestamp = time.strftime("%Y%m%d%H%M%S")
screenshot = pyautogui.screenshot(region=(x, y, w, h))
screenshot.save(f"screenshot_{timestamp}.png")

# OCRでテキストを抽出
extracted_text = ocr(f"screenshot_{timestamp}.png")

# テキストをtxtファイルに保存
with open("extracted_text.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(extracted_text)

print("テキストを抽出して extracted_text.txt に保存しました。")
