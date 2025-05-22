import os
from dotenv import load_dotenv

# Load OpenAI API key from .env
load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

from lib.input import get_user_prompt
from lib.generator import generate_story, generate_branch_story


def main():
    # 1) Prompt for story topic
    topic = get_user_prompt()

    # 2) Generate the story intro and two choices
    print("\n--- Story Beginning ---")
    intro, options = generate_story(topic)
    print(intro + "\n")

    # 3) Display numbered options
    for opt in options:
        print(opt)

    # 4) Prompt user to pick 1 or 2
    choice = None
    while choice not in ('1', '2'):
        choice = input("\nPick 1 or 2: ").strip()

    # 5) Map numeric choice to the option text
    selected_option = options[int(choice) - 1]

    # 6) Continue and complete the story based on selection
    print("\n--- Completing Story ---")
    full_story = generate_branch_story(intro, selected_option)
    print(full_story)


if __name__ == "__main__":
    main()