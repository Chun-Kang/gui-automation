import time
import os
import pyautogui
import AppKit
import random

# -----------------------------
# 設定
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

button_sequence = [
    {"tag": "ok.png", "confidence": 0.8, "wait": 0.5},
    {"tag": "attack.png", "confidence": 0.8, "wait": 0.5},
    {"tag": "reload.png", "confidence": 0.8, "wait": 0.5},
    {"tag": "reload.png", "confidence": 0.8, "wait": 0.5},
    {"tag": "quest-list.png", "confidence": 0.8, "wait": 0.5},
    {"tag": "go-to-challenge.png", "confidence": 0.8, "wait": 0.5},
    {"tag": "challenge.png", "confidence": 0.8, "wait": 0.5},
]

VISUALIZE = True  # 原本用來畫紅框，先保留變數但不使用

# 取得螢幕 Retina 比例
screen = AppKit.NSScreen.screens()[0]
scale = screen.backingScaleFactor()
print(f"Retina 比例: {scale}")


# 可以修改這個數字，1~無限
repeat_count = 0


# -----------------------------
# 自動 focus AndApp
# -----------------------------
APP_NAME = "GranblueFantasyAndApp"
os.system(f'''osascript -e 'tell application "{APP_NAME}" to activate' ''')
time.sleep(0.8)  # 等待視窗 focus

print("程式 5 秒後開始...")
time.sleep(5)

# -----------------------------
# 模擬人為移動滑鼠
# -----------------------------
def human_like_move(button_center):
    x, y = button_center
    x = int(x / scale)
    y = int(y / scale)

    offset_range = 10  # 最多 ±10 像素

    x_offset = random.randint(-offset_range, offset_range)
    y_offset = random.randint(-offset_range, offset_range)

    x_click = x + x_offset
    y_click = y + y_offset

    print(f"點擊座標 (邏輯像素): x={x_click}, y={y_click}")
    duration = random.uniform(0.2, 0.5)  # 移動時間
    pyautogui.moveTo(x, y, duration=duration)

# -----------------------------
# 模擬人為點擊
# -----------------------------
def human_like_click(button_center):
    human_like_move(button_center)
    time.sleep(random.uniform(0.2, 1.0))  # 點擊前隨機延遲
    pyautogui.click()

# -----------------------------
# 點擊圖片
# -----------------------------
def click_image(image_path, confidence=0.9):
    # 最多等待 30 秒
    for _ in range(30):
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                button_center = pyautogui.center(location)
            break
        except pyautogui.ImageNotFoundException:
            # 如果找不到就繼續等待
            pass
            time.sleep(1)
            continue
        
    human_like_click(button_center)

# -----------------------------
# 外層循環流程
# -----------------------------

current_loop = 0
while  True:
    current_loop += 1
    if repeat_count != 0:
        print(f"\n=== 第 {current_loop} 次流程 ===")
        if current_loop > repeat_count:
            break
    else:
        print(f"\n=== 無限循環第 {current_loop} 次流程 ===")
        
    # -----------------------------
    # 自動化流程
    # -----------------------------
    for btn in button_sequence:
        img_name = btn["tag"]
        confidence = btn.get("confidence", 0.8)
        wait_after = btn.get("wait", 0.5)

        button_path = os.path.join(IMG_DIR, img_name)
        print(f"\n等待按鈕出現: {img_name} ...")
        button_center = None

        click_image(button_path, confidence=confidence)

        # 點擊後等待每個按鈕自訂時間
        time.sleep(wait_after)

print("\n自動化流程完成！")
