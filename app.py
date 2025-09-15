import streamlit as st
from questions_store import load_storage_agent
from question_bank_agent import QuestionBankAgent, QuestionGeneratorAgent
from feedback_generator import FeedbackGenerator
from datetime import datetime
import os
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize agents
storage_agent = load_storage_agent("dynamic_questions.json")
question_bank = QuestionBankAgent()
question_generator = QuestionGeneratorAgent(question_bank)
feedback_generator = FeedbackGenerator(api_key=GEMINI_API_KEY, storage_file="dynamic_questions.json")

# Streamlit config
st.set_page_config(page_title="AI-Powered Interview App", layout="wide")
st.title("AI-Powered Excel & Data Interview Platform")

# --- Session state initialization ---
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "responses" not in st.session_state:
    st.session_state["responses"] = []
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "interview_started" not in st.session_state:
    st.session_state["interview_started"] = False
if "question_deadline" not in st.session_state:
    st.session_state["question_deadline"] = None
if "evaluations" not in st.session_state:
    st.session_state["evaluations"] = None
if "candidate_intro" not in st.session_state:
    st.session_state["candidate_intro"] = ""
if "timer_seconds" not in st.session_state:
    st.session_state["timer_seconds"] = 60  # seconds per question

# Sidebar controls
role = st.sidebar.selectbox("Select Candidate Role", ["finance", "operations", "data_analytics"])
num_questions = 8

# --- Intro screen ---
if not st.session_state["interview_started"]:
    st.header("📢 Welcome to the AI-Powered Excel & Data Interview Platform")
    st.markdown("""
    ### How this works:
    - You will be asked **8 questions one at a time**.  
    - Each question has a **time limit of 60 seconds**.  
    - After completing all, you’ll receive **detailed evaluation & feedback**.  
    """)
    st.session_state["candidate_intro"] = st.text_area(
        "👤 Please introduce yourself briefly before starting:",
        value=st.session_state.get("candidate_intro", ""),
        height=120
    )

    if st.button("🚀 Start Interview"):
        if st.session_state["candidate_intro"].strip() == "":
            st.warning("Please enter your introduction before starting.")
        else:
            # Generate questions
            questions = question_generator.generate_interview_questions(role=role, count=num_questions)
            st.session_state["questions"] = questions
            st.session_state["responses"] = [""] * len(questions)
            st.session_state["current_index"] = 0
            st.session_state["interview_started"] = True
            st.session_state["question_deadline"] = time.time() + st.session_state["timer_seconds"]
            st.session_state["evaluations"] = None
            st.rerun()

    if st.sidebar.button("Show Question Bank Analytics"):
        analytics = storage_agent.get_analytics()
        if "error" in analytics:
            st.error(analytics["error"])
        else:
            st.subheader("📊 Question Bank Analytics")
            st.metric("Total Questions", analytics['total_questions'])
            st.metric("Total Usage", analytics['total_usage'])
            st.metric("Average Effectiveness", analytics['average_effectiveness'])
            st.markdown("**Category Distribution:**")
            st.bar_chart(analytics['category_distribution'])
            st.markdown("**Difficulty Distribution:**")
            st.bar_chart(analytics['difficulty_distribution'])
            st.markdown("**Top Performing Questions:**")
            for tq in analytics['top_questions']:
                st.markdown(f"- {tq['question']} (Effectiveness: {tq['effectiveness']})")
    st.stop()

# --- Interview in progress ---
questions = st.session_state["questions"]
idx = st.session_state["current_index"]
total = len(questions)

# Auto-advance if timer ended
if st.session_state.get("question_deadline"):
    remaining = int(st.session_state["question_deadline"] - time.time())
    if remaining <= 0:
        # Save answer if any
        text_key = f"resp_{idx}"
        st.session_state["responses"][idx] = st.session_state.get(text_key, "")
        # Move to next question or mark complete
        if idx + 1 < total:
            st.session_state["current_index"] += 1
            st.session_state["question_deadline"] = time.time() + st.session_state["timer_seconds"]
        else:
            st.session_state["current_index"] = total
            st.session_state["question_deadline"] = None
        st.rerun()

