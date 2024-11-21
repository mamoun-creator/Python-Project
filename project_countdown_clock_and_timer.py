# Mamoun Mohamed
# 21/11/2024
# Enhanced Countdown Timer.

import tkinter as tk
from tkinter import messagebox
import time

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        
        # Initialize timer variables
        self.total_seconds = 0
        self.timer_running = False
        
        # Create UI elements
        self.label = tk.Label(root, text="Enter seconds:", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start Countdown", font=("Arial", 14), command=self.start_timer)
        self.start_button.pack(pady=10)
        
        self.time_display = tk.Label(root, text="00:00", font=("Arial", 24), fg="blue")
        self.time_display.pack(pady=20)

    def start_timer(self):
        try:
            self.total_seconds = int(self.entry.get())
            if self.total_seconds < 0:
                messagebox.showerror("Invalid Input", "Please enter a positive number of seconds.")
                return

            if not self.timer_running:
                self.timer_running = True
                self.run_timer()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of seconds.")

    def run_timer(self):
        if self.total_seconds > 0:
            minutes, seconds = divmod(self.total_seconds, 60)
            time_str = f"{minutes:02}:{seconds:02}"
            self.time_display.config(text=time_str)
            self.total_seconds -= 1
            self.root.after(1000, self.run_timer)  # Update every 1 second
        else:
            self.time_display.config(text="00:00")
            messagebox.showinfo("Time's Up!", "The countdown has finished!")

def main():
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
