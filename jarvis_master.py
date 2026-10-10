import threading
import time

from hud import JarvisHUD
import voice_ai


class JarvisMaster:

    def __init__(self):

        self.hud = None
        self.hud_thread = None

    # ========================================================
    # HUD
    # ========================================================

    def start_hud(self):

        def run_hud():

            self.hud = JarvisHUD()
            
            voice_ai.HUD = self.hud

            self.hud.set_state("STANDBY")

            self.hud.run()

        self.hud_thread = threading.Thread(
            target=run_hud,
            daemon=True
        )

        self.hud_thread.start()

        time.sleep(1)

    # ========================================================
    # START
    # ========================================================

    def start(self):

        print("=" * 60)
        print("          J.A.R.V.I.S. MASTER SYSTEM")
        print("=" * 60)

        print("\n🔵 Starting holographic interface...")

        self.start_hud()

        print("✅ HUD ONLINE")

        # ----------------------------------------------------
        # Existing voice system
        # ----------------------------------------------------

        print("\n🎤 Starting voice system...")

        from voice_ai import main

        main()


# ============================================================
# START JARVIS
# ============================================================

if __name__ == "__main__":

    jarvis = JarvisMaster()

    try:

        jarvis.start()

    except KeyboardInterrupt:

        print("\nJARVIS manually stopped.")

    except Exception as error:

        print("\nJARVIS MASTER ERROR:")
        print(error)

        input("\nPress Enter to close...")