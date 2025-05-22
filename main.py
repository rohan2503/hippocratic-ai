import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use the new OpenAI client interface
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from lib.input import get_user_prompt
from lib.generator import generate_story, generate_branch_story

def main():
    # 1) Prompt for story topic
    topic = get_user_prompt()

    # 2) Generate the story intro and two choices
    print("\n--- Story Beginning ---")
    intro, options = generate_story(topic)
    print(intro + "\n")
    for opt in options:
        print(opt)

    # 3) Prompt user to pick 1 or 2
    choice = None
    while choice not in ("1", "2"):
        choice = input("\nPick 1 or 2: ").strip()
    selected_option = options[int(choice) - 1]

    # 4) Complete the story based on the choice
    print("\n--- Completing Story ---")
    full_story = generate_branch_story(intro, selected_option)
    print(full_story)

    # 5) Generate an illustration via DALL·E
    print("\n--- Generating Illustration URL ---")
    try:
        img_resp = client.images.generate(
            model="dall-e-3",
            prompt=f"Illustrate this bedtime story for kids:\n\n{full_story}",
            n=1,
            size="1024x1024"          # ← changed from 512x512
        )
        img_url = img_resp.data[0].url
        print(f"\nIllustration URL (paste into your browser):\n{img_url}\n")
    except Exception as e:
        print(f"\n⚠️ Illustration generation failed: {e}")

if __name__ == "__main__":
    main()