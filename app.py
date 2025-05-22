import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import openai
from openai import RateLimitError

from lib.generator import generate_story, generate_branch_story
from lib.judge import critique_story
from lib.refiner import refine_story

# Load environment variables and set API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI(title="Bedtime Story AI", version="0.1.0")

# Pydantic models for requests and responses
class StoryRequest(BaseModel):
    topic: str
    refinement_rounds: int = 1  # number of critique-refine cycles

class StoryDraft(BaseModel):
    draft: str
    options: List[str]

class StoryCritique(BaseModel):
    critique: str

class StoryRefine(BaseModel):
    story: str
    critique: str

class StoryResponse(BaseModel):
    draft: str
    options: List[str]
    critique: str
    final: str

class BranchRequest(BaseModel):
    intro: str
    choice: str

class BranchResponse(BaseModel):
    full_story: str

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok", "version": app.version}

# Full pipeline: draft -> critique -> refine
@app.post("/story", response_model=StoryResponse)
async def full_story(req: StoryRequest):
    try:
        draft, options = generate_story(req.topic)
        critique = critique_story(draft)
        final = draft
        for _ in range(req.refinement_rounds):
            final = refine_story(final, critique)
            critique = critique_story(final)
        return StoryResponse(
            draft=draft,
            options=options,
            critique=critique,
            final=final
        )
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded or insufficient quota.")

# Generate draft only
@app.post("/story/draft", response_model=StoryDraft)
async def get_draft(req: StoryRequest):
    try:
        draft, options = generate_story(req.topic)
        return StoryDraft(draft=draft, options=options)
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded or insufficient quota.")

# Critique only
@app.post("/story/critique", response_model=StoryCritique)
async def get_critique(req: StoryDraft):
    try:
        critique = critique_story(req.draft)
        return StoryCritique(critique=critique)
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded or insufficient quota.")

# Refine only
@app.post("/story/refine", response_model=StoryDraft)
async def get_refine(req: StoryRefine):
    try:
        final = refine_story(req.story, req.critique)
        # After refine, no new options
        return StoryDraft(draft=final, options=[])
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded or insufficient quota.")

# Branch continuation endpoint
@app.post("/story/branch", response_model=BranchResponse)
async def branch_story(req: BranchRequest):
    try:
        full = generate_branch_story(req.intro, req.choice)
        return BranchResponse(full_story=full)
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded or insufficient quota.")

# Run with: uvicorn app:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)