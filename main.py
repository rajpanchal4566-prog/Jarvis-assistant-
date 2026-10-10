from jarvis_core import JarvisCore


def main():

    print("=" * 60)
    print("              J.A.R.V.I.S.")
    print("=" * 60)
    print("Starting JARVIS Core...")
    print()

    jarvis = JarvisCore()

    try:
        jarvis.run()

    except KeyboardInterrupt:
        print()
        print("JARVIS stopped.")

    except Exception as error:
        print()
        print("JARVIS ERROR:")
        print(error)


if __name__ == "__main__":
    main()