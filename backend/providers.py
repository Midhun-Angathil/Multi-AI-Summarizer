import os, httpx

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
COHERE_KEY = os.getenv("COHERE_API_KEY")
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY")

async def ask_openai(question: str):
    if not OPENAI_KEY:
        return "[OpenAI disabled - add API key in .env]"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}"},
            json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": question}]}
        )
        return r.json()["choices"][0]["message"]["content"]

async def ask_claude(question: str):
    if not ANTHROPIC_KEY:
        return "[Claude disabled - add API key in .env]"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01"},
            json={"model": "claude-3-opus-20240229", "messages": [{"role": "user", "content": question}]}
        )
        return r.json()["content"][0]["text"]

async def ask_gemini(question: str):
    if not GEMINI_KEY:
        return "[Gemini disabled - add API key in .env]"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}",
            json={"contents": [{"parts": [{"text": question}]}]}
        )
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

async def ask_cohere(question: str):
    if not COHERE_KEY:
        return "[Cohere disabled - add API key in .env]"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.cohere.ai/v1/chat",
            headers={"Authorization": f"Bearer {COHERE_KEY}"},
            json={"model": "command-r-plus", "message": question}
        )
        return r.json()["text"]

async def ask_perplexity(question: str):
    if not PERPLEXITY_KEY:
        return "[Perplexity disabled - add API key in .env]"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {PERPLEXITY_KEY}"},
            json={"model": "sonar-medium-chat", "messages": [{"role": "user", "content": question}]}
        )
        return r.json()["choices"][0]["message"]["content"]
