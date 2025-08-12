import tkinter as tk
import webbrowser

class Notification:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RingRing Meeting Reminder")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = screen_width // 2
        height = screen_height // 2
        x = (screen_width - width) // 2
        y = (screen_height - height) // 3
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.attributes("-alpha", 0.95)
        self.root.configure(bg="#e8eef5")

        self.title_label = tk.Label(
            self.root, 
            font=("Helvetica", 32, "bold"),
            bg="#e8eef5",
            fg="#222222",
            wraplength=width - 80,
            justify="center"
        )
        self.title_label.pack(pady=(30, 10))

        self.desc_label = tk.Label(
            self.root,
            font=("Helvetica", 20),
            bg="#e8eef5",
            fg="#444444",
            wraplength=width - 80,
            justify="center"
        )
        self.desc_label.pack(pady=(0, 40))

        self.btn_frame = tk.Frame(self.root, bg="#e8eef5")
        self.btn_frame.pack(pady=20, fill="x", padx=40)

        btn_bg = "#333333"
        btn_active_bg = "#555555"
        btn_fg = "#222222"  # 深色文字

        self.btn_join = tk.Button(
            self.btn_frame,
            text="Join The Meeting",
            font=("Helvetica", 28),
            width=15,
            height=3,
            bg=btn_bg,
            fg=btn_fg,
            activebackground=btn_active_bg,
            activeforeground=btn_fg,
            relief="flat",
            command=lambda: None
        )
        self.btn_join.pack(side="left", expand=True, padx=20)

        self.btn_dismiss = tk.Button(
            self.btn_frame,
            text="Dismiss",
            font=("Helvetica", 28),
            width=15,
            height=3,
            bg=btn_bg,
            fg=btn_fg,
            activebackground=btn_active_bg,
            activeforeground=btn_fg,
            relief="flat",
            command=self.root.destroy
        )
        self.btn_dismiss.pack(side="right", expand=True, padx=20)

    def show(self, meeting_info: dict):
        self.title_label.config(text=meeting_info.get("title", "No Title"))
        self.desc_label.config(text=meeting_info.get("description", ""))
        link = meeting_info.get("link")
        if link:
            self.btn_join.config(command=lambda: webbrowser.open(link), state="normal")
        else:
            self.btn_join.config(state="disabled")
        self.root.mainloop()


if __name__ == "__main__":
    info = {
        "title": "Team Sync Meeting",
        "description": "Discuss project updates and next steps.",
        "link": "https://meet.google.com/abc-defg-hij"
    }
    notification = Notification()
    notification.show(info)