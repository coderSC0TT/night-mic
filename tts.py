import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
import threading
import queue
import keyboard
import ctypes

# ===================== 安全窗口激活 =====================
user32 = ctypes.WinDLL('user32', use_last_error=True)

def get_hwnd(root):
    return ctypes.windll.user32.GetParent(root.winfo_id())

def safe_force_focus(hwnd):
    user32.SetWindowPos(hwnd, -1, 0,0,0,0, 0x0002 | 0x0001)
    user32.SetForegroundWindow(hwnd)
    user32.SetFocus(hwnd)

# ===================== 查找VB-Cable =====================
def find_vb_cable_device():
    for i, dev in enumerate(sd.query_devices()):
        name = dev['name'].lower()
        if 'cable input' in name and dev['max_output_channels'] > 0:
            return i
    return None

VB_DEVICE = find_vb_cable_device()
TARGET_SAMPLE_RATE = 22050

task_queue = queue.Queue()
is_busy = False

# ===================== TTS =====================
def text_to_speech(text):
    try:
        temp_file = tempfile.mktemp(suffix=".wav")
        import pyttsx3
        engine = pyttsx3.init('sapi5')
        engine.setProperty("rate", 180)
        engine.setProperty("volume", 1.0)
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        engine.stop()
        with wave.open(temp_file, 'rb') as wf:
            data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
        os.remove(temp_file)
        return data
    except Exception as e:
        print("TTS Error:", e)
        return None

# ===================== 播放 =====================
def play_audio(data):
    try:
        sd.play(data, samplerate=TARGET_SAMPLE_RATE, device=VB_DEVICE)
        sd.wait()
    except:
        pass

# ===================== 后台线程 =====================
def worker():
    global is_busy
    while True:
        text = task_queue.get()
        is_busy = True
        result_label.config(text="发送中...")
        root.update()
        audio = text_to_speech(text)
        if audio is not None:
            play_audio(audio)
            result_label.config(text="✅ 已发送")
        else:
            result_label.config(text="❌ 失败")
        is_busy = False
        task_queue.task_done()

# ===================== 发送/隐藏逻辑 =====================
def send_or_hide():
    text = input_entry.get().strip()
    input_entry.delete(0, tk.END)
    
    if text and not is_busy and VB_DEVICE is not None:
        task_queue.put(text)
    elif VB_DEVICE is None:
        result_label.config(text="❌ 未找到VB-Cable")
    
    root.withdraw()

# ===================== 拖动 =====================
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_x() + event.x - root.x
    y = root.winfo_y() + event.y - root.y
    root.geometry(f"+{x}+{y}")

# ===================== 全局回车呼出 =====================
def on_global_enter():
    if root.state() == "normal":
        return
    hwnd = get_hwnd(root)
    root.deiconify()
    center_window()
    safe_force_focus(hwnd)
    input_entry.focus_force()
    root.after(50, lambda: input_entry.focus_force())

# ===================== 居中 =====================
def center_window():
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"+{x}+{y}")

# ===================== 界面 =====================
root = tk.Tk()
root.title("文字开麦")
root.geometry("220x65")  # 更小更扁
root.attributes("-topmost", True)
root.attributes("-alpha", 0.75)
root.overrideredirect(False)

root.bind("<ButtonPress-1>", start_move)
root.bind("<B1-Motion>", do_move)

# 只有输入框 + 状态提示，极度精简
input_entry = ttk.Entry(root, width=30, font=("微软雅黑", 9))
input_entry.pack(pady=(5, 1))

result_label = tk.Label(root, text="就绪", font=("微软雅黑", 8), fg="green")
result_label.pack(pady=(1, 4))

# 窗口内回车统一为：发送/隐藏
root.bind("<Return>", lambda e: send_or_hide())

# 启动后默认隐藏
root.withdraw()

threading.Thread(target=worker, daemon=True).start()

# 全局回车呼出
keyboard.add_hotkey("enter", on_global_enter)

root.mainloop()