import customtkinter as ctk
import tkinter as tk
import math
import random
import time
import threading


class JarvisHUD:

    def __init__(self):

        # ====================================================
        # WINDOW
        # ====================================================

        self.root = ctk.CTk()

        self.root.title("J.A.R.V.I.S. - HOLOGRAPHIC INTERFACE")

        self.root.geometry("1200x760")

        self.root.minsize(1000, 650)

        self.root.configure(
            fg_color="#02050a"
        )

        self.canvas = tk.Canvas(
            self.root,
            width=1200,
            height=760,
            bg="#02050a",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # STATE
        # ====================================================

        self.state = "STANDBY"

        self.running = True

        self.angle = 0

        self.scan_angle = 0

        self.wave_phase = 0

        self.pulse_phase = 0

        self.data_phase = 0

        self.activity = 0.25

        self.target_activity = 0.25

        self.last_time = time.time()

        self.state_lock = threading.Lock()

        # ====================================================
        # PARTICLES
        # ====================================================

        self.particles = []

        for _ in range(80):

            self.particles.append(
                {
                    "angle": random.uniform(0, math.pi * 2),
                    "radius": random.uniform(180, 470),
                    "speed": random.uniform(0.001, 0.006),
                    "size": random.choice([1, 1, 1, 2]),
                    "alpha": random.uniform(0.3, 1.0)
                }
            )

        # ====================================================
        # STATE SETTINGS
        # ====================================================

        self.state_settings = {

            "SLEEPING": {
                "speed": 0.25,
                "activity": 0.08
            },

            "STANDBY": {
                "speed": 0.7,
                "activity": 0.22
            },

            "WAKE": {
                "speed": 3.5,
                "activity": 0.9
            },

            "LISTENING": {
                "speed": 2.5,
                "activity": 0.75
            },

            "PROCESSING": {
                "speed": 2.0,
                "activity": 0.65
            },

            "EXECUTING": {
                "speed": 3.0,
                "activity": 0.85
            },

            "SPEAKING": {
                "speed": 3.2,
                "activity": 1.0
            }
        }

        # ====================================================
        # STATIC INTERFACE
        # ====================================================

        self.draw_background()

        self.draw_interface()

        # ====================================================
        # START ANIMATION
        # ====================================================

        self.animate()

    # ========================================================
    # STATE
    # ========================================================

    def set_state(self, state):

        state = str(state).upper()

        with self.state_lock:

            self.state = state

    # ========================================================
    # GET STATE
    # ========================================================

    def get_state(self):

        with self.state_lock:

            return self.state

    # ========================================================
    # BACKGROUND
    # ========================================================

    def draw_background(self):

        self.canvas.delete("background")

        width = self.canvas.winfo_width()

        height = self.canvas.winfo_height()

        if width < 100:
            width = 1200

        if height < 100:
            height = 760

        # ====================================================
        # GRID
        # ====================================================

        grid_spacing = 40

        for x in range(0, width, grid_spacing):

            self.canvas.create_line(
                x,
                0,
                x,
                height,
                fill="#03151c",
                width=1,
                tags="background"
            )

        for y in range(0, height, grid_spacing):

            self.canvas.create_line(
                0,
                y,
                width,
                y,
                fill="#03151c",
                width=1,
                tags="background"
            )

        # ====================================================
        # TOP LINE
        # ====================================================

        self.canvas.create_line(
            40,
            92,
            width - 40,
            92,
            fill="#06495a",
            width=1,
            tags="background"
        )

        # ====================================================
        # BOTTOM LINE
        # ====================================================

        self.canvas.create_line(
            40,
            height - 65,
            width - 40,
            height - 65,
            fill="#06495a",
            width=1,
            tags="background"
        )

    # ========================================================
    # STATIC INTERFACE
    # ========================================================

    def draw_interface(self):

        width = 1200
        height = 760

        # ====================================================
        # TITLE
        # ====================================================

        self.canvas.create_text(
            width / 2,
            35,
            text="J.A.R.V.I.S.",
            fill="#00d9ff",
            font=("Segoe UI", 28, "bold"),
            tags="static"
        )

        self.canvas.create_text(
            width / 2,
            65,
            text="ARTIFICIAL INTELLIGENCE SYSTEM",
            fill="#367f91",
            font=("Segoe UI", 9),
            tags="static"
        )

        # ====================================================
        # LEFT PANEL
        # ====================================================

        self.canvas.create_text(
            75,
            130,
            text="SYSTEM STATUS",
            fill="#00d9ff",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            tags="static"
        )

        self.canvas.create_text(
            75,
            160,
            text="CORE",
            fill="#377e90",
            font=("Segoe UI", 8),
            anchor="w",
            tags="static"
        )

        self.canvas.create_text(
            75,
            182,
            text="ONLINE",
            fill="#00d9ff",
            font=("Segoe UI", 15, "bold"),
            anchor="w",
            tags="static"
        )

        self.canvas.create_text(
            75,
            220,
            text="VOICE",
            fill="#377e90",
            font=("Segoe UI", 8),
            anchor="w",
            tags="static"
        )

        self.canvas.create_text(
            75,
            242,
            text="ACTIVE",
            fill="#00d9ff",
            font=("Segoe UI", 15, "bold"),
            anchor="w",
            tags="static"
        )

        self.canvas.create_text(
            75,
            280,
            text="SECURITY",
            fill="#377e90",
            font=("Segoe UI", 8),
            anchor="w",
            tags="static"
        )

        self.canvas.create_text(
            75,
            302,
            text="VERIFIED",
            fill="#00d9ff",
            font=("Segoe UI", 13, "bold"),
            anchor="w",
            tags="static"
        )

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        self.canvas.create_text(
            1125,
            130,
            text="JARVIS CORE",
            fill="#00d9ff",
            font=("Segoe UI", 10, "bold"),
            anchor="e",
            tags="static"
        )

        self.canvas.create_text(
            1125,
            160,
            text="PROCESSOR",
            fill="#377e90",
            font=("Segoe UI", 8),
            anchor="e",
            tags="static"
        )

        self.canvas.create_text(
            1125,
            182,
            text="ACTIVE",
            fill="#00d9ff",
            font=("Segoe UI", 13, "bold"),
            anchor="e",
            tags="static"
        )

        self.canvas.create_text(
            1125,
            220,
            text="NETWORK",
            fill="#377e90",
            font=("Segoe UI", 8),
            anchor="e",
            tags="static"
        )

        self.canvas.create_text(
            1125,
            242,
            text="ONLINE",
            fill="#00d9ff",
            font=("Segoe UI", 13, "bold"),
            anchor="e",
            tags="static"
        )

        self.canvas.create_text(
            1125,
            280,
            text="INTERFACE",
            fill="#377e90",
            font=("Segoe UI", 8),
            anchor="e",
            tags="static"
        )

        self.canvas.create_text(
            1125,
            302,
            text="HOLOGRAPHIC",
            fill="#00d9ff",
            font=("Segoe UI", 11, "bold"),
            anchor="e",
            tags="static"
        )

        # ====================================================
        # BOTTOM INFORMATION
        # ====================================================

        self.canvas.create_text(
            60,
            height - 38,
            text="VOICE INTERFACE",
            fill="#367f91",
            font=("Segoe UI", 8),
            anchor="w",
            tags="static"
        )

        self.canvas.create_text(
            210,
            height - 38,
            text="● ONLINE",
            fill="#00d9ff",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            tags="static"
        )

        self.canvas.create_text(
            width - 60,
            height - 38,
            text="J.A.R.V.I.S. CORE v1.0",
            fill="#367f91",
            font=("Segoe UI", 8),
            anchor="e",
            tags="static"
        )

    # ========================================================
    # CENTER
    # ========================================================

    def draw_center(self, cx, cy, speed, activity):

        # ====================================================
        # OUTER ROTATING RINGS
        # ====================================================

        rings = [
            (250, 2, 1),
            (230, -2, 2),
            (210, 3, 1),
            (190, -3, 2),
            (165, 4, 1),
            (145, -4, 2)
        ]

        for radius, direction, width in rings:

            start = (
                self.angle * speed * direction
            ) % 360

            self.canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start,
                extent=250,
                outline="#007f99",
                width=width,
                style=tk.ARC,
                tags="dynamic"
            )

        # ====================================================
        # SEGMENTED RING
        # ====================================================

        radius = 220

        for i in range(24):

            angle = (
                self.angle * speed * 1.5
                + i * 15
            )

            active = (
                math.sin(
                    math.radians(angle)
                ) > 0.25
            )

            if active:

                color = "#00d9ff"

            else:

                color = "#06495a"

            start = angle % 360

            self.canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start,
                extent=7,
                outline=color,
                width=3,
                style=tk.ARC,
                tags="dynamic"
            )

        # ====================================================
        # RADIAL MECHANISM
        # ====================================================

        for i in range(16):

            angle = math.radians(
                self.angle * speed
                + i * 22.5
            )

            inner = 95
            outer = 180

            x1 = cx + math.cos(angle) * inner
            y1 = cy + math.sin(angle) * inner

            x2 = cx + math.cos(angle) * outer
            y2 = cy + math.sin(angle) * outer

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#075b70",
                width=1,
                tags="dynamic"
            )

        # ====================================================
        # INNER RINGS
        # ====================================================

        for radius in [125, 105, 85, 65]:

            pulse = math.sin(
                self.pulse_phase
                + radius
            )

            r = radius + int(
                pulse * activity * 4
            )

            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline="#00aeca",
                width=2,
                tags="dynamic"
            )

        # ====================================================
        # CORE GLOW
        # ====================================================

        pulse = (
            math.sin(
                self.pulse_phase
            ) + 1
        ) / 2

        glow_radius = (
            48
            + int(
                pulse
                * 25
                * activity
            )
        )

        for extra in [22, 15, 8]:

            r = glow_radius + extra

            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline="#075b70",
                width=1,
                tags="dynamic"
            )

        # ====================================================
        # CORE
        # ====================================================

        core_radius = (
            35
            + int(
                pulse
                * 15
                * activity
            )
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
            cx - 24,
            cy - 24,
            cx + 24,
            cy + 24,
            outline="#32eaff",
            width=2,
            tags="dynamic"
        )

        self.canvas.create_oval(
            cx - 13,
            cy - 13,
            cx + 13,
            cy + 13,
            fill="#00d9ff",
            outline="",
            tags="dynamic"
        )

        # ====================================================
        # RADAR SCAN
        # ====================================================

        scan_radius = 255

        scan_angle = math.radians(
            self.scan_angle
        )

        x = cx + math.cos(scan_angle) * scan_radius

        y = cy + math.sin(scan_angle) * scan_radius

        self.canvas.create_line(
            cx,
            cy,
            x,
            y,
            fill="#00d9ff",
            width=1,
            tags="dynamic"
        )

        # ====================================================
        # SCAN ARC
        # ====================================================

        self.canvas.create_arc(
            cx - scan_radius,
            cy - scan_radius,
            cx + scan_radius,
            cy + scan_radius,
            start=self.scan_angle,
            extent=35,
            outline="#00d9ff",
            width=2,
            style=tk.ARC,
            tags="dynamic"
        )

    # ========================================================
    # WAVEFORM
    # ========================================================

    def draw_waveform(self, cx, cy, activity):

        points = []

        width = 180

        for x in range(-width, width, 6):

            normalized = x / width

            envelope = (
                1
                - abs(normalized)
            )

            wave = math.sin(
                x * 0.08
                + self.wave_phase
            )

            wave2 = math.sin(
                x * 0.16
                + self.wave_phase * 1.7
            )

            amplitude = (
                8
                + activity * 35
            )

            y = (
                cy
                + (
                    wave * 0.65
                    + wave2 * 0.35
                )
                * amplitude
                * envelope
            )

            points.append(
                (cx + x, y)
            )

        for i in range(
            len(points) - 1
        ):

            self.canvas.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                fill="#00d9ff",
                width=2,
                tags="dynamic"
            )

    # ========================================================
    # PARTICLES
    # ========================================================

    def draw_particles(self, cx, cy, activity):

        for particle in self.particles:

            particle["angle"] += (
                particle["speed"]
                * activity
            )

            angle = particle["angle"]

            radius = particle["radius"]

            x = (
                cx
                + math.cos(angle)
                * radius
            )

            y = (
                cy
                + math.sin(angle)
                * radius
                * 0.65
            )

            size = particle["size"]

            self.canvas.create_oval(
                x - size,
                y - size,
                x + size,
                y + size,
                fill="#00aeca",
                outline="",
                tags="dynamic"
            )

    # ========================================================
    # TECHNICAL DATA
    # ========================================================

    def draw_data(self, activity):

        self.data_phase += 1

        cpu = int(
            20
            + activity * 70
            + math.sin(
                self.data_phase * 0.05
            ) * 10
        )

        memory = int(
            35
            + activity * 35
            + math.sin(
                self.data_phase * 0.03
            ) * 8
        )

        signal = int(
            80
            + math.sin(
                self.data_phase * 0.08
            ) * 15
        )

        # LEFT DATA

        self.canvas.create_text(
            75,
            350,
            text=f"CPU LOAD   {cpu:02d}%",
            fill="#176579",
            font=("Consolas", 9),
            anchor="w",
            tags="dynamic"
        )

        self.canvas.create_text(
            75,
            375,
            text=f"MEMORY     {memory:02d}%",
            fill="#176579",
            font=("Consolas", 9),
            anchor="w",
            tags="dynamic"
        )

        self.canvas.create_text(
            75,
            400,
            text=f"LINK       {signal:02d}%",
            fill="#176579",
            font=("Consolas", 9),
            anchor="w",
            tags="dynamic"
        )

        # RIGHT DATA

        self.canvas.create_text(
            1125,
            350,
            text="NEURAL LINK",
            fill="#176579",
            font=("Consolas", 9),
            anchor="e",
            tags="dynamic"
        )

        self.canvas.create_text(
            1125,
            375,
            text="CONNECTED",
            fill="#00aeca",
            font=("Consolas", 9),
            anchor="e",
            tags="dynamic"
        )

        self.canvas.create_text(
            1125,
            400,
            text=f"ACTIVITY {int(activity * 100):02d}%",
            fill="#176579",
            font=("Consolas", 9),
            anchor="e",
            tags="dynamic"
        )

    # ========================================================
    # STATE DISPLAY
    # ========================================================

    def draw_state(self, width, height):

        state = self.get_state()

        self.canvas.create_text(
            width / 2,
            height - 105,
            text=state,
            fill="#00d9ff",
            font=("Segoe UI", 18, "bold"),
            tags="dynamic"
        )

        # STATE DESCRIPTION

        descriptions = {

            "SLEEPING":
                "LOW POWER / AWAITING WAKE COMMAND",

            "STANDBY":
                "SYSTEM READY / AWAITING COMMAND",

            "WAKE":
                "VOICE INTERFACE ACTIVATED",

            "LISTENING":
                "LISTENING FOR COMMAND",

            "PROCESSING":
                "PROCESSING REQUEST",

            "EXECUTING":
                "EXECUTING COMMAND",

            "SPEAKING":
                "VOICE OUTPUT ACTIVE"
        }

        description = descriptions.get(
            state,
            "SYSTEM ACTIVE"
        )

        self.canvas.create_text(
            width / 2,
            height - 82,
            text=description,
            fill="#367f91",
            font=("Segoe UI", 8),
            tags="dynamic"
        )

    # ========================================================
    # ANIMATION
    # ========================================================

    def animate(self):

        if not self.running:

            return

        try:

            width = self.canvas.winfo_width()

            height = self.canvas.winfo_height()

            if width < 500:

                width = 1200

            if height < 400:

                height = 760

            state = self.get_state()

            settings = self.state_settings.get(
                state,
                self.state_settings["STANDBY"]
            )

            speed = settings["speed"]

            self.target_activity = settings["activity"]

            # =================================================
            # SMOOTH ACTIVITY
            # =================================================

            self.activity += (
                self.target_activity
                - self.activity
            ) * 0.08

            # =================================================
            # CENTER
            # =================================================

            cx = width / 2

            cy = height / 2 + 15

            # =================================================
            # CLEAR DYNAMIC
            # =================================================

            self.canvas.delete(
                "dynamic"
            )

            # =================================================
            # ANIMATION PHASES
            # =================================================

            self.angle += speed

            self.scan_angle += (
                speed * 1.8
            )

            self.wave_phase += (
                0.12
                + self.activity * 0.25
            )

            self.pulse_phase += (
                0.08
                + self.activity * 0.22
            )

            # =================================================
            # DRAW
            # =================================================

            self.draw_center(
                cx,
                cy,
                speed,
                self.activity
            )

            # =================================================
            # WAVEFORM
            # =================================================

            if state in [
                "LISTENING",
                "SPEAKING",
                "PROCESSING",
                "EXECUTING"
            ]:

                self.draw_waveform(
                    cx,
                    cy,
                    self.activity
                )

            # =================================================
            # PARTICLES
            # =================================================

            self.draw_particles(
                cx,
                cy,
                self.activity
            )

            # =================================================
            # DATA
            # =================================================

            self.draw_data(
                self.activity
            )

            # =================================================
            # STATE
            # =================================================

            self.draw_state(
                width,
                height
            )

            # =================================================
            # NEXT FRAME
            # =================================================

            self.root.after(
                30,
                self.animate
            )

        except Exception as error:

            print(
                "HUD ANIMATION ERROR:",
                error
            )

            self.root.after(
                100,
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


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    hud = JarvisHUD()

    hud.run()