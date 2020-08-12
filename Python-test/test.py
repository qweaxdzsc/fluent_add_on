import tkinter as tk
from tkinter import filedialog
import threading


def file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    # file_path = '54'
    data = {
        'path': file_path,
    }
    print(data)
# root.quit()


a = threading.Thread(target=file())
a.start()
print(a.is_alive())
b = threading.Thread(target=file())
b.start()
print(b.is_alive())