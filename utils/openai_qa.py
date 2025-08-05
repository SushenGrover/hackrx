import os
import openai

def ask_gpt(context_clauses, question):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = (
        "You are an expert insurance contract analyst. "
        "Given the following clauses, answer precisely and formally, including all key conditions and legal references. "
        "If uncertain, say so clearly.\n"
    )
    user_prompt = (
        system_prompt +
        "\n---\n".join(context_clauses) +
        f"\n\nAnswer the question: {question}\n" +
        "Answer in formal contract style, using accurate terminology.\n"
    )
    
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if budget constrained
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=75,  # adjust as needed for length
        temperature=0.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return response.choices[0].message.content
