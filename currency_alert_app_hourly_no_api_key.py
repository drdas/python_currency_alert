import json
import requests
import threading
import time
import tkinter as tk
from tkinter import messagebox
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
#from win10toast import ToastNotifier
from win10toast_click import ToastNotifier

import schedule
import os
import win32event
import win32api
import winerror
import sys

mutex = win32event.CreateMutex(None, False, "Global\\FXAlertMutex")

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    print("Another instance is already running.")
    sys.exit(0)

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "pair": ["USD", "JPY"],
    "low": 140.0,
    "high": 160.0,
    "interval": 15
}

notifier = ToastNotifier()
running = True
job_ref = None
icon = None
icons = {}  # will hold red and blue icon images

# --- Config ---
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

# --- Icons ---
def create_icon(color):
    img = Image.new('RGB', (64, 64), color=color)
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill='white')
    return img

icons['blue'] = create_icon((0, 100, 255))
icons['red'] = create_icon((200, 0, 0))

# --- FX Check ---
def run_check():
    config = load_config()
    base, target = config["pair"]
    api_key = "GET_API_KEY_FROM_PROVIDER"  # Replace with your actual key

    # Alpha Vantage FX quote endpoint
    url = (
        f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
        f"&from_currency={base}&to_currency={target}&apikey={api_key}"
    )

    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if "Realtime Currency Exchange Rate" not in data:
            print(f"Error: Unexpected API response — {data}")
            return

        rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        print(f"{base}->{target} rate: {rate}")

        # Tooltip + icon color
        if rate < config["low"] or rate > config["high"]:
            status = "ALERT"
            icon.icon = icons["red"]
            icon.title = f"{base}→{target}: {rate:.2f} ({status})"

            notifier.show_toast(
                f"FX Alert: {base}→{target}",
                f"Rate {rate:.2f} outside {config['low']}–{config['high']}",
                duration=10,
                threaded=False
            )
        else:
            status = "OK"
            icon.icon = icons["blue"]
            icon.title = f"{base}→{target}: {rate:.2f} ({status})"

    except Exception as e:
        print(f"Error fetching rate: {e}")

# --- Schedule ---
def reload_job():
    global job_ref
    config = load_config()

    if job_ref:
        schedule.cancel_job(job_ref)

    job_ref = schedule.every(config["interval"]).minutes.do(run_check)

def job_loop():
    reload_job()
    while running:
        schedule.run_pending()
        time.sleep(1)

# --- Tray Menu ---
def on_exit(icon_, item):
    global running
    running = False
    icon_.stop()

def open_settings(icon_, item):
    cfg = load_config()

    def save():
        try:
            cfg["pair"][0] = base_var.get().upper()
            cfg["pair"][1] = target_var.get().upper()
            cfg["low"] = float(low_var.get())
            cfg["high"] = float(high_var.get())
            cfg["interval"] = int(interval_var.get())
            save_config(cfg)
            reload_job()
            run_check()  # immediately refresh display
            messagebox.showinfo("Saved", "Settings updated.")
            settings.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    settings = tk.Tk()
    settings.title("FX Alert Settings")
    settings.geometry("300x300")

    # Force window to the front and enable focus
    settings.lift()
    settings.attributes('-topmost', True)
    settings.after_idle(settings.attributes, '-topmost', False)
    settings.focus_force()

    base_var = tk.StringVar(value=cfg["pair"][0])
    target_var = tk.StringVar(value=cfg["pair"][1])
    low_var = tk.StringVar(value=cfg["low"])
    high_var = tk.StringVar(value=cfg["high"])
    interval_var = tk.StringVar(value=cfg["interval"])

    tk.Label(settings, text="Base Currency").pack()
    tk.Entry(settings, textvariable=base_var).pack()
    tk.Label(settings, text="Target Currency").pack()
    tk.Entry(settings, textvariable=target_var).pack()
    tk.Label(settings, text="Low Limit").pack()
    tk.Entry(settings, textvariable=low_var).pack()
    tk.Label(settings, text="High Limit").pack()
    tk.Entry(settings, textvariable=high_var).pack()
    tk.Label(settings, text="Interval (min)").pack()
    tk.Entry(settings, textvariable=interval_var).pack()

    #tk.Button(settings, text="Save", command=save).pack(pady=10)
    #settings.mainloop()
	
    def close():
        settings.destroy()

    tk.Button(settings, text="Save", command=save).pack(pady=(10, 5))
    tk.Button(settings, text="Cancel", command=close).pack(pady=(0, 10))

    settings.protocol("WM_DELETE_WINDOW", close)  # handle window close (X)
    settings.mainloop()

# --- Main ---
def main():
    global icon
    icon = Icon("FXAlert", icons["blue"])
    icon.menu = Menu(
        MenuItem("Settings", open_settings),
        MenuItem("Exit", on_exit)
    )

    t = threading.Thread(target=job_loop, daemon=True)
    t.start()
    run_check()  # immediate first check
    icon.run()

if __name__ == "__main__":
    main()
