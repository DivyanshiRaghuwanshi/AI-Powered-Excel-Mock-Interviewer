from typing import List, Dict, Any
from answer_evaluator import HybridEvaluator
from questions_store import QuestionStorageAgent
from datetime import datetime

class FeedbackGenerator:
    def __init__(self, api_key: str = None, storage_file: str = "dynamic_questions.json"):
        self.evaluator = HybridEvaluator(api_key=api_key)
        self.storage = QuestionStorageAgent(storage_file)

    def generate_feedback_and_score(self, question: Dict, candidate_response: str) -> Dict[str, Any]:
        """
        Generate feedback and score for a single question-response pair
        """
        result = self.evaluator.evaluate_comprehensive(question, candidate_response)

        # --- Override scoring with keyword-based check ---
        keywords = [kw.lower() for kw in question.get("keywords", [])]
        answer_lower = candidate_response.lower()
        matches = sum(1 for kw in keywords if kw in answer_lower)

        if keywords:
            ratio = matches / len(keywords)
            if ratio == 0:
                result['score'] = 20
            elif ratio < 0.5:
                result['score'] = 50
            elif ratio < 1:
                result['score'] = 75
            else:
                result['score'] = 100
            result['evaluation_source'] = "keyword_based"

        # Update question performance in storage
        self.storage.update_question_performance(
            question_id=question['id'],
            score=result.get('score', 0),
            outcome=result.get('outcome')
        )

        feedback_data = {
            "question_id": question['id'],
            "question": question['question'],
            "candidate_response": candidate_response,
            "score": result.get('score', 0),
            "overall_feedback": result.get('overall_feedback', ''),
            "evaluation_source": result.get('evaluation_source', ''),
            "timestamp": datetime.now().isoformat()
        }

        return feedback_data


    def generate_bulk_feedback(self, qa_pairs: List[Dict]) -> List[Dict[str, Any]]:
        """
        Generate feedback for multiple question-response pairs
        qa_pairs: List of dicts with 'question' and 'response' keys
        """
        feedback_list = []
        for pair in qa_pairs:
            feedback = self.generate_feedback_and_score(pair['question'], pair['response'])
            feedback_list.append(feedback)
        return feedback_list
