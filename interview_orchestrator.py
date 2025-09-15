import random
from datetime import datetime
from typing import Dict, List

from question_bank_agent import QuestionBankAgent, QuestionGeneratorAgent
from questions_store import QuestionStorageAgent
from answer_evaluator import HybridEvaluator

class InterviewOrchestrator:
    def __init__(self, role: str, api_key: str = None):
        # Role for interview (finance, operations, data_analytics)
        self.role = role
        
        # Initialize components
        self.question_bank = QuestionBankAgent()
        self.generator = QuestionGeneratorAgent(self.question_bank)
        self.storage = QuestionStorageAgent()
        self.evaluator = HybridEvaluator(api_key=api_key)
    
    def conduct_interview(self, num_questions: int = 6) -> Dict:
        """Generate questions, evaluate responses, store performance"""
        
        questions = self.generator.generate_interview_questions(self.role, count=num_questions)
        
        interview_results = []
        
        for question in questions:
            print(f"\nQuestion: {question['question']}")
            
            # Here you can integrate actual candidate response input
            candidate_response = input("Your Answer: ")
            
            # Evaluate candidate answer
            evaluation = self.evaluator.evaluate_comprehensive(question, candidate_response)
            
            # Store or update question in storage
            stored_id = self.storage.store_question(question)
            self.storage.update_question_performance(
                question_id=stored_id,
                score=evaluation['score'],
                outcome=evaluation.get('outcome', None)
            )
            
            interview_results.append({
                "question": question['question'],
                "response": candidate_response,
                "evaluation": evaluation
            })
        
        return {
            "role": self.role,
            "timestamp": datetime.now().isoformat(),
            "results": interview_results
        }
    
    def get_best_questions_for_role(self, count: int = 6) -> List[Dict]:
        """Fetch best questions for this role based on effectiveness"""
        return self.storage.get_best_questions(self.role, count=count)

if __name__ == "__main__":
    print("=== Interview Orchestrator ===")
    role = input("Enter candidate role (finance/operations/data_analytics): ").strip()
    
   
    orchestrator = InterviewOrchestrator(role=role, api_key=None)
    
    results = orchestrator.conduct_interview(num_questions=6)
    
    print("\n=== Interview Completed ===")
    for r in results['results']:
        print(f"\nQ: {r['question']}")
        print(f"A: {r['response']}")
        print(f"Score: {r['evaluation']['score']}/100")
        print(f"Feedback: {r['evaluation']['overall_feedback']}")
