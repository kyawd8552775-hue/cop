# ripple_app.py

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

from ripple_pipeline import process_wav

class RippleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ripple Visualization Generator")
        self.geometry("500x200")

        self.wav_path = tk.StringVar()

        tk.Label(self, text="Select WAV file:").pack(pady=5)

        frame = tk.Frame(self)
        frame.pack(pady=5)

        self.entry = tk.Entry(frame, textvariable=self.wav_path, width=40)
        self.entry.pack(side=tk.LEFT, padx=5)

        browse_btn = tk.Button(frame, text="Browse", command=self.browse_wav)
        browse_btn.pack(side=tk.LEFT)

        self.run_btn = tk.Button(self, text="Run Pipeline", command=self.run_pipeline)
        self.run_btn.pack(pady=10)

        self.status = tk.Label(self, text="", fg="cyan", justify="left")
        self.status.pack(pady=5)

    def browse_wav(self):
        path = filedialog.askopenfilename(
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if path:
            self.wav_path.set(path)

    def run_pipeline(self):
        path = self.wav_path.get().strip()
        if not path or not os.path.isfile(path):
            messagebox.showerror("Error", "Please select a valid WAV file.")
            return

        self.run_btn.config(state=tk.DISABLED)
        self.status.config(text="Processing...")

        def worker():
            try:
                events_path, mel_path = process_wav(path, web_dir="web")
                msg = (
                    "Done.\nGenerated:\n"
                    f" - {os.path.basename(events_path)}\n"
                    f" - {os.path.basename(mel_path)}"
                )
                self.status.config(text=msg)
            except Exception as e:
                self.status.config(text="Error occurred.")
                messagebox.showerror("Error", str(e))
            finally:
                self.run_btn.config(state=tk.NORMAL)

        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    app = RippleApp()
    app.mainloop()
