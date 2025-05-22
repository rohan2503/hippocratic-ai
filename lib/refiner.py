import openai

def refine_story(original: str, critique: str) -> str:
    """Rewrite the story addressing the critique feedback."""
    refine_prompt = (
        "Revise the following story for a 5-10 year old, "
        "applying all the critique points below to improve clarity, tone, and structure.\n\n"
        "CRITICAL REQUIREMENTS:\n"
        "- Keep ALL original character names exactly the same\n"
        "- Always refer to animal characters with their animal type (e.g., 'Rosie the rabbit', 'Dottie the deer', 'Sam the squirrel')\n"
        "- Make it clear throughout the story that these are animal characters, not humans\n"
        "- Include animal-specific actions (hopping, leaping, scampering, etc.) where appropriate\n"
        "- Only simplify language and improve structure - do NOT remove animal identity\n\n"
        f"Original Story:\n\"\"\"\n{original}\n\"\"\"\n\n"
        f"Critique:\n\"\"\"\n{critique}\n\"\"\"\n\n"
        "Rewritten Story (remember to keep animal identities clear throughout):"
    )
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": refine_prompt}],
        max_tokens=400,
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()