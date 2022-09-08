import numpy as np
import tkinter as tk
import random
import time
import threading
import pandas as pd
import os
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime


counter = 0
running = False
cps = 0
cpm = 0
wpm = 0
wps = 0


def startfn(event):
    global running
    if not running:
        if not event.keycode in [16, 17, 18]:
            running = True
            t = threading.Thread(target=time_thread)
            t.start()

    if not sample_label.cget("text").startswith(input_entry.get()):
        input_entry.config(fg="red")
    else:
        input_entry.config(fg="black")
    if input_entry.get() == sample_label.cget("text")[:-1]:
        running = False
        input_entry.config(fg="green")


def resetfn(event=None):
    global running
    global counter
    running = False
    counter = 0
    speed_label.config(text="Speed: \n0.00 cps\n0.00 cpm\n0.00 wps\n0.00 wpm")
    sample_label.config(text=rtext(text))
    input_entry.delete(0, tk.END)


def deletefn():
    if "save.txt" in os.listdir():
        os.remove("save.txt")
        resetfn()

    with open("save.txt", "w") as f:
        f.write("")
        f.close()


def time_thread():
    global counter
    global wps
    global wpm
    global cps
    global cpm

    while running:
        time.sleep(0.1)
        counter += 0.1
        cps = len(input_entry.get()) / counter
        cpm = cps * 60
        wps = len(input_entry.get().split(" ")) / counter
        wpm = wps * 60
        speed_label.config(
            text=f"Speed: \n{cps:.2f} cps\n{cpm:.2f} cpm\n{wps:.2f} wps\n{wpm:.2f} wpm"
        )


def rtext(text):
    res = []
    for i in range(10):
        res.append(random.choice(text))

    rr = [x + " " for x in res]
    rr[-1] = rr[-1].replace(" ", "")
    return "".join(rr)


df = pd.DataFrame(columns=["Time", "CPS", "CPM", "WPS", "WPM"])


def savefn(event=None):
    global df
    df.loc[0] = [
        datetime.now().strftime("%H:%M:%S"),
        round(cps, 2),
        round(cpm, 2),
        round(wps, 2),
        round(wpm, 2),
    ]
    # write df to file
    if ("save.txt" in os.listdir() and os.stat("save.txt").st_size == 0) or not (
        "save.txt" in os.listdir()
    ):
        df.to_csv("save.txt", index=True, header=True)
    else:
        df.to_csv("save.txt", index=True, header=False, mode="a")
    resetfn()


def displayfn():
    dff = pd.read_csv("save.txt")
    window = tk.Tk()
    window.title("Score Graph")
    window.geometry("1000x500")
    window.resizable(False, False)
    window.bind("<Escape>", lambda e: window.destroy())
    window.config(bg="white")
    # plot matplotlib graph of data read from save.txt
    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(np.arange(0, len(dff)), dff["CPM"], label="CPM")
    ax.plot(np.arange(0, len(dff)), dff["WPM"], label="WPM")
    ax.legend()
    ax.set_xlabel("Time")
    ax.set_ylabel("Score")
    ax.set_title("Score Graph")
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()
    window.mainloop()


root = tk.Tk()

# run root
root.title("test")
root.geometry("1200x600")


text = open("text.txt", "r").read().split("\n")
frame = tk.Frame(root)

sample_label = tk.Label(frame, text=rtext(text), font=("Helvetica", 24))
sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

input_entry = tk.Entry(frame, width=40, font=("Helvetica", 24))
input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
input_entry.bind("<KeyPress>", startfn)
input_entry.bind("<Return>", savefn)
input_entry.bind("<Tab>", resetfn)

speed_label = tk.Label(
    frame,
    text="Speed: \n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPS",
    font=("Helventica", 18),
)
speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

reset_button = tk.Button(frame, text="Reset", font=("Helvetica", 24), command=resetfn)
reset_button.grid(row=3, column=0, columnspan=1, padx=5, pady=10)

save_button = tk.Button(frame, text="Save", font=("Helvetica", 24), command=savefn)
save_button.grid(row=3, column=1, columnspan=1, padx=5, pady=10)

display_score = tk.Button(
    frame, text="Display Score", font=("Helvetica", 24), command=displayfn
)
display_score.grid(row=4, column=0, columnspan=1, padx=5, pady=10)

delete_score = tk.Button(
    frame, text="Delete Score", font=("Helvetica", 24), command=deletefn
)
delete_score.grid(row=4, column=1, columnspan=1, padx=5, pady=10)
frame.pack(expand=True)

root.mainloop()
