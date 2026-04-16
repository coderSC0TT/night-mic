# coding=gbk
import keyboard

is_busy = False
task_queue = None

def set_queue(q):
    global task_queue
    task_queue = q

def trigger_text(text):
    if not is_busy and text.strip():
        task_queue.put(text.strip())

def register_hotkeys(open_callback, open_hotkey, quick_msgs):
    try:
        keyboard.add_hotkey(open_hotkey, open_callback)
        print()
    except:
        print()

    for hk, text in quick_msgs.items():
        try:
            keyboard.add_hotkey(hk, lambda t=text: trigger_text(t))
            print(f"? {hk} -> {text}")
        except:
            print(f"? {hk} 注册失败")