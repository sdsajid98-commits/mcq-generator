# 🌌 Galaxy MCQ Quiz Generator

A futuristic, neon-themed Streamlit app to generate AI-powered MCQ quizzes using the Groq API.

---

## Features

- Generate quizzes dynamically based on:
  - Topic (e.g., Biology, Finance, Islamic Studies)
  - Difficulty (Easy, Medium, Hard)
  - Number of questions
- AI-powered MCQ generation via Groq API
- Track user answers and calculate scores
- Neon/glass aesthetic with animated stars and progress bars
- Correct/incorrect answer highlighting
- Responsive and interactive forms using Streamlit session state

---

## Installation

1. Clone the repository:

    git clone <your-repo-url>
    cd <repo-folder>

2. Create a virtual environment (optional but recommended):

    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

3. Install dependencies:

    pip install -r requirements.txt

4. Set up API keys:

- Replace the placeholder API key in the script:
  
    client = GroqClient(api_key="YOUR_API_KEY_HERE")

---

## Usage

Run the Streamlit app:

    streamlit run app.py

- Enter the quiz topic, difficulty, and number of questions.
- Click **🚀 Generate Quiz** to fetch questions from AI.
- Answer the MCQs in the form.
- Submit your answers and view your neon-styled score and progress bar.

---

## Dependencies

- Python 3.x  
- Streamlit  
- Groq Client (`groq-client`)  
- JSON  

*(You can generate `requirements.txt` by running `pip freeze > requirements.txt`)*

---

## Developer

👩‍💻 Developed by **Siddiqa Ali**

---

## License

MIT License
