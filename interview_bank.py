from question_bank_agent import QuestionBankAgent, QuestionGeneratorAgent
from questions_store import QuestionStorageAgent
from answer_evaluator import HybridEvaluator
from typing import List, Dict
from datetime import datetime

class InterviewAgent:
    def __init__(self, role: str, storage_file: str = "dynamic_questions.json", api_key: str = None):
        # Initialize the question bank and generator
        self.question_bank = QuestionBankAgent()
        self.generator = QuestionGeneratorAgent(self.question_bank)
        
        # Storage agent to track questions and performance
        self.storage_agent = QuestionStorageAgent(storage_file)
        
        # Evaluator for AI-based evaluation
        self.evaluator = HybridEvaluator(api_key=api_key)
        
        self.role = role
        self.current_session = []
    
    def generate_interview(self, num_questions: int = 6) -> List[Dict]:
        """Generate a new interview session for the role"""
        questions = self.generator.generate_interview_questions(self.role, num_questions)
        
        # Store generated questions in storage if not already present
        for q in questions:
            if not self.storage_agent.get_question_by_id(q['id']):
                q['target_roles'] = [self.role]
                self.storage_agent.store_question(q)
        
        self.current_session = questions
        return questions
    
    def evaluate_response(self, question_id: int, candidate_response: str) -> Dict:
        """Evaluate a single candidate response"""
        question = self.storage_agent.get_question_by_id(question_id)
        if not question:
            raise ValueError(f"Question ID {question_id} not found.")
        
        # AI evaluation
        eval_result = self.evaluator.evaluate_comprehensive(question, candidate_response)
        
        # Update question performance
        self.storage_agent.update_question_performance(
            question_id,
            score=eval_result['score'],
            outcome=eval_result.get('outcome')
        )
        
        return eval_result
    
    def evaluate_session(self, responses: Dict[int, str]) -> List[Dict]:
        """Evaluate multiple responses in one session"""
        results = []
        for qid, response in responses.items():
            result = self.evaluate_response(qid, response)
            results.append(result)
        return results
    
    def get_session_summary(self) -> Dict:
        """Summarize current session questions and stats"""
        summary = {
            "role": self.role,
            "num_questions": len(self.current_session),
            "questions": [
                {"id": q['id'], "question": q['question'], "difficulty": q['difficulty']}
                for q in self.current_session
            ],
            "generated_at": datetime.now().isoformat()
        }
        return summary
