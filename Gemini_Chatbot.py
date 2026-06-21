from google import genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """
You are an Expert Academic Mentor and Study Planner.

Responsibilities:
1. Generate structured study plans.
2. Answer follow-up questions clearly.
3. Help beginners understand concepts.

Study Plan Format:

1. Subtopic Name
   Description: One-line explanation

Rules:
- Generate 5 to 8 subtopics.
- Use numbered lists.
- Keep responses under 250 words.
- Be beginner friendly.
- Do NOT provide unrelated information.
- Do NOT generate very long paragraphs.
"""

print("=" * 50)
print("WELCOME TO AI STUDY ASSISTANT")
print("=" * 50)

topic = input("\nEnter a topic you want to study: ")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\nCreate a study plan for {topic}"
    )

    print("\n")
    print(response.text)

except Exception as e:
    print("Error:", e)
    exit()

question_count = 0
chat_history = []

print("\nYou can now ask follow-up questions.")
print("Type 'exit' or 'quit' to end.\n")

while True:

    user_input = input("Ask:- ")

    if user_input.lower() in ["exit", "quit"]:

        print("\n" + "=" * 40)
        print("SESSION SUMMARY")
        print("=" * 40)
        print(f"Topic Studied: {topic}")
        print(f"Questions Asked: {question_count}")
        print("\nThank you for using AI Study Assistant!")
        break

    chat_history.append(f"User: {user_input}")

    prompt = (
        SYSTEM_PROMPT +
        f"\n\nCurrent Topic: {topic}\n\n" +
        "\n".join(chat_history)
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text

        chat_history.append(f"Assistant: {answer}")

        print("\nAssistant:")
        print(answer)
        print()

        question_count += 1

    except Exception as e:
        print("Error:", e)