Bedtime Story AI
Bedtime Story AI is an interactive storytelling app that generates uplifting, age-appropriate bedtime stories for children ages 5–10. It features a unique Choose-Your-Own-Adventure (CYOA) mode, allowing children to make choices that shape the story’s direction and outcome.
Features
AI-Generated Stories: Simple, positive tales with clear structure and morals.
Choose-Your-Own-Adventure: At key points, children pick between two story branches.
API & Interactive Modes: Use via REST API or integrate into your own CLI/app.
Custom Topics: Generate stories about any topic you choose.
Requirements
Python 3.8+
OpenAI API key
Dependencies in requirements.txt (install with pip install -r requirements.txt)


Core Logic (lib/generator.py):

generate_story(topic) → returns (intro, ["1. …", "2. …"])

generate_branch_story(intro, choice) → returns a complete resolution + moral

Feedback Loop

lib/judge.py critiques a story draft

lib/refiner.py polishes it based on the critique

FastAPI Service (app.py):

GET /health → service status

POST /story/draft → { topic, refinement_rounds } → draft + options

POST /story → full pipeline: draft → critique → refine → returns { draft, options, critique, final }

POST /story/critique → critique only

POST /story/refine → refine only

POST /story/branch → continue a branch: { intro, choice } → full resolved story

Quick Start

Clone & virtualenv

git clone https://github.com/rohan2503/hippocratic-ai.git
cd hippocratic-ai
python3 -m venv venv
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Configure your API key

Copy .env.example to .env and drop in your OpenAI key:

OPENAI_API_KEY=sk-...

Run the CLI

python main.py

Spin up the API

uvicorn app:app --reload

Then visit http://127.0.0.1:8000/docs for interactive docs.

