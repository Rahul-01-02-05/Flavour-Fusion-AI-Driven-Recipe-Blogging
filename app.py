import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

# ---------- PAGE CONFIG ----------

st.set_page_config(
page_title="Flavour Fusion",
page_icon="🍲",
layout="centered"
)

# ---------- GLASS UI CSS ----------

st.markdown("""

<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

h1 {
    text-align: center;
    color: white;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #ddd;
    margin-bottom: 10px;
}

.recipe-box {
    background: rgba(0,0,0,0.35);
    padding: 20px;
    border-radius: 15px;
    color: white;
    margin-top: 15px;
}
</style>

""", unsafe_allow_html=True)

# ---------- LOAD API ----------

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key is None:
    st.error("API key not found. Check .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# ---------- SIDEBAR ----------

st.sidebar.title("⚙️ Controls")

words = st.sidebar.slider("Recipe length", 100, 800, 300)

style = st.sidebar.selectbox(
"Writing style",
["Professional", "Friendly", "Fun"]
)

# ---------- FUNCTIONS ----------

def get_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break… it froze.",
        "Debugging: where you fix one bug and create three."
        ]
    return random.choice(jokes)


def generate_recipe(topic, words, style):
    if topic.strip() == "":
        return "Please enter a recipe topic."
    prompt = f"""
    Write a {style.lower()} recipe blog about {topic}
    in around {words} words.
    Include introduction, ingredients,
    step-by-step instructions and tips.
    """
    response = model.generate_content(prompt)
    return response.text

# ---------- HEADER CARD ----------

st.markdown("""

<div class="main-card">
    <h1>🍲 Flavour Fusion</h1>
    <div class="subtitle">AI-Powered Recipe Generator</div>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT CARD ----------

st.markdown('<div class="main-card">', unsafe_allow_html=True)

topic = st.text_input("Enter recipe topic")

generate = st.button("✨ Generate Recipe")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- OUTPUT ----------

if generate:
    st.info(get_joke())
    recipe = generate_recipe(topic, words, style)
    st.markdown(
        f'<div class="recipe-box">{recipe}</div>',
        unsafe_allow_html=True
        )

