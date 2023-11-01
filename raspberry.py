import tkinter as tk
from tkinter import messagebox
import requests 
import threading
import time
import atexit

SHUTDOWN_URL = "http://10.100.10.159:5000/shutdown_notification"

SERVER_URL = "http://10.100.10.159:5000/check_card"

conference_room_number = "2202"


def card_swiped():
    card_id = card_id_var.get()
    response = requests.post(SERVER_URL, json={"card_id": card_id})

    print(f"HTTP Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    try:
        data = response.json()
        if data["success"]:
            show_success(data["message"], data.get("events", []))
        else:
            show_failure(data["message"], data.get("events", []))
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode the server response as JSON.")
        simple_show_failure("卡號無效")

def show_success(message, events):
    event_times = '\n'.join(events)
    messagebox.showinfo("Success", f"{message}\n\nNearby Events:\n{event_times}")

def show_failure(message, events):
    event_times = '\n'.join(events)
    messagebox.showerror("Error", f"{message}")

def simple_show_failure(message):
    messagebox.showerror("Error", message)



def notify_server_on_shutdown():
    try:
        response = requests.get(f"{SHUTDOWN_URL}?room={conference_room_number}")
        if response.status_code != 200:
            print("Failed to notify server about the shutdown!")
    except requests.RequestException:
        print("Failed to send shutdown notification.")


def on_closing():
    notify_server_on_shutdown()
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Card Verification App")

    label = tk.Label(root, text=f"{conference_room_number} \nEnter Card ID:")
    label.pack(padx=20, pady=10)

    card_id_var = tk.StringVar()

    entry = tk.Entry(root, textvariable=card_id_var)
    entry.pack(padx=20, pady=10)

    # 新增確認按鈕
    confirm_button = tk.Button(root, text="Confirm", command=card_swiped)
    confirm_button.pack(padx=20, pady=20)

    # 為視窗關閉事件掛載函數
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
