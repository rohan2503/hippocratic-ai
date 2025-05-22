# Bedtime Story AI

An interactive storytelling app that generates uplifting, age-appropriate bedtime stories for children ages 5–10. It features a Choose-Your-Own-Adventure (CYOA) mode, plus automatic critique & refinement, and a clean REST API. The CLI also supports on-the-fly illustrations via DALL·E—you’ll get a copy-pasted URL you can open in your browser.

---

## 🚀 Features

- **AI-Generated Stories**  
  Simple, positive tales with a clear beginning, conflict, resolution, and moral.

- **Choose-Your-Own-Adventure**  
  At key points, kids choose between two branches. The story continues and ends based on their pick.

- **Feedback Loop**  
  Each draft is automatically critiqued and refined to improve clarity and language for ages 5–10.

- **Illustrations with DALL·E**  
  After the final story prints in the CLI, you’ll receive a pre-signed URL to a colorful DALL·E illustration—just copy & paste it into your browser.

- **Multiple Interfaces**  
  - **CLI**: Run end-to-end in your terminal.  
  - **REST API**: Integrate into your own app or webpage.

- **Custom Topics**  
  Ask for a story on any subject (“fox and grapes,” “space explorer turtle,” etc.).

---

## 📋 Requirements

- **Python** 3.8 or higher  
- **OpenAI API key** (GPT-3.5-turbo + DALL·E)  
- **Dependencies** listed in `requirements.txt`

---


## 🛠 Installation & Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/rohan2503/hippocratic-ai.git
   cd hippocratic-ai
   ```

2. **(Optional) Create a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**  
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=sk-...
     ```

---

## 🚦 Usage

### 1. CLI/Interactive Use

```bash
python3 main.py
```

### 2. Run the API Server

Start the FastAPI server:
```bash
uvicorn app:app --reload
```
Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

#### Key Endpoints

- **Start a CYOA Story:**
  ```
  POST /start
  {
    "topic": "a brave squirrel"
  }
  ```
  Returns the story intro and two choices.

- **Continue the CYOA Story:**
  ```
  POST /continue
  {
    "story_so_far": "<intro text>",
    "choice": "1. Climb the tallest tree"
  }
  ```
  Returns the next segment and a new set of choices.

- **Classic Story Generation:**
  ```
  POST /story
  {
    "topic": "space adventure",
    "refinement_rounds": 1
  }
  ```



---

## 🧩 Example

**Request:**
```json
POST /start
{ "topic": "a lost kitten" }
```

**Response:**
```json
{
  "story_segment": "Once there was a kitten named Fluffy who wandered away from home. She saw a dark forest and a sunny meadow ahead.",
  "question": "1. Explore the dark forest\n2. Run to the sunny meadow"
}
```

---

## 📝 License

MIT License

---

