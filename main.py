import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use the new OpenAI client interface
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from lib.input import get_user_prompt
from lib.generator import generate_story, generate_branch_story
from lib.judge import critique_story
from lib.refiner import refine_story

def main():
    # 1) Prompt for a story topic
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

    # 4) Complete the story based on the selection
    print("\n--- Completing Story ---")
    continuation = generate_branch_story(intro, selected_option)
    print(continuation)
    
    # 5) Combine intro and continuation for the complete story
    complete_story = intro + "\n\n" + continuation

    # 6) Critique the complete story
    print("\n--- Critiquing Story ---")
    critique = critique_story(complete_story)
    print(critique)

    # 7) Refine the complete story based on the critique
    print("\n--- Refining Story ---")
    refined_story = refine_story(complete_story, critique)
    print(refined_story)

    # 8) Generate a single illustration via DALL·E (no text)
    print("\n--- Generating Illustration URL ---")
    try:
        resp = client.images.generate(
            model="dall-e-3",
            prompt=(
                "Create a single image composed of 6 equal comic-style panels (arranged in 2 rows of 3). "
                "Use a gentle, storybook illustration style with soft colors and no text or captions. "
                "Each panel should show one key beat of the story below, in order:\n\n"
                f"{refined_story}"
            ),
            n=1,
            size="1792x1024"  # wide format to fit 2×3 panels nicely
        )
        img_url = resp.data[0].url
        print(f"\nIllustration URL (paste into your browser):\n{img_url}\n")
    except Exception as e:
        print(f"\n⚠️ Illustration generation failed: {e}")

if __name__ == "__main__":
    main()