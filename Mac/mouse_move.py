import os
import random
import time
import pyautogui
import platform

# 设置终端类型，避免 "TERM environment variable not set" 报错
os.environ['TERM'] = 'vt100'

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

screen_width, screen_height = pyautogui.size()

try:
    while True:
        countdown = 90
        while countdown > 0:
            clear_screen()
            print(f"Will move mouse in {countdown} seconds...")
            time.sleep(1)
            countdown -= 1

        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        pyautogui.moveTo(x, y, duration=1)

        if platform.system() == "Darwin":
            os.system(
                'osascript -e \'display notification "鼠标已移动" with title "提示" sound name "Glass"\''
            )

except KeyboardInterrupt:
    print("\n程序已终止。")
