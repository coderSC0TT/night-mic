# coding=gbk
import tkinter as tk
from tkinter import ttk
import threading
import queue
import ctypes

from config import OPEN_HOTKEY, QUICK_MSGS
from audio import text_to_speech, play_audio, VB_DEVICE
from hotkey import register_hotkeys, is_busy, set_queue

user32 = ctypes.WinDLL('user32', use_last_error=True)

def get_hwnd(root):
    return ctypes.windll.user32.GetParent(root.winfo_id())

def safe_force_focus(hwnd):
    user32.SetWindowPos(hwnd, -1, 0,0,0,0, 0x0002 | 0x0001)
    user32.SetForegroundWindow(hwnd)
    user32.SetFocus(hwnd)

task_queue = queue.Queue()

def worker():
    global is_busy
    while True:
        text = task_queue.get()
        is_busy = True
        result_label.config(text="播放中...")
        audio = text_to_speech(text)
        if audio is not None:
            play_audio(audio)
            result_label.config(text="? 完成")
        else:
            result_label.config(text="? 失败")
        is_busy = False
        task_queue.task_done()

def send_or_hide():
    text = input_entry.get().strip()
    input_entry.delete(0, tk.END)
    if text and not is_busy and VB_DEVICE is not None:
        task_queue.put(text)
    root.withdraw()

def on_global_open():
    if root.state() == "normal":
        return
    hwnd = get_hwnd(root)
    root.deiconify()
    center_window()
    safe_force_focus(hwnd)
    input_entry.focus_force()

def center_window():
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")

def start_move(e):
    root.x, root.y = e.x, e.y

def do_move(e):
    x = root.winfo_x() + e.x - root.x
    y = root.winfo_y() + e.y - root.y
    root.geometry(f"+{x}+{y}")

# ==================== 界面 ====================
root = tk.Tk()
root.title("文字开麦")
root.geometry("290x140")
root.attributes("-topmost", True)
root.attributes("-alpha", 0.85)
root.overrideredirect(False)

root.bind("<ButtonPress-1>", start_move)
root.bind("<B1-Motion>", do_move)

input_entry = ttk.Entry(root, width=38, font=("微软雅黑", 9))
input_entry.pack(pady=(4, 1))

result_label = tk.Label(root, text="就绪", font=("微软雅黑", 8), fg="green")
result_label.pack(pady=(1, 2))

key_frame = tk.Frame(root)
key_frame.pack(pady=2)
tk.Label(key_frame, text=f"呼出: {OPEN_HOTKEY}", font=("微软雅黑",7), fg="#0066cc").grid(row=0,column=0,columnspan=3)

for idx, (hk, txt) in enumerate(QUICK_MSGS.items()):
    tk.Label(key_frame, text=f"{hk}:{txt}", font=("微软雅黑",7)).grid(row=1+idx//3, column=idx%3, padx=3)

root.bind("<Return>", lambda e: send_or_hide())
root.withdraw()

threading.Thread(target=worker, daemon=True).start()

set_queue(task_queue)
register_hotkeys(on_global_open, OPEN_HOTKEY, QUICK_MSGS)

root.mainloop()