import openai

def refine_story(original: str, critique: str) -> str:
    """Rewrite the story addressing the critique feedback."""
    refine_prompt = (
        "Revise the following story for a 5-10 year old, "
        "applying all the critique points below to improve clarity, tone, and structure.\n\n"
        f"Original Story:\n\"\"\"\n{original}\n\"\"\"\n\n"
        f"Critique:\n\"\"\"\n{critique}\n\"\"\"\n\n"
        "Rewritten Story:"
    )
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": refine_prompt}],
        max_tokens=300,
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()