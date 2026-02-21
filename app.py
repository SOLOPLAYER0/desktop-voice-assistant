import datetime
from groq import Groq
from rag import retrieve_relevant  # <-- import RAG

client = Groq(api_key="ENTER YOUR GROQ API KEY")

def ask(query):
    
    now = datetime.datetime.now().strftime("%I:%M %p")
    
 
    context = retrieve_relevant(query)

    system_msg = (
        "You are Alice, a friendly, helpful and polite AI voice assistant. "
        "Keep responses short 2 - 3 sentences maximum, clear, and natural."
        f"The current time right now is: {now}. "
        "You know the user's personal schedule, routine, tasks, and day plan through the given context. "
        "If the user asks about their routine, what to do now, what is next, what is planned today, "
        "their gym schedule, study time, or daily tasks — answer using the context. "
        "If no relevant context exists, answer generally and politely. "
        f"\n\nRelevant context:\n{context}\n\n"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content


