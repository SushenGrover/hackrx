# utils/openai_qa.py
import os
import openai
import asyncio

client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ask_gpt_async(context_clauses, question):
    prompt = (
        "You are an expert insurance contract analyst. "
        "Given the following clauses, answer in concise formal language using correct insurance terminology. "
        "\n"
        "Context:\n" +
        "\n---\n".join(context_clauses) +
        f"\n\nQ: {question}\nA:"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=140
        )
        return response.choices[0].message.content.strip()
    except Exception:
        # fallback to gpt-4 if needed
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=140
        )
        return response.choices[0].message.content.strip()
