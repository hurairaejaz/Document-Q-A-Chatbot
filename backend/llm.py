from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
def generate_answer(question, chunks):
    """
    Generate answer from retrieved chunks using Groq.
    """
    context = "\n\n".join(chunks)
    prompt = f"""
You are an intelligent AI assistant.
Your task is to answer ONLY using the provided document context.
Instructions:
- Answer only from the context.
- Do not make up information.
- If the answer is not available in the context, reply:
  "I couldn't find this information in the uploaded document."
- Give complete and clear answers.
- Use bullet points whenever appropriate.
Document Context:
{context}
Question:
{question}
Answer:
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions only from uploaded documents."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM Error: {str(e)}"
    