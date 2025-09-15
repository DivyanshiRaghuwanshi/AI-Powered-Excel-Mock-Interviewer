import random
from datetime import datetime
from typing import Dict, Any

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class HybridEvaluator:
    def __init__(self, api_key: str = None):
        """
        Hybrid Evaluator:
        - Rule-based scoring for offline evaluation
        - Gemini AI-based feedback if api_key provided
        """
        self.api_key = api_key
        if self.api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=self.api_key)

    def evaluate_comprehensive(self, question: Dict[str, Any], response: str) -> Dict[str, Any]:
        rule_score = self._rule_based_score(question, response)

        ai_feedback = {}
        ai_score = None
        if self.api_key and GEMINI_AVAILABLE:
            try:
                ai_feedback = self._ai_feedback(question, response)
                ai_score = ai_feedback.get('ai_score', None)
            except Exception:
                ai_feedback = {}
                ai_score = None

        # Blend scores if AI available, else just use rule
        if ai_score is not None:
            final_score = (rule_score * 0.5) + (ai_score * 0.5)  # balanced 50/50
        else:
            final_score = rule_score

        evaluation = {
            'score': round(final_score, 1),
            'overall_feedback': ai_feedback.get('feedback', 'Good attempt, check details.') if ai_feedback else 'Good attempt, check details.',
            'strengths': ai_feedback.get('strengths', []) if ai_feedback else [],
            'improvements': ai_feedback.get('improvements', []) if ai_feedback else [],
            'evaluation_source': 'AI+Rule-based' if ai_feedback else 'Rule-based',
            'timestamp': datetime.now().isoformat()
        }
        return evaluation


    def _rule_based_score(self, question: Dict[str, Any], response: str) -> float:
        """
        Improved scoring:
        - Keyword matching (up to 80 points)
        - Difficulty weighting (up to 20 points)
        """
        keywords = question.get('keywords', [])
        difficulty = question.get('difficulty', 'basic')
        difficulty_weight = {'basic': 0.3, 'intermediate': 0.6, 'advanced': 1.0}

        if not keywords:
            return 50.0 

        matched_keywords = sum(1 for kw in keywords if kw.lower() in response.lower())
        keyword_score = (matched_keywords / len(keywords)) * 80  # keywords dominate

        # Difficulty adds weight for harder Qs
        diff_score = difficulty_weight.get(difficulty, 0.3) * 20

        final_score = keyword_score + diff_score
        return min(final_score, 100)


    def _ai_feedback(self, question: Dict[str, Any], response: str) -> Dict[str, Any]:
        """
        Generate AI feedback using Gemini
        Returns:
            - feedback text
            - strengths list
            - improvements list
            - ai_score (0-100)
        """
        prompt = f"""
        You are an Excel evaluator. Evaluate the following candidate answer to an Excel question.
        Question: {question.get('question')}
        Candidate Answer: {response}

        Provide:
        1. A score from 0 to 100
        2. 3 key strengths
        3. 3 areas of improvement
        4. Overall feedback (brief)

        Output in valid JSON only with keys: ai_score, strengths, improvements, feedback
        """

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response_obj = model.generate_content(prompt)

            text = response_obj.text.strip()

            import json, re
            # Extract JSON safely
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if not json_match:
                return {}

            ai_output = json.loads(json_match.group())

            return {
                'ai_score': min(float(ai_output.get('ai_score', 0)), 100),
                'strengths': ai_output.get('strengths', []),
                'improvements': ai_output.get('improvements', []),
                'feedback': ai_output.get('feedback', '')
            }
        except Exception as e:
            return {}
