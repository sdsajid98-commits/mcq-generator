def generate_mcq_prompt(topic, difficulty, num_questions):
    """
    Returns a prompt string to send to Groq API to generate MCQs.
    """
    prompt = f"""
You are an expert quiz creator. Generate {num_questions} multiple-choice questions (MCQs)
on the topic "{topic}" with difficulty level "{difficulty}". 

Format the output as a JSON array like this:

[
  {{
    "question": "Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A"
  }},
  ...
]

Make sure each question has exactly 4 options and only one correct answer. 
Do not include any explanations.
"""
    return prompt
