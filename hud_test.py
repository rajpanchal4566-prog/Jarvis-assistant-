import customtkinter as ctk
import tkinter as tk
import math


# ============================================================
# J.A.R.V.I.S. HOLOGRAPHIC HUD
# ============================================================

ctk.set_appearance_mode("dark")


class JarvisHUD:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title("J.A.R.V.I.S.")

        self.root.geometry("900x650")

        self.root.configure(
            fg_color="#05070d"
        )

        self.root.resizable(False, False)

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=900,
            height=650,
            bg="#05070d",
            highlightthickness=0
        )

        self.canvas.pack()

        self.angle = 0
        self.scan_y = 100

        self.status = "JARVIS ONLINE"

        self.draw_static()

        self.animate()

    # ========================================================
    # STATIC UI
    # ========================================================

    def draw_static(self):

        # Title
        self.canvas.create_text(
            450,
            45,
            text="J.A.R.V.I.S.",
            fill="#00d9ff",
            font=("Segoe UI", 28, "bold")
        )

        self.canvas.create_text(
            450,
            78,
            text="ARTIFICIAL INTELLIGENCE SYSTEM",
            fill="#4aa8bd",
            font=("Segoe UI", 10)
        )

        # Status
        self.canvas.create_text(
            450,
            570,
            text=self.status,
            fill="#00d9ff",
            font=("Segoe UI", 14, "bold"),
            tags="status"
        )

        self.canvas.create_text(
            450,
            600,
            text="VOICE INTERFACE • ONLINE",
            fill="#4aa8bd",
            font=("Segoe UI", 10)
        )

    # ========================================================
    # ANIMATION
    # ========================================================

    def animate(self):

        self.canvas.delete("dynamic")

        cx = 450
        cy = 330

        # ----------------------------------------------------
        # OUTER RINGS
        # ----------------------------------------------------

        for radius, offset in [
            (190, 0),
            (165, 45),
            (140, 90),
            (115, 135)
        ]:

            start = (
                self.angle * 2 + offset
            ) % 360

            self.canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start,
                extent=250,
                outline="#00d9ff",
                width=2,
                style=tk.ARC,
                tags="dynamic"
            )

        # ----------------------------------------------------
        # INNER CORE
        # ----------------------------------------------------

        pulse = (
            math.sin(
                math.radians(self.angle * 4)
            ) + 1
        ) / 2

        core_radius = 45 + int(
            pulse * 8
        )

        self.canvas.create_oval(
            cx - core_radius,
            cy - core_radius,
            cx + core_radius,
            cy + core_radius,
            outline="#00d9ff",
            width=3,
            tags="dynamic"
        )

        # Core
        self.canvas.create_oval(
            cx - 20,
            cy - 20,
            cx + 20,
            cy + 20,
            fill="#00d9ff",
            outline="",
            tags="dynamic"
        )

        # ----------------------------------------------------
        # RADIAL LINES
        # ----------------------------------------------------

        for i in range(12):

            angle = math.radians(
                self.angle + i * 30
            )

            x1 = cx + math.cos(angle) * 60
            y1 = cy + math.sin(angle) * 60

            x2 = cx + math.cos(angle) * 210
            y2 = cy + math.sin(angle) * 210

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#075b70",
                width=1,
                tags="dynamic"
            )

        # ----------------------------------------------------
        # SCANNING LINE
        # ----------------------------------------------------

        self.scan_y += 3

        if self.scan_y > 520:

            self.scan_y = 120

        self.canvas.create_line(
            250,
            self.scan_y,
            650,
            self.scan_y,
            fill="#00d9ff",
            width=1,
            tags="dynamic"
        )

        # ----------------------------------------------------
        # SIDE INFORMATION
        # ----------------------------------------------------

        self.canvas.create_text(
            90,
            240,
            text="SYSTEM",
            fill="#4aa8bd",
            font=("Segoe UI", 10),
            tags="dynamic"
        )

        self.canvas.create_text(
            90,
            265,
            text="ONLINE",
            fill="#00d9ff",
            font=("Segoe UI", 14, "bold"),
            tags="dynamic"
        )

        self.canvas.create_text(
            810,
            240,
            text="CORE",
            fill="#4aa8bd",
            font=("Segoe UI", 10),
            tags="dynamic"
        )

        self.canvas.create_text(
            810,
            265,
            text="ACTIVE",
            fill="#00d9ff",
            font=("Segoe UI", 14, "bold"),
            tags="dynamic"
        )

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

        self.angle += 2

        self.root.after(
            30,
            self.animate
        )

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        self.root.mainloop()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    hud = JarvisHUD()

    hud.run()