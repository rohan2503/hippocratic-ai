import openai

def critique_story(story: str) -> str:
    """Ask the LLM to critique the story for age-appropriateness, structure, etc."""
    critique_prompt = (
        "You are a children's story critic for ages 5-10. "
        "Read the story below and point out any issues (hard words, confusing structure, missing lesson). "
        "Then suggest specific improvements.\n\n"
        f"Story:\n\"\"\"\n{story}\n\"\"\"\n\nCritique:"
    )
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": critique_prompt}],
        max_tokens=150,
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()
