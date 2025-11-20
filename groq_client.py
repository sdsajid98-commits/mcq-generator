import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)

def generate_mcqs(prompt_text, model: str = "llama-3.3-70b-versatile"):
    """
    Sends the prompt to Groq API using chat completions and returns the response text.
    """
    # Groq chat completion API
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful quiz generator."},
            {"role": "user", "content": prompt_text}
        ],
        model=model,
    )
    # response.choices is a list; get the first
    content = response.choices[0].message.content
    return content
