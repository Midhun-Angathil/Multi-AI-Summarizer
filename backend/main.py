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

class QueryRequest(BaseModel):
    query: str
    providers: list[str]
    history: list[dict] | None = None

CACHE = {}
def get_cached(query: str, provider: str):
    return CACHE.get(f"{provider}_{query}")
def set_cache(query: str, provider: str, response: str):
    CACHE[f"{provider}_{query}"] = response

def simulate_response(provider: str, query: str) -> str:
    return f"[{provider} simulated response for query: '{query}'] ⚠️ Provider not accessible in free mode."

# ---------------- Providers ----------------
async def call_gemini(query: str, history: list[dict] = None) -> str:
    cached = get_cached(query, "gemini")
    if cached:
        return cached
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        response = "⚠️ Gemini API key missing. Set GEMINI_API_KEY in .env"
        set_cache(query, "gemini", response)
        return response
    try:
        # If Gemini supports history, concatenate history into the prompt
        prompt = ""
        if history:
            for m in history:
                role = "AI" if m.get("role") == "ai" else "User"
                prompt += f"{role}: {m.get('content','')}\n"
        prompt += f"User: {query}\nAI:"
        url_models = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url_models)
            r.raise_for_status()
            models = r.json().get("models", [])
        model_name = None
        for m in models:
            if "generateText" in m.get("supportedGenerationMethods", []):
                model_name = m["name"]
                break
        if not model_name:
            response = "⚠️ Gemini no accessible text-generation model."
            set_cache(query, "gemini", response)
            return response
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateText?key={api_key}"
        payload = {"prompt": {"text": prompt}, "temperature": 0.4, "candidate_count": 1}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            candidates = data.get("candidates")
            if candidates:
                response = candidates[0].get("content", "[Gemini returned empty]")
            else:
                response = "[Gemini returned no candidates]"
    except Exception as e:
        response = f"⚠️ Gemini call failed: {str(e)}"
    set_cache(query, "gemini", response)
    return response

async def call_cohere(query: str, history: list[dict] = None) -> str:
    cached = get_cached(query, "cohere")
    if cached:
        return cached
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        response = "⚠️ Cohere API key missing. Set COHERE_API_KEY in .env"
        set_cache(query, "cohere", response)
        return response
    # If Cohere supports history, concatenate history into the prompt
    prompt = ""
    if history:
        for m in history:
            role = "AI" if m.get("role") == "ai" else "User"
            prompt += f"{role}: {m.get('content','')}\n"
    prompt += f"User: {query}\nAI:"
    url = "https://api.cohere.ai/v1/generate"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": "command", "prompt": prompt, "max_tokens": 300, "temperature": 0.4}
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            gens = data.get("generations")
            if gens:
                response = gens[0].get("text", "[Cohere returned empty]").strip()
            else:
                response = "[Cohere returned no generations]"
    except Exception as e:
        response = f"⚠️ Cohere call failed: {str(e)}"
    set_cache(query, "cohere", response)
    return response

async def call_openai(query: str, history: list[dict]) -> str:
    cached = get_cached(query, "openai")
    if cached:
        return cached
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        response = "⚠️ OpenAI API key missing. Set OPENAI_API_KEY in .env"
        set_cache(query, "openai", response)
        return response
    try:
        openai.api_key = api_key
        # Prompt engineered for concise high-quality summary
        messages = [{"role":"system","content":"Answer concisely and clearly, covering all critical points, avoid verbosity. Use short sentences."}]
        for m in (history or []):
            role = "assistant" if m.get("role")=="ai" else "user"
            messages.append({"role": role, "content": m.get("content","")})
        messages.append({"role":"user","content":query})
        response_obj = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.4,
            max_tokens=500
        )
        response = response_obj.choices[0].message.content.strip()
    except Exception as e:
        response = f"⚠️ OpenAI call failed: {str(e)}"
    set_cache(query, "openai", response)
    return response

async def call_claude(query: str, history: list[dict] = None) -> str:
    cached = get_cached(query, "claude")
    if cached:
        return cached
    # Simulate Claude, but you can add history logic if API supports it
    response = simulate_response("Claude", query)
    set_cache(query, "claude", response)
    return response

