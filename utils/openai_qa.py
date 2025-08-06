# utils/openai_qa.py
import os
import openai
import asyncio

client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ask_gpt_async(context_clauses, question):
    prompt = (
        "You are a legal assistant trained in analyzing Indian health insurance policies. "
        "Given the clauses below, answer the question in concise, clause-style language used in official policy summaries. "
        "Do not add or assume any facts not in the context. Only use details mentioned in the clauses. "
        "Do not include INR amounts, percentages, or time durations unless explicitly mentioned.\n\n"
        "Be clear, accurate, and specific in 1–2 sentences. Do not restate the question or mention the policy name.\n\n"
        "Examples:\n"
        "- 'A grace period of thirty days is provided after the premium due date without loss of continuity benefits.'\n"
        "- 'Yes, maternity expenses are covered after 24 months, limited to two deliveries.'\n"
        "- 'Yes, organ donor’s hospitalisation for harvesting is covered, but post-operative treatment is excluded.'\n"
        "- 'Room rent limited to 1% of SI per day; ICU at 2% of SI.'\n\n"
        f"Context:\n---\n" + "\n---\n".join(context_clauses) +
        f"\n\nQ: {question}\nA:"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=160
        )
        return response.choices[0].message.content.strip()
    except Exception:
        # fallback to gpt-4 if needed
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=160
        )
        return response.choices[0].message.content.strip()
