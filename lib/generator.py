import openai
import re


def generate_story(topic: str) -> tuple[str, list[str]]:
    """
    Generate the opening of a bedtime story for ages 5–10 about `topic`, ending with exactly two numbered choices.

    Returns:
        intro (str): The story setup introducing characters and conflict.
        options (list[str]): A list of two option strings, each starting with '1.' or '2.'.
    """
    prompt = (
        f"Write the beginning of a bedtime story for a 5-10 year old about \"{topic}\". "
        "Introduce the main characters and conflict clearly. "
        "At the end, present exactly two numbered options for what should happen next,\n"
        "formatted like:\n"
        "1. Do X\n"
        "2. Do Y\n"
        "Do not resolve the story or include a moral yet."
    )
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7
    )
    content = resp.choices[0].message.content.strip()

    # Split into intro and options
    lines = content.splitlines()
    intro_lines = []
    options = []
    for line in lines:
        if re.match(r"^\s*[12]\.\s+", line):
            options.append(line.strip())
        else:
            intro_lines.append(line)
    intro = "\n".join(intro_lines).strip()
    # Ensure exactly two options
    if len(options) != 2:
        # Fallback: treat last two lines as options
        options = lines[-2:]
    return intro, options


def generate_branch_story(intro: str, choice: str) -> str:
    """
    Continue and complete the story based on the chosen option.
    If the option leads to a positive outcome, end with a positive moral;
    if it leads to a negative outcome, end with a cautionary moral.

    Returns:
        full_story (str): The completed story with resolution and moral.
    """
    prompt = (
        "You are an expert children's author writing for ages 5-10. "
        "Continue the story below based on the chosen option. "
        "Write a clear resolution and close with an appropriate moral that matches the outcome.\n\n"
        f"Story beginning:\n{intro}\n\n"
        f"Chosen option: {choice}\n"
        "Continue and finish the tale with a moral."
    )
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()