async def call_perplexity(query: str, history: list[dict] = None) -> str:
    cached = get_cached(query, "perplexity")
    if cached:
        return cached
    # Simulate Perplexity, but you can add history logic if API supports it
    response = simulate_response("Perplexity", query)
    set_cache(query, "perplexity", response)
    return response

# Helper function to generate AI-powered summary
async def generate_ai_summary(responses: dict, original_query: str) -> str:
    """Generate a unified summary using available AI providers in priority order"""
    valid_responses = {k: v for k, v in responses.items() if not v.startswith("⚠️")}
    
    if not valid_responses:
        return "⚠️ No valid responses received to summarize."
    
    # Create summarization prompt
    responses_text = ""
    for provider, response in valid_responses.items():
        responses_text += f"**{provider}**: {response}\n\n"
    
    summary_prompt = f"""Please provide a unified, comprehensive summary based on these AI responses to the question: "{original_query}"

AI Responses:
{responses_text}

Create a cohesive summary that combines the key insights from all responses, eliminates redundancy, and provides the most accurate and complete answer possible. Keep it concise but comprehensive."""

    # Try providers in priority order: OpenAI -> Cohere -> Gemini
    summary_providers = [
        ("openai", call_openai),
        ("cohere", call_cohere), 
        ("gemini", call_gemini)
    ]
    
    for provider_name, provider_func in summary_providers:
        try:
            if provider_name == "openai" and os.getenv("OPENAI_API_KEY"):
                summary = await provider_func(summary_prompt, [])
                if not summary.startswith("⚠️"):
                    return f"🤖 **AI-Generated Summary** (via {provider_name.upper()}):\n\n{summary}"
            elif provider_name == "cohere" and os.getenv("COHERE_API_KEY"):
                summary = await provider_func(summary_prompt, [])
                if not summary.startswith("⚠️"):
                    return f"🤖 **AI-Generated Summary** (via {provider_name.upper()}):\n\n{summary}"
            elif provider_name == "gemini" and os.getenv("GEMINI_API_KEY"):
                summary = await provider_func(summary_prompt, [])
                if not summary.startswith("⚠️"):
                    return f"🤖 **AI-Generated Summary** (via {provider_name.upper()}):\n\n{summary}"
        except Exception as e:
            continue
    
    # Fallback to simple concatenation if no AI summarizer is available
    return f"📝 **Combined Responses** (AI summarization unavailable):\n\n" + "\n\n---\n\n".join([f"**{k}**: {v}" for k, v in valid_responses.items()])

def summarize_responses(responses: dict, original_query: str = "") -> str:
    """Legacy function maintained for compatibility - now calls generate_ai_summary"""
    # Simple fallback for synchronous calls
    valid_texts = [v for v in responses.values() if not v.startswith("⚠️")]
    if not valid_texts:
        return "⚠️ No valid responses received."
    
    # For synchronous calls, return simple concatenation
    return "\n\n---\n\n".join([f"**{k}**: {v}" for k, v in responses.items() if not v.startswith("⚠️")])

@app.post("/ask")
async def ask(request: QueryRequest):
    query = request.query
    selected_providers = request.providers
    history = request.history or []
    results = {}
    sources_used = []

    tasks = []
    for provider in selected_providers:
        p_lower = provider.lower()
        if p_lower=="gemini":
            tasks.append(call_gemini(query, history))
        elif p_lower=="cohere":
            tasks.append(call_cohere(query, history))
        elif p_lower=="openai":
            tasks.append(call_openai(query, history))
        elif p_lower=="claude":
            tasks.append(call_claude(query, history))
        elif p_lower=="perplexity":
            tasks.append(call_perplexity(query, history))
        else:
            tasks.append(asyncio.sleep(0, result=simulate_response(provider.capitalize(), query)))
        sources_used.append(provider.capitalize())

    responses_list = await asyncio.gather(*tasks)
    for i, provider in enumerate(selected_providers):
        results[provider] = responses_list[i]

    # Generate AI-powered summary
    summary = await generate_ai_summary(results, query)

    return {
        "query": query,
        "summary": summary,
        "responses": results,
        "sources": sources_used
    }