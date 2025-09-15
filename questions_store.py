import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import random

class QuestionStorageAgent:
    def __init__(self, storage_file="dynamic_questions.json"):
        self.storage_file = storage_file
        self.questions = {}
        self.load_questions()   # this calls the fixed method
        
    def _get_questions_list(self):
        """Return the actual list of questions regardless of storage structure"""
        return self.questions.get("questions", []) if isinstance(self.questions, dict) else self.questions     

    def load_questions(self):  
        """Load questions from the storage file if it exists."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.questions = json.load(f)
            except Exception:
                self.questions = {}
        else:
            self.questions = {}
    
    def _initialize_seed_questions(self):
        """Create initial question bank with seed questions"""
        seed_questions = [
            {
                "id": 1,
                "question": "What Excel function would you use to sum values in range A1:A10?",
                "type": "formula",
                "category": "basic_formulas",
                "difficulty": "basic",
                "keywords": ["SUM", "formula", "range"],
                "target_roles": ["finance", "operations", "data_analytics"],
                "usage_count": 0,
                "avg_score": 0.0,
                "success_rate": 0.0,
                "effectiveness_score": 0.5,
                "created_date": datetime.now().isoformat(),
                "performance_history": [],
                "generated": False
            },
            {
                "id": 2,
                "question": "How would you remove duplicate values from a dataset in Excel?",
                "type": "concept",
                "category": "data_manipulation",
                "difficulty": "intermediate",
                "keywords": ["remove duplicates", "data", "filter", "unique"],
                "target_roles": ["data_analytics", "operations"],
                "usage_count": 0,
                "avg_score": 0.0,
                "success_rate": 0.0,
                "effectiveness_score": 0.5,
                "created_date": datetime.now().isoformat(),
                "performance_history": [],
                "generated": False
            },
            {
                "id": 3,
                "question": "Explain the difference between VLOOKUP and INDEX-MATCH functions.",
                "type": "concept",
                "category": "lookup_functions",
                "difficulty": "advanced",
                "keywords": ["VLOOKUP", "INDEX", "MATCH", "lookup"],
                "target_roles": ["finance", "data_analytics"],
                "usage_count": 0,
                "avg_score": 0.0,
                "success_rate": 0.0,
                "effectiveness_score": 0.5,
                "created_date": datetime.now().isoformat(),
                "performance_history": [],
                "generated": False
            },
            {
                "id": 4,
                "question": "How would you create a pivot table to analyze sales data by region and product?",
                "type": "concept",
                "category": "data_analysis",
                "difficulty": "intermediate",
                "keywords": ["pivot table", "sales data", "analysis", "region"],
                "target_roles": ["finance", "operations", "data_analytics"],
                "usage_count": 0,
                "avg_score": 0.0,
                "success_rate": 0.0,
                "effectiveness_score": 0.5,
                "created_date": datetime.now().isoformat(),
                "performance_history": [],
                "generated": False
            },
            {
                "id": 5,
                "question": "What's the difference between absolute and relative cell references? Give examples.",
                "type": "concept",
                "category": "basic_formulas",
                "difficulty": "basic",
                "keywords": ["absolute", "relative", "cell reference", "$"],
                "target_roles": ["finance", "operations", "data_analytics"],
                "usage_count": 0,
                "avg_score": 0.0,
                "success_rate": 0.0,
                "effectiveness_score": 0.5,
                "created_date": datetime.now().isoformat(),
                "performance_history": [],
                "generated": False
            },
            {
                "id": 6,
                "question": "How would you use SUMIF to calculate total sales for a specific product?",
                "type": "formula",
                "category": "advanced_formulas",
                "difficulty": "intermediate",
                "keywords": ["SUMIF", "conditional", "criteria", "sales"],
                "target_roles": ["finance", "operations"],
                "usage_count": 0,
                "avg_score": 0.0,
                "success_rate": 0.0,
                "effectiveness_score": 0.5,
                "created_date": datetime.now().isoformat(),
                "performance_history": [],
                "generated": False
            }
        ]
        self.questions = seed_questions
    
    def store_question(self, question: Dict, performance_data: Dict = None):
        """Store new question with performance metadata"""
        # Generate unique ID if not provided
        if 'id' not in question:
            question['id'] = self._generate_question_id()
        
        question_entry = {
            **question,
            "usage_count": 0,
            "avg_score": 0.0,
            "success_rate": 0.0,
            "effectiveness_score": 0.5,
            "created_date": datetime.now().isoformat(),
            "performance_history": []
        }
        
        if performance_data:
            question_entry.update(performance_data)
        
        self._get_questions_list().append(question_entry)
        self.save_questions()
        return question_entry['id']
    
    def update_question_performance(self, question_id: int, score: int, outcome: str = None):
        """Update question performance based on candidate results"""
        # Make sure we are iterating the actual list of questions
        
        questions_list = self._get_questions_list()
        for question in questions_list:
            if question['id'] == question_id:
                # Update usage statistics
                question['usage_count'] = question.get('usage_count', 0) + 1
                old_avg = question.get('avg_score', 0)
                count = question['usage_count']
                question['avg_score'] = ((old_avg * (count - 1)) + score) / count

                # Update success rate if outcome provided
                if outcome == "hired":
                    old_success = question.get('success_rate', 0)
                    question['success_rate'] = ((old_success * (count - 1)) + 1) / count
                elif outcome == "not_hired":
                    old_success = question.get('success_rate', 0)
                    question['success_rate'] = (old_success * (count - 1)) / count

                # Track performance history
                history = question.get('performance_history', [])
                history.append({
                    'score': score,
                    'timestamp': datetime.now().isoformat(),
                    'outcome': outcome
                })
                question['performance_history'] = history

                # Calculate effectiveness score
                question['effectiveness_score'] = self._calculate_effectiveness(question)
                break

        self.save_questions()

    
    def _calculate_effectiveness(self, question: Dict) -> float:
        """Calculate how effective a question is at predicting performance"""
        if question['usage_count'] < 3:
            return 0.5  # Default for new questions
        
        # Factors for effectiveness calculation
        score_variance = abs(question['avg_score'] - 70) / 30  # How well it discriminates
        usage_factor = min(question['usage_count'] / 50, 1.0)  # More usage = more reliable
        success_correlation = question.get('success_rate', 0.5)  # Hiring correlation
        
        # Weighted effectiveness score
        effectiveness = (
            score_variance * 0.4 +  # Discrimination ability
            usage_factor * 0.3 +    # Reliability through usage
            success_correlation * 0.3  # Predictive power
        )
        
        return min(max(effectiveness, 0.0), 1.0)  # Clamp between 0 and 1
    

    def get_questions_by_criteria(self, 
                                category: str = None, 
                                difficulty: str = None, 
                                role: str = None,
                                min_effectiveness: float = 0.0,
                                count: int = None) -> List[Dict]:
        """Retrieve questions based on specific criteria with fallback if not enough"""
        filtered_questions = self._get_questions_list().copy()
        
        if category:
            filtered_questions = [q for q in filtered_questions if q.get('category') == category]
        if difficulty:
            filtered_questions = [q for q in filtered_questions if q.get('difficulty') == difficulty]
        if role:
            filtered_questions = [q for q in filtered_questions if role in q.get('target_roles', [])]
        if min_effectiveness > 0:
            filtered_questions = [q for q in filtered_questions if q.get('effectiveness_score', 0) >= min_effectiveness]

        # Sort by effectiveness descending
        filtered_questions.sort(key=lambda x: x.get('effectiveness_score', 0), reverse=True)
        
        # Fallback: return as many as possible even if less than count
        if count:
            return filtered_questions[:count]
        return filtered_questions

    
    def get_best_questions(self, role: str, count: int = 6) -> List[Dict]:
        """Get the most effective questions for a specific role"""
        role_questions = [q for q in self._get_questions_list() if role in q.get('target_roles', [])]
        # Ensure we have questions across different difficulties
        difficulties = ['basic', 'intermediate', 'advanced']
        selected_questions = []
        
        for difficulty in difficulties:
            difficulty_questions = [q for q in role_questions if q.get('difficulty') == difficulty]
            difficulty_questions.sort(key=lambda x: x.get('effectiveness_score', 0), reverse=True)
            
            # Take top 2 from each difficulty level
            selected_questions.extend(difficulty_questions[:2])
        
        # If we need more questions, fill with remaining best questions
        if len(selected_questions) < count:
            remaining_questions = [q for q in role_questions if q not in selected_questions]
            remaining_questions.sort(key=lambda x: x.get('effectiveness_score', 0), reverse=True)
            selected_questions.extend(remaining_questions[:count - len(selected_questions)])
        
        return selected_questions[:count]
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """Retrieve a specific question by ID"""
        for question in self._get_questions_list():
            if question['id'] == question_id:
                return question
        return None
    
    def delete_question(self, question_id: int) -> bool:
        """Delete a question from storage"""
        questions_list = self._get_questions_list()
        for i, question in enumerate(questions_list):
            if question['id'] == question_id:
                del questions_list[i]
                self.save_questions()
                return True
        return False
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics about the question bank"""
        questions_list = self._get_questions_list()
        if not questions_list:
            return {"error": "No questions in database"}
        
        total_questions = len(questions_list)
        total_usage = sum(q.get('usage_count', 0) for q in questions_list)
        avg_effectiveness = sum(q.get('effectiveness_score', 0) for q in questions_list) / total_questions

        # Category distribution
        categories = {}
        for question in questions_list:
            cat = question.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        # Difficulty distribution
        difficulties = {}
        for question in questions_list:
            diff = question.get('difficulty', 'unknown')
            difficulties[diff] = difficulties.get(diff, 0) + 1

        # Top performing questions
        top_questions = sorted(questions_list, key=lambda x: x.get('effectiveness_score', 0), reverse=True)[:5]

        return {
            'total_questions': total_questions,
            'total_usage': total_usage,
            'average_effectiveness': round(avg_effectiveness, 3),
            'category_distribution': categories,
            'difficulty_distribution': difficulties,
            'top_questions': [
                {
                    'id': q['id'],
                    'question': q['question'][:50] + '...',
                    'effectiveness': q.get('effectiveness_score', 0)
                }
                for q in top_questions
            ],
            'last_updated': getattr(self, "metadata", {}).get("last_updated")
        }

            
            
    def save_questions(self):
        """Save all questions to storage file."""
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.questions, f, indent=4, ensure_ascii=False)           
        
    
    def _generate_question_id(self) -> int:
        """Generate unique question ID"""
        existing_ids = [q['id'] for q in self._get_questions_list()]
        new_id = max(existing_ids, default=0) + 1
        return new_id
    
    def backup_questions(self, backup_file: str = None):
        """Create backup of questions database"""
        if not backup_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"questions_backup_{timestamp}.json"
        
        try:
            with open(backup_file, 'w') as f:
                json.dump({
                    'questions': self.questions,
                    'metadata': self.metadata
                }, f, indent=2)
            return backup_file
        except IOError as e:
            print(f"Error creating backup: {e}")
            return None

# Utility functions for external use
def load_storage_agent(storage_file: str = "dynamic_questions.json") -> QuestionStorageAgent:
    """Factory function to create and return storage agent"""
    return QuestionStorageAgent(storage_file)

def get_question_stats(storage_file: str = "dynamic_questions.json") -> Dict:
    """Quick function to get question bank statistics"""
    agent = QuestionStorageAgent(storage_file)
    return agent.get_analytics()