# AI-Powered-Excel-Mock-Interviewer
The AI-Powered Excel Mock Interviewer is an autonomous system that evaluates a candidate’s Excel skills via a structured, intelligent, multi-turn interview. Unlike traditional manual interviews, this system provides consistent, scalable, and unbiased assessment, making the hiring process faster and more data-driven.

It simulates a real Excel interview, evaluates answers in real-time using AI, tracks performance, and generates detailed feedback reports.

## Problem Statement
Business Context

The organization is expanding Finance, Operations, and Data Analytics divisions. Excel proficiency is critical for new hires. Current challenges include:

Manual interviews are time-consuming and inconsistent.

Senior analysts spend excessive time in pre-screening.

Hiring pipeline slows, affecting organizational growth.

Goal: Build an AI-driven system to automatically assess Excel skills efficiently and consistently.


# Technology Stack & Justifications
Component	Choice	Justification

**Python 3.11**

Wide ecosystem for AI, ML, and data handling. Supports modern libraries, maintainable, and widely used in enterprise.

**Streamlit: UI Framework**

Interactive dashboards with session state. Supports real-time UI updates (timer, question navigation) without complex frontend frameworks.

**JSON-based Question Storage: Data Storage**

Lightweight, portable, and easily extensible. Tracks question usage, effectiveness, and candidate performance.

**LLM Integration (OpenAI/Gemini): AI Evaluation**

Allows semantic evaluation of open-ended responses. Capable of generating feedback and scoring based on correctness and completeness.

**Dynamic Question Bank: Template + Seed Questions**

Solves cold-start problem; templates auto-generate diverse questions, seed questions provide initial reliability.

Rationale:
All choices prioritize fast prototyping, low friction deployment, and scalability, while ensuring that AI evaluation is both data-driven and interpretable.

## Question Bank Design

basic_formulas:	SUM, AVERAGE, COUNT ->	Finance, Operations

lookup_functions:	VLOOKUP, INDEX-MATCH ->	Finance, Data Analytics

data_analysis:	PIVOT, FILTER, SORT ->	Operations, Data Analytics

advanced_formulas:	IF, SUMIF, COUNTIF ->	Data Analytics, Finance

data_manipulation:	CONCATENATE, TEXT, DATE	-> Operations

scenario_based:	DASHBOARD, REPORTING ->	Finance, Operations

Why:
Categorizing ensures role-specific focus, which increases relevance and reduces noise in evaluation.

# AI Evaluation Methodology

**Semantic Scoring:** Uses LLM to check answer correctness, completeness, and context.

**Keyword Matching:** For structured formulas, extracts Excel functions to ensure precise evaluation.

**Hybrid Scoring:** Combines numeric scoring (0–100) with textual feedback for candidates.

**Performance Tracking:** Updates usage_count, avg_score, success_rate, and effectiveness_score for each question.

# Timer & Session Handling

**Per-question timer** with countdown display

Auto-advance on timeout to prevent stalling

Streamlit **session state** used for storing:

  -Current question index
  
  -Candidate responses
  
  -Timer state


# 📈 Analytics & Reporting

**Question Metrics:** usage, avg_score, success_rate, effectiveness

**Role-wise Analysis:** identifies top and low-performing questions

**Candidate Summary Report:**

  -Question-wise performance
  
  -Strengths & weaknesses
  
  -Suggested improvement points


## Cold Start Strategy

Challenge: No pre-existing Excel interview dataset.

Solution:

**Template-based question generation:** Covers common Excel tasks

**Seed questions:** 5–10 verified questions per category

**Performance-driven refinement:** Candidate interactions update effectiveness scores

**Iterative improvement:** Questions with low effectiveness replaced or updated

Why:
Allows a scalable, self-learning system even without initial datasets.

## Installation & Usage
git clone https://github.com/yourusername/ai-excel-interviewer.git

cd ai-excel-interviewer

python -m venv venv

venv\Scripts\activate         # Windows

pip install -r requirements.txt

streamlit run app.py


**Add API keys in .env:**

GEMENI_API_KEY=<your_api_key>

## 📂 Project Structure
excel_mock_interviewer/
├─ app.py                 # Streamlit app with interview flow
├─ question_bank_agent.py # Templates, role/difficulty logic
├─ questions_store.py     # Storage, analytics, performance tracking
├─ feedback_generator.py  # LLM-based answer evaluation
├─ dynamic_questions.json # Seed questions and storage
├─ requirements.txt
└─ README.md

##  Future Enhancements

- **PDF Feedback Generation** – Export detailed performance reports for candidates in a shareable PDF format.
  
- **Integration with Zoom / Microsoft Teams** – Enable real-time interviews directly within popular video conferencing platforms.
  
- **Multi-Language Support** – Allow candidates to take interviews in their preferred language for inclusivity.
    
- **Voice-based Q&A System** – Integrate speech-to-text (for candidate responses) and text-to-speech (for interviewer questions) to simulate more natural, human-like interviews.
  
- **Advanced ML Evaluation** – Use predictive ML models to score responses without relying solely on LLM API calls, reducing latency and cost.
  
- **HR Dashboard with Analytics** – Provide recruiters with an admin dashboard that includes aggregate insights, candidate comparisons, and skill distribution trends.  

# Demo:
<img width="1804" height="908" alt="Screenshot 2025-09-15 231203" src="https://github.com/user-attachments/assets/44357def-0890-4b0e-a647-e6b5fc28b681" />
<img width="1797" height="849" alt="Screenshot 2025-09-15 231232" src="https://github.com/user-attachments/assets/44408380-0aa4-43b7-a70d-5b1179c54bb6" />
<img width="1796" height="840" alt="Screenshot 2025-09-15 231327" src="https://github.com/user-attachments/assets/8305340c-cdad-4623-a822-460beff275a1" />
<img width="1559" height="879" alt="Screenshot 2025-09-15 231606" src="https://github.com/user-attachments/assets/51b3abec-92cc-4583-ad05-3b1a235a316d" />
<img width="1300" height="743" alt="Screenshot 2025-09-15 231632" src="https://github.com/user-attachments/assets/f3a9c63b-2682-4fa3-ac5c-13667235abfc" />


## Key Takeaways

Structured, role-specific Excel interviews automated.

AI scoring combined with data-driven analytics.

Self-learning question bank solving cold start problem.

Real-time session handling and timer support using modern Streamlit methods.





