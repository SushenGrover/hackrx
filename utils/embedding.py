# utils/embedding.py
import openai
import os

def summarize_clause(clause):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize this insurance clause in 1-2 sentences without losing key conditions:\n\n{clause}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def get_embeddings(sentences):
    client = openai.OpenAI(api_key="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")
    response = client.embeddings.create(
        input=sentences,
        model="text-embedding-ada-002"
    )
    return [item.embedding for item in response.data]  # Slightly changed access
