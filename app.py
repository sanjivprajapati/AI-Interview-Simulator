import streamlit as st
import random
import pandas as pd
import google.generativeai as genai
if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="AI Interview Simulator")

st.title("🎤 AI Interview Simulator")

# Session State
if "history" not in st.session_state:
    st.session_state.history = []

if "question" not in st.session_state:
    st.session_state.question = ""
st.write(
    f"Question {st.session_state.current_index + 1}/5"
)
# Questions
questions = {
    "Software Engineer": [
        "Explain OOP concepts.",
        "Difference between Stack and Queue?",
        "Tell me about yourself."
    ],
    "Data Analyst": [
        "What is Data Cleaning?",
        "Difference between SQL and Excel?",
        "Tell me about yourself."
    ],
    "AI/ML Engineer": [
        "What is Overfitting?",
        "Difference between AI and ML?",
        "Tell me about yourself."
    ],
    "HR": [
        "Why should we hire you?",
        "What are your strengths?",
        "Tell me about yourself."
    ]
}

# Role Selection
role = st.selectbox(
    "Choose Role",
    list(questions.keys())
)

# Start Interview
if st.button("Start Interview"):

    prompt = f"""
    Generate 5 interview questions for {role} role.

    Return only questions.
    One question per line.
    """

    response = model.generate_content(prompt)

    generated_questions = response.text.split("\n")

    generated_questions = [
        q.strip("- ").strip()
        for q in generated_questions
        if q.strip()
    ]

    st.session_state.questions = generated_questions
    st.session_state.current_index = 0

    st.session_state.question = generated_questions[0]
# Show Question
if st.session_state.question != "":

    st.write("## Question:")
    st.write(st.session_state.question)

    answer = st.text_area("Your Answer")

    # Submit Button
# Submit Button
    if st.button("Submit"):

      prompt = f"""
      You are an interview evaluator.

      Question:
      {st.session_state.question}

      Candidate Answer:
      {answer}

      Give:
      1. Score out of 10
      2. Strengths
      3. Weaknesses
      4. Suggestions

      Keep response short.
      """

      response = model.generate_content(prompt)

      st.write("## AI Feedback")
      st.write(response.text)

      score = min(len(answer) // 10, 10)

      chance = min(score * 10, 95)

      st.write(f"🎯 Selection Chance: {chance}%")

      st.session_state.history.append(chance)

      if chance >= 80:
        st.success("High chance of selection 🚀")

      elif chance >= 50:
        st.warning("Average chance — improve answers.")

      else:
        st.error("Need more practice.")

# Next Question
if st.button("Next Question"):

    if st.session_state.current_index < len(st.session_state.questions) - 1:

        st.session_state.current_index += 1

        st.session_state.question = (
            st.session_state.questions[
                st.session_state.current_index
            ]
        )
    else:
        st.success("Interview Completed 🎉")
# History
if len(st.session_state.history) > 0:

    best_score = max(st.session_state.history)

    avg_score = (
        sum(st.session_state.history)
        / len(st.session_state.history)
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Average Score", f"{avg_score:.1f}%")

    with col2:
        st.metric("Best Score", f"{best_score}%")

    df = pd.DataFrame(
        st.session_state.history,
        columns=["Score"]
    )

    st.line_chart(df)