import tkinter as tk
import math
import time
import threading


class JarvisHUD:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("J.A.R.V.I.S.")

        self.root.attributes(
            "-fullscreen",
            True
        )

        self.root.attributes(
            "-topmost",
            True
        )

        self.root.configure(
            bg="black"
        )

        self.canvas = tk.Canvas(
            self.root,
            bg="black",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.running = True

        self.angle = 0

        self.status = "STANDBY"

        self.root.bind(
            "<Escape>",
            self.close
        )

        self.animate()

    def set_status(self, status):

        self.status = status.upper()

    def animate(self):

        if not self.running:
            return

        self.canvas.delete("all")

        width = self.root.winfo_width()
        height = self.root.winfo_height()

        center_x = width // 2
        center_y = height // 2

        radius = 180

        # Outer rotating ring

        for i in range(3):

            r = radius + i * 35

            self.canvas.create_oval(
                center_x - r,
                center_y - r,
                center_x + r,
                center_y + r,
                outline="#00bfff",
                width=2
            )

        # Rotating scanner lines

        for i in range(12):

            angle = math.radians(
                self.angle + i * 30
            )

            x1 = center_x + math.cos(angle) * 80
            y1 = center_y + math.sin(angle) * 80

            x2 = center_x + math.cos(angle) * 220
            y2 = center_y + math.sin(angle) * 220

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#00bfff",
                width=2
            )

        # Core

        self.canvas.create_oval(
            center_x - 65,
            center_y - 65,
            center_x + 65,
            center_y + 65,
            outline="#00eaff",
            width=5
        )

        self.canvas.create_oval(
            center_x - 35,
            center_y - 35,
            center_x + 35,
            center_y + 35,
            fill="#008cff",
            outline="#00ffff",
            width=3
        )

        # Title

        self.canvas.create_text(
            center_x,
            100,
            text="J.A.R.V.I.S.",
            fill="#00eaff",
            font=("Consolas", 38, "bold")
        )

        # Status

        self.canvas.create_text(
            center_x,
            center_y + 280,
            text=self.status,
            fill="#00eaff",
            font=("Consolas", 24, "bold")
        )

        self.angle += 2

        self.root.after(
            30,
            self.animate
        )

    def show(self):

        self.root.mainloop()

    def close(self, event=None):

        self.running = False

        self.root.destroy()


hud = JarvisHUD()