from fastapi import FastAPI
from pydantic import BaseModel
import os
import httpx
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import asyncio

load_dotenv()

app = FastAPI(title="Multi AI Summarizer")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "multi-ai-summarizer backend running!"}

# ---------------- Request Model ----------------
class QueryRequest(BaseModel):
    query: str
    providers: list[str]

# ---------------- Cache ----------------
CACHE = {}

def get_cached(query: str, provider: str):
    return CACHE.get(f"{provider}_{query}")

def set_cache(query: str, provider: str, response: str):
    CACHE[f"{provider}_{query}"] = response

# ---------------- Simulated response ----------------
def simulate_response(provider: str, query: str) -> str:
    return f"[{provider} simulated response for query: '{query}'] ⚠️ Provider not accessible in free mode."

# ---------------- Gemini ----------------
async def list_gemini_models(api_key: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json().get("models", [])

def select_text_generation_model(models: list) -> str | None:
    for model in models:
        if "generateText" in model.get("supportedGenerationMethods", []):
            return model["name"]
    return None

async def call_gemini(query: str) -> str:
    cached = get_cached(query, "gemini")
    if cached:
        return cached

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        response = simulate_response("Gemini", query)
        set_cache(query, "gemini", response)
        return response

    try:
        models = await list_gemini_models(api_key)
        model_name = select_text_generation_model(models)
        if not model_name:
            response = "[Gemini: no accessible text-generation model] ⚠️ Free tier does not allow text-generation yet."
            set_cache(query, "gemini", response)
            return response

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateText?key={api_key}"
        payload = {"prompt": {"text": query}, "temperature": 0.7, "candidate_count": 1}

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            candidates = data.get("candidates")
            if candidates:
                response = candidates[0].get("content", "[Gemini returned empty content]")
            else:
                response = "[Gemini returned no candidates]"
    except Exception as e:
        response = f"[Gemini call failed: {str(e)}] ⚠️ Free tier or missing access"

    set_cache(query, "gemini", response)
    return response

# ---------------- Cohere ----------------
async def call_cohere(query: str) -> str:
    cached = get_cached(query, "cohere")
    if cached:
        return cached

    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        response = simulate_response("Cohere", query)
        set_cache(query, "cohere", response)
        return response

    url = "https://api.cohere.ai/v1/generate"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": "command", "prompt": query, "max_tokens": 200}  # reduced max_tokens to save cost

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            generations = data.get("generations")
            if generations:
                response = generations[0].get("text", "[Cohere returned empty text]").strip()
            else:
                response = "[Cohere returned no generations]"
    except Exception as e:
        response = f"[Cohere call failed: {str(e)}] ⚠️ Free tier or missing access"

    set_cache(query, "cohere", response)
    return response

# ---------------- OpenAI ----------------
async def call_openai(query: str) -> str:
    cached = get_cached(query, "openai")
    if cached:
        return cached

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        response = simulate_response("OpenAI", query)
        set_cache(query, "openai", response)
        return response

    try:
        openai.api_key = api_key
        response_obj = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            temperature=0.7,
            max_tokens=200  # reduced max_tokens
        )
        response = response_obj.choices[0].message.content.strip()
    except Exception as e:
        response = f"[OpenAI call failed: {str(e)}] ⚠️ Free tier or missing access"

    set_cache(query, "openai", response)
    return response

# ---------------- Claude ----------------
async def call_claude(query: str) -> str:
    cached = get_cached(query, "claude")
    if cached:
        return cached

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        response = simulate_response("Claude", query)
        set_cache(query, "claude", response)
        return response

    # Placeholder for real API call
    response = simulate_response("Claude", query)
    set_cache(query, "claude", response)
    return response

# ---------------- Perplexity ----------------
async def call_perplexity(query: str) -> str:
    cached = get_cached(query, "perplexity")
    if cached:
        return cached

    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        response = simulate_response("Perplexity", query)
        set_cache(query, "perplexity", response)
        return response

    # Placeholder for real API call
    response = simulate_response("Perplexity", query)
    set_cache(query, "perplexity", response)
    return response

# ---------------- Summarizer ----------------
def summarize_responses(responses: dict) -> str:
    valid_texts = [text for text in responses.values() if not text.lower().startswith("[")]
    if not valid_texts:
        return "⚠️ No valid responses received."
    return " ".join(valid_texts)

@app.post("/ask")
async def ask(request: QueryRequest):
    query = request.query
    selected_providers = request.providers
    results = {}
    sources_used = []

    tasks = []
    for provider in selected_providers:
        if provider == "gemini":
            tasks.append(call_gemini(query))
        elif provider == "cohere":
            tasks.append(call_cohere(query))
        elif provider == "openai":
            tasks.append(call_openai(query))
        elif provider == "claude":
            tasks.append(call_claude(query))
        elif provider == "perplexity":
            tasks.append(call_perplexity(query))
        else:
            # simulated
            tasks.append(call_placeholder(provider.capitalize(), query))
        sources_used.append(provider.capitalize())

    responses = await asyncio.gather(*tasks)

    for i, provider in enumerate(selected_providers):
        results[provider] = responses[i]

    summary = summarize_responses(results)

    return {
        "query": query,
        "summary": summary,
        "responses": results,
        "sources": sources_used
    }
