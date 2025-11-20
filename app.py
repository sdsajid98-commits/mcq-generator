import streamlit as st
from groq_client import generate_mcqs
from prompts import generate_mcq_prompt
import json

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "submit_quiz" not in st.session_state:
    st.session_state.submit_quiz = False

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Galaxy MCQ Quiz Generator", layout="wide")

# -----------------------------
# CSS STYLING
# -----------------------------
st.markdown("""
<style>
/* App container and background */
[data-testid="stAppViewContainer"] {
    position: relative;
    background: radial-gradient(circle at top, #2b0057, #0a001a 60%);
    color: #e4d9ff;
    overflow: hidden;
}

/* Stars */
#stars {
    position: absolute;
    top: 0;
    left: 0;
    width: 200%;
    height: 200%;
    z-index: 0;
    pointer-events: none;
    background: transparent;
    box-shadow:
      50px 80px white,
      150px 200px white,
      250px 100px white,
      400px 50px white,
      500px 300px white,
      600px 200px white,
      700px 150px white,
      800px 350px white,
      900px 400px white,
      1000px 100px white;
    animation: twinkle 5s infinite alternate;
}

@keyframes twinkle {
    0% { transform: translate(0px,0px); opacity: 0.8; }
    50% { transform: translate(1px,-1px); opacity: 1; }
    100% { transform: translate(-1px,1px); opacity: 0.9; }
}

/* Neon headings */
.title-glow {
    font-size: 50px !important;
    font-weight: 800;
    color: #d9b8ff;
    text-align: center;
    text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 40px #8b00ff, 0 0 80px #8b00ff;
}

.sub-title {
    font-size: 20px !important;
    text-align: center;
    color: #c9aaff !important;
    margin-top: -10px;
    text-shadow: 0 0 5px #c9aaff, 0 0 10px #b88cff;
}

/* Glass card */
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 20px;
    margin: 20px 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(125, 0, 255, 0.5);
    position: relative;
    z-index: 1;
}

/* Inputs */
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.1) !important;
    color: #2b0057 !important;
    border-radius: 10px !important;
    border: 1px solid #b88cff !important;
    box-shadow: 0 0 10px #b88cff inset;
}

.stTextInput input::placeholder {
    color: #8b00ff !important;
    opacity: 1;
}

/* Labels & slider text */
.stTextInput label, .stSelectbox label, .stSlider label, h2, h3 {
    color: #ffd6ff !important;
    text-shadow: 0 0 3px #b88cff;
}

/* Sliders */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #ff00e6, #8b00ff) !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(45deg, #b76eff, #ffb48f) !important;
    color: #fff !important;
    padding: 12px 30px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    border: none;
    box-shadow: 0 0 20px rgba(180, 0, 255, 0.8), 0 0 40px rgba(125,0,255,0.5);
    transition: 0.3s;
    position: relative;
    z-index: 2;
}
.stButton>button:hover {
    background: linear-gradient(45deg, #d19fff, #ffcfa0) !important;
    transform: scale(1.05);
}

/* Section headings inside cards */
h2, h3, label, .stMarkdown {
    color: #d8c2ff !important;
    font-weight: 600 !important;
    text-shadow: 0 0 5px #b88cff;
}

/* MCQ options - force white text no matter what */
.stRadio [role="radiogroup"] label,
.stRadio [role="radiogroup"] label span,
.stRadio [role="radiogroup"] div {
    color: #ffffff !important;
    font-weight: 600 !important;
    text-shadow: none !important;
}

/* Correct answer highlight */
.correct-answer {
    background-color: rgba(0, 255, 153, 0.1);
    border-left: 5px solid #00ff99;
    padding-left: 10px;
    border-radius: 5px;
}

/* Wrong answer highlight */
.wrong-answer {
    background-color: rgba(255, 102, 102, 0.1);
    border-left: 5px solid #ff6666;
    padding-left: 10px;
    border-radius: 5px;
}

/* Progress bar container */
.progress-container {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 20px;
    width: 100%;
    margin: 10px 0;
}

/* Progress bar fill */
.progress-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #b76eff, #ffb48f);
    border-radius: 10px;
    transition: width 0.5s ease-in-out;
}

/* Neon score animation */
.score-glow {
    font-size: 24px;
    font-weight: bold;
    color: #00ffcc;
    text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffee, 0 0 20px #00ccff;
    animation: pulse 1.5s infinite alternate;
}

@keyframes pulse {
    from { text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffee; }
    to   { text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffee; }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# STAR LAYER
# -----------------------------
st.markdown('<div id="stars"></div>', unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<h1 class="title-glow">🌌 MCQ Quiz Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Create futuristic AI-powered quizzes</p>', unsafe_allow_html=True)

# -----------------------------
# INPUT FORM (GLASS CARD)
# -----------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("## 🔮 Quiz Settings")

with st.form("quiz_form"):
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Topic:", placeholder="e.g. Biology, Islamic Studies, Finance")
    with col2:
        difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"])
    num_questions = st.slider("Number of Questions:", 1, 30, 5)
    generate = st.form_submit_button("🚀 Generate Quiz")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# GENERATE MCQS AND SAVE TO SESSION STATE
# -----------------------------
if generate:
    # Show quiz settings
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"""
        <h3 style="color:#e6d7ff;"> Quiz Settings</h3>
        <p style="color:#f0e5ff;"><b>Topic:</b> {topic}</p>
        <p style="color:#f0e5ff;"><b>Difficulty:</b> {difficulty}</p>
        <p style="color:#f0e5ff;"><b>Number of Questions:</b> {num_questions}</p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Call Groq API
    prompt = generate_mcq_prompt(topic, difficulty, num_questions)
    ai_response = generate_mcqs(prompt)

    # Parse JSON
    try:
        st.session_state.mcqs = json.loads(ai_response)
    except json.JSONDecodeError:
        st.error("⚠️ Failed to parse AI response. Try again.")
        st.session_state.mcqs = []

    # Reset previous answers & submit flag
    st.session_state.user_answers = {}
    st.session_state.submit_quiz = False

# -----------------------------
# Display Quiz Form with radio buttons
# -----------------------------
if st.session_state.mcqs:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 🎮 Quiz Time!")

    with st.form("quiz_answers_form"):
        for idx, q in enumerate(st.session_state.mcqs, 1):
            st.markdown(f"**Q{idx}: {q['question']}**")
            st.session_state.user_answers[f"q{idx}"] = st.radio(
                "",
                q['options'],
                key=f"q{idx}",
                label_visibility="collapsed"
            )

        submit_quiz = st.form_submit_button("📝 Submit Answers")
        if submit_quiz:
            st.session_state.submit_quiz = True

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Show Results & Score
# -----------------------------
if st.session_state.submit_quiz:
    score = 0
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## ✨ Results")

    for idx, q in enumerate(st.session_state.mcqs, 1):
        user_ans = st.session_state.user_answers.get(f"q{idx}", "No answer")
        correct_ans = q['answer']

        if user_ans == correct_ans:
            score += 1
            st.markdown(f"<div class='correct-answer'>✅ {user_ans}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='wrong-answer'>❌ {user_ans} | Correct: {correct_ans}</div>",
                        unsafe_allow_html=True)

    # Show total score neon
    st.markdown(f"<div class='score-glow'>🎯 Total Score: {score} / {len(st.session_state.mcqs)}</div>", unsafe_allow_html=True)

    # Show progress bar
    st.markdown(f"""
        <div class='progress-container'>
            <div class='progress-fill' style='width:{(score / len(st.session_state.mcqs)) * 100}%;'></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
