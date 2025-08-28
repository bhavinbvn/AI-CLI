# import os
# import requests
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# # Try to load OpenAI API key
# api_key = os.getenv("OPENAI_API_KEY")
# client = None
# if api_key:
#     client = OpenAI(api_key=api_key)


# def parse_instruction_ai(text: str) -> dict:
#     """
#     Try OpenAI GPT first. If quota/connection fails, fallback to Ollama local model.
#     """
#     # --- Try OpenAI ---
#     if client:
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4o-mini",   # or "gpt-3.5-turbo" for cheaper
#                 messages=[
#                     {"role": "system", "content": "You are a CLI NLU parser. Convert user instructions into structured JSON {intent, args}. Only output JSON."},
#                     {"role": "user", "content": text}
#                 ]
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             print(f"[WARN] OpenAI failed → falling back to Ollama ({e})")

#     # --- Fallback to Ollama ---
#     try:
#         resp = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "qwen2:0.5b",
#                 "prompt": f"Respond ONLY with valid JSON. Convert this into structured JSON with keys intent and args only: {text}",
#                 "stream": False
#             }
#         )
#         data = resp.json()
#         raw = data.get("response", "").strip()
#         return json.loads(raw)
#     except Exception as e:
#         return {"intent": "unknown", "args": {}, "error": str(e)}




import os
import requests
import json

def parse_instruction_ai(text: str) -> dict:
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2:0.5b",
                "prompt": f"""You are a command parser.
Return ONLY valid JSON, nothing else.
Format:
{{
  "intent": "string",
  "args": {{}}
}}

Examples:
User: create a basic html file named index.html
Output: {{
  "intent": "create_file",
  "args": {{"name": "index.html", "type": "html"}}
}}

Now parse this request:
{text}""",
                "stream": False
            }
        )
        data = resp.json()
        raw = data.get("response", "").strip()

        # Try to extract JSON between braces
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end != -1:
            raw = raw[start:end]

        return json.loads(raw)
    except Exception as e:
        return {"intent": "unknown", "args": {}, "error": str(e)}