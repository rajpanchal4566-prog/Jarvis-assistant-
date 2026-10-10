import ollama


MODEL = "llama3.2:3b"


def ask_ai(user_text):

    try:

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are JARVIS, a personal AI assistant. "
                        "Speak naturally and briefly. "
                        "Call the user boss. "
                        "Be helpful and conversational."
                    )
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        return response["message"]["content"]

    except Exception as error:

        print("AI ERROR:", error)

        return (
            "I'm having trouble accessing my local AI brain, boss."
        )


if __name__ == "__main__":

    print("=" * 50)
    print("J.A.R.V.I.S. LOCAL AI BRAIN")
    print("=" * 50)

    while True:

        question = input("\nYou: ")

        if question.lower() in [
            "exit",
            "quit",
            "stop"
        ]:

            print(
                "JARVIS: Going offline, boss."
            )

            break

        answer = ask_ai(question)

        print(
            "\nJARVIS:",
            answer
        )