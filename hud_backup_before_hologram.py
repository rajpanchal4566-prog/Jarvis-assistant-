import customtkinter as ctk
import tkinter as tk
import math


class JarvisHUD:

    def __init__(self):

        self.root = ctk.CTk()

        self.root.title("J.A.R.V.I.S.")

        self.root.geometry("900x650")

        self.root.resizable(False, False)

        self.root.configure(
            fg_color="#05070d"
        )

        self.canvas = tk.Canvas(
            self.root,
            width=900,
            height=650,
            bg="#05070d",
            highlightthickness=0
        )

        self.canvas.pack()

        self.angle = 0
        self.scan_y = 120

        self.state = "STANDBY"

        self.running = True

        self.draw_static()

        self.animate()

    # ========================================================
    # STATE
    # ========================================================

    def set_state(self, state):

        self.state = state.upper()

        print(f"HUD STATE: {self.state}")

    # ========================================================
    # STATIC UI
    # ========================================================

    def draw_static(self):

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

        self.canvas.create_text(
            450,
            570,
            text="STANDBY",
            fill="#00d9ff",
            font=("Segoe UI", 15, "bold"),
            tags="state"
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

        if not self.running:
            return

        self.canvas.delete("dynamic")

        cx = 450
        cy = 330

        # ----------------------------------------------------
        # STATE SPEED
        # ----------------------------------------------------

        speeds = {
            "STANDBY": 1,
            "WAKE": 4,
            "LISTENING": 6,
            "PROCESSING": 3,
            "EXECUTING": 5,
            "SPEAKING": 7
        }

        speed = speeds.get(
            self.state,
            2
        )

        # ----------------------------------------------------
        # OUTER RINGS
        # ----------------------------------------------------

        rings = [
            (210, 0),
            (185, 50),
            (160, 100),
            (135, 150)
        ]

        for radius, offset in rings:

            start = (
                self.angle * speed
                + offset
            ) % 360

            self.canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start,
                extent=260,
                outline="#00d9ff",
                width=2,
                style=tk.ARC,
                tags="dynamic"
            )

        # ----------------------------------------------------
        # CORE PULSE
        # ----------------------------------------------------

        pulse = (
            math.sin(
                math.radians(
                    self.angle * speed * 2
                )
            ) + 1
        ) / 2

        core_radius = (
            40 + int(pulse * 12)
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
                self.angle * speed
                + i * 30
            )

            x1 = cx + math.cos(angle) * 65
            y1 = cy + math.sin(angle) * 65

            x2 = cx + math.cos(angle) * 220
            y2 = cy + math.sin(angle) * 220

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

        self.scan_y += speed

        if self.scan_y > 520:
            self.scan_y = 120

        self.canvas.create_line(
            230,
            self.scan_y,
            670,
            self.scan_y,
            fill="#00d9ff",
            width=1,
            tags="dynamic"
        )

        # ----------------------------------------------------
        # LEFT STATUS
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

        # ----------------------------------------------------
        # RIGHT STATUS
        # ----------------------------------------------------

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
        # STATE TEXT
        # ----------------------------------------------------

        self.canvas.delete("state")

        self.canvas.create_text(
            450,
            570,
            text=self.state,
            fill="#00d9ff",
            font=("Segoe UI", 15, "bold"),
            tags="state"
        )

        self.angle += 1

        self.root.after(
            30,
            self.animate
        )

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        self.running = False

        try:
            self.root.destroy()
        except Exception:
            pass

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    hud = JarvisHUD()

    hud.run()