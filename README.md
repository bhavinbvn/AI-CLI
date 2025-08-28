# 🚀 AI-Native CLI  

AI-Native CLI is a unified **command-line assistant** that lets developers perform software engineering tasks using **natural language**.  
Instead of typing exact commands or boilerplate code, you just tell the CLI what you want:  

```bash
ai-cli "create a FastAPI service called patient_api"
ai-cli "add a POST endpoint /predict to the FastAPI app"
ai-cli "create a basic html file named index.html with heading 'AI CLI'"
ai-cli "create a C program for summation"
```

The CLI parses your intent, generates structured actions, and executes them — creating files, scaffolding projects, running git, or launching processes.  

---

## ✨ Features  

- **AI-Powered Natural Language Interface**  
  - Converts plain English into structured developer operations.  
  - Supports **Ollama (local LLMs)** or **OpenAI** for parsing & code generation.  

- **Developer Operations**  
  - 📂 File creation (HTML, C, Python, etc.)  
  - ⚡ Project scaffolding (FastAPI boilerplates)  
  - 🌐 Add endpoints dynamically to FastAPI apps  
  - 🧑‍💻 Git init & commit automation  
  - ▶ Run project processes  

- **Logging & Output**  
  - JSON and Excel-based logging of all actions  
  - Schema: `Test Name, Description, Status, Error, Screenshot link`  
  - Rich CLI output with colors and formatted JSON  

---

## 🛠️ Installation  

Clone this repository:  

```bash
git clone https://github.com/yourusername/ai_native_cli.git
cd ai_native_cli
```

Create and activate a virtual environment:  

```bash
python -m venv .venv
.venv\Scripts\activate  # (Windows)
source .venv/bin/activate  # (Linux/Mac)
```

Install dependencies:  

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration  

### Option 1: Using **Ollama** (local LLMs, recommended)  
1. [Install Ollama](https://ollama.ai)  
2. Pull your preferred model (example: `qwen2:0.5b`):  
   ```bash
   ollama pull qwen2:0.5b
   ```
3. The CLI will connect to Ollama automatically at `http://localhost:11434`.

### Option 2: Using **OpenAI API**  
1. Get an API key from [OpenAI](https://platform.openai.com/account/api-keys).  
2. Export it:  
   ```bash
   setx OPENAI_API_KEY "your_key_here"   # Windows
   export OPENAI_API_KEY="your_key_here" # Linux/Mac
   ```

---

## 🚀 Usage  

Run the CLI:  

```bash
ai-cli "create a basic html file named index.html"
```

Example outputs:  

**1. Create HTML file**  
```bash
ai-cli "create a basic html file named index.html with heading 'AI CLI'"
```
👉 Creates `index.html` with boilerplate HTML + `<h1>AI CLI</h1>`  

**2. Create FastAPI project**  
```bash
ai-cli "create a FastAPI service called patient_api"
```
👉 Generates `patient_api` scaffold with `app.py`  

**3. Add endpoint**  
```bash
ai-cli "add a GET endpoint /hello to the FastAPI app"
```
👉 Modifies `app.py` with a new `/hello` route  

**4. Git Operations**  
```bash
ai-cli "initialize git and commit with message 'first commit'"
```

---

## 📊 Logs & Outputs  

Every command is logged into:  

- `logs.json` → structured JSON logs  
- `logs.xlsx` → Excel sheet for tracking test runs  

Schema:  

| Test Name | Description              | Status   | Error           | Screenshot Link | Timestamp |
|-----------|--------------------------|----------|-----------------|-----------------|-----------|
| ad-hoc    | Created file index.html  | SUCCESS  | null            | null            | 2025-08-28 |

---

## 🏗️ Architecture  

```
User → ai-cli → NLU (Ollama/OpenAI) → Intent JSON → Executor → Action (file/git/process) → Logs
```

- **ai_cli/ai_nlu.py** → natural language parser (Ollama/OpenAI)  
- **ai_cli/core/executor.py** → executes actions (file ops, git, processes)  
- **ai_cli/actions/** → specific operation modules  
- **ai_cli/schemas.py** → log schemas  
- **ai_cli/core/logging.py** → JSON/Excel logging  

---

## 📌 Roadmap  

- [ ] AI code generation (not just templates) for arbitrary requests  
- [ ] Voice input/output  
- [ ] Plugin system for extending operations (Docker, Kubernetes, AWS)  
- [ ] Unit tests + CI  

---

## 🤝 Contributing  

1. Fork the repo  
2. Create your feature branch (`git checkout -b feature/awesome`)  
3. Commit your changes (`git commit -m 'feat: added awesome feature'`)  
4. Push and open a PR  

---

## 📜 License  

MIT License. See [LICENSE](LICENSE).  
