import threading
import time
import tkinter as tk

from hud import JarvisHUD


# ============================================================
# J.A.R.V.I.S. MASTER CONTROLLER
# ============================================================

class JarvisMaster:

    def __init__(self):

        self.hud = None
        self.hud_thread = None

    # ========================================================
    # START HUD
    # ========================================================

    def start_hud(self):

        def run():

            self.hud = JarvisHUD()

            self.hud.run()

        self.hud_thread = threading.Thread(
            target=run,
            daemon=True
        )

        self.hud_thread.start()

        time.sleep(1)

    # ========================================================
    # START JARVIS
    # ========================================================

    def start(self):

        print("=" * 60)
        print("          J.A.R.V.I.S. MASTER SYSTEM")
        print("=" * 60)

        print("\nStarting holographic interface...")

        self.start_hud()

        print("HUD: ONLINE")

        print("\nStarting voice system...")

        # Import only after HUD has started.
        from voice_ai import main

        main()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    jarvis = JarvisMaster()

    try:

        jarvis.start()

    except KeyboardInterrupt:

        print("\n")
        print("JARVIS manually stopped.")

    except Exception as error:

        print("\nJARVIS MASTER ERROR:")
        print(error)

        input(
            "\nPress Enter to close..."
        )