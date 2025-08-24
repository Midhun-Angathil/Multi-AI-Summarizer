import os, httpx

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

async def summarize_responses(question: str, responses: dict):
    if not OPENAI_KEY:
        return "Summarizer disabled - add OpenAI key in .env"

    combined = f"User Question: {question}\n\n"
    for provider, resp in responses.items():
        combined += f"\n{provider}:\n{resp}\n"

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Summarize and merge responses into one concise helpful answer."},
                    {"role": "user", "content": combined}
                ]
            }
        )
        return r.json()["choices"][0]["message"]["content"]