# --- Check if interview complete ---
if st.session_state["current_index"] >= total:
    st.subheader("✅ Interview Complete — Evaluation & Feedback")
    if st.session_state["evaluations"] is None:
        qa_pairs = []
        for i, q in enumerate(questions):
            resp = st.session_state.get(f"resp_{i}", "") or st.session_state["responses"][i]
            qa_pairs.append({"question": q, "response": resp})
        st.session_state["evaluations"] = feedback_generator.generate_bulk_feedback(qa_pairs)

    evaluations = st.session_state["evaluations"]
    overall_scores = [f["score"] for f in evaluations]
    avg_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0
    st.metric("Overall Score", f"{round(avg_score,1)}/100")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Question-wise Feedback")
        for f in evaluations:
            st.markdown(f"**Q:** {f['question']}")
            st.markdown(f"**Answer:** {f['candidate_response']}")
            st.markdown(f"**Score:** {f['score']}/100")
            st.markdown(f"**Feedback:** {f['overall_feedback']}")
            st.markdown("---")
    with col2:
        st.subheader("Quick Metrics")
        strengths = []
        improvements = []
        for f in evaluations:
            strengths.extend(f.get("strengths", []))
            improvements.extend(f.get("improvements", []))
        strengths = list(dict.fromkeys([s for s in strengths if s]))[:10]
        improvements = list(dict.fromkeys([i for i in improvements if i]))[:10]
        if strengths:
            st.write("**Strengths:**")
            for s in strengths:
                st.write(f"- {s}")
        if improvements:
            st.write("**Improvements:**")
            for imp in improvements:
                st.write(f"- {imp}")
    if st.button("Start New Interview"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
    st.stop()

# --- Current question display ---
progress_pct = idx / total if total > 0 else 0
st.progress(progress_pct)
st.subheader(f"Question {idx+1} of {total}")
q = questions[idx]
st.markdown(f"**{q['question']}**")

# Answer box
text_key = f"resp_{idx}"
if text_key not in st.session_state:
    st.session_state[text_key] = st.session_state["responses"][idx] if idx < len(st.session_state["responses"]) else ""
answer = st.text_area("Your answer:", value=st.session_state[text_key], key=text_key, height=160,
                      placeholder="Type your answer here...")

# Timer display
if st.session_state.get("question_deadline"):
    remaining = int(st.session_state["question_deadline"] - time.time())
    if remaining > 0:
        st.warning(f"⏳ Time Remaining: {remaining} seconds")
    else:
        st.warning("⏳ Time Remaining: 0 seconds")

# Action buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Submit Answer"):
        st.session_state["responses"][idx] = st.session_state.get(text_key, "")
        if idx + 1 < total:
            st.session_state["current_index"] += 1
            st.session_state["question_deadline"] = time.time() + st.session_state["timer_seconds"]
        else:
            st.session_state["current_index"] = total
            st.session_state["question_deadline"] = None
        st.rerun()
with col2:
    if st.button("Skip / Next"):
        st.session_state["responses"][idx] = st.session_state.get(text_key, "")
        if idx + 1 < total:
            st.session_state["current_index"] += 1
            st.session_state["question_deadline"] = time.time() + st.session_state["timer_seconds"]
        else:
            st.session_state["current_index"] = total
            st.session_state["question_deadline"] = None
        st.rerun()
with col3:
    if st.button("Previous") and idx > 0:
        st.session_state["responses"][idx] = st.session_state.get(text_key, "")
        st.session_state["current_index"] -= 1
        st.session_state["question_deadline"] = time.time() + st.session_state["timer_seconds"]
        st.rerun()











st.rerun()