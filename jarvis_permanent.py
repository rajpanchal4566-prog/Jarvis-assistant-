import threading
import time

from hud import JarvisHUD
from jarvis_core import JarvisCore


def main():

    hud = None

    # ========================================================
    # HUD THREAD
    # ========================================================

    def start_hud():

        nonlocal hud

        hud = JarvisHUD()

        hud.set_state("SLEEPING")

        hud.run()

    thread = threading.Thread(
        target=start_hud,
        daemon=True
    )

    thread.start()

    # Give HUD time to initialize.
    time.sleep(1)

    # ========================================================
    # JARVIS CORE
    # ========================================================

    jarvis = JarvisCore(
        hud=hud
    )

    jarvis.run()


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\nJARVIS manually stopped."
        )

    except Exception as error:

        print(
            "\nJARVIS ERROR:",
            error
        )

        input(
            "\nPress Enter to close..."
        )