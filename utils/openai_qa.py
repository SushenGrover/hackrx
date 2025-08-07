# utils/openai_qa.py
import os
import openai
import asyncio

client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ask_gpt_async(context_clauses, question):
    prompt = (
        "You are a legal assistant specialized in understanding insurance contracts, terms, and provisions for effective legal interpretation.\n\n"
        "Given the clauses below, answer the question using the exact style and language of official policy summaries:\n"
        "- Do not introduce or assume facts not present in the context.\n"
        "- Include only explicitly mentioned time durations, INR amounts, or percentages.\n"
        "- Do NOT restate the question or mention the policy name.\n"
        "- Be clear, precise, and specific.\n\n"
        "Examples:\n"
        "- A grace period of thirty days is provided after the premium due date without loss of continuity benefits.\n"
        "- Yes, maternity expenses are covered after 24 months, limited to two deliveries.\n"
        "- Yes, organ donor's hospitalisation for harvesting is covered, but post-operative treatment is excluded.\n"
        "- Room rent limited to 1% of SI per day; ICU at 2% of SI.\n\n"
        "---\n"
        + "\n---\n".join(context_clauses)
        + f"\n\nQuestion:\n{question}\n\nAnswer:"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        print(f"[Warning] gpt-4o failed: {e}. Falling back to gpt-4.")
        try:
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Error] GPT fallback failed: {e}")
            return "Unable to retrieve a response due to system error."
