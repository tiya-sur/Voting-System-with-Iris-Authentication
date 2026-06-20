import tkinter as tk
import threading
import queue
import activity_detection

def start_detection():
    global result_queue
    result_queue = queue.Queue()
    ml_thread = threading.Thread(target=activity_detection.run_detection, args=(result_queue,))
    ml_thread.daemon = True
    ml_thread.start()
    update_results()

def update_results():
    try:
        result = result_queue.get_nowait()
        result_label.config(text=result)
    except queue.Empty:
        pass
    root.after(100, update_results)

root = tk.Tk()
start_button = tk.Button(root, text="Start Detection", command=start_detection)
start_button.pack()
result_label = tk.Label(root, text="")
result_label.pack()
root.mainloop()