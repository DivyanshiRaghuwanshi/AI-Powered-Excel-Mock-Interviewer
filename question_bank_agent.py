import json
import random
from typing import List, Dict, Any
from datetime import datetime

from questions_store import QuestionStorageAgent, load_storage_agent

class QuestionBankAgent:
    def __init__(self):
        self.question_categories = {
            "basic_formulas": ["SUM", "AVERAGE", "COUNT", "MAX", "MIN"],
            "lookup_functions": ["VLOOKUP", "HLOOKUP", "INDEX", "MATCH"],
            "data_analysis": ["PIVOT", "FILTER", "SORT", "SUBTOTAL"],
            "advanced_formulas": ["IF", "SUMIF", "COUNTIF", "NESTED"],
            "data_manipulation": ["CONCATENATE", "TEXT", "DATE", "TIME"],
            "scenario_based": ["DASHBOARD", "REPORTING", "ANALYSIS"]
        }

        self.role_focus = {
            "finance": ["basic_formulas", "lookup_functions", "scenario_based"],
            "operations": ["data_analysis", "data_manipulation", "scenario_based"],
            "data_analytics": ["advanced_formulas", "data_analysis", "lookup_functions"]
        }

        self.initialize_base_questions()

    def initialize_base_questions(self):
        """Create foundational question templates"""
        self.base_questions = [
            {
                "template": "What function would you use to {action} in Excel?",
                "variations": {"action": ["sum values in a range", "find the average", "count non-empty cells"]},
                "category": "basic_formulas",
                "difficulty": "basic"
            },
            {
                "template": "How would you {task} in a large dataset?",
                "variations": {"task": ["remove duplicates", "find unique values", "filter specific criteria"]},
                "category": "data_analysis",
                "difficulty": "intermediate"
            },
            {
                "template": "Explain the difference between {concept1} and {concept2}.",
                "variations": {"concept1": ["VLOOKUP", "absolute references", "SUMIF"],
                               "concept2": ["INDEX-MATCH", "relative references", "SUMIFS"]},
                "category": "advanced_formulas",
                "difficulty": "advanced"
            }
        ]


class QuestionGeneratorAgent:
    def __init__(self, question_bank: QuestionBankAgent):
        self.question_bank = question_bank
        self.used_questions = set()
        self.difficulty_progression = ["basic", "intermediate", "advanced"]

    def generate_interview_questions(self, role: str, count: int = 6) -> List[Dict]:
        """Generate personalized questions for a role with guaranteed count"""
        questions = []
        categories = self.question_bank.role_focus.get(role, ["basic_formulas"])

        # Balanced difficulty allocation
        base_num = count // 3
        remainder = count % 3
        difficulty_distribution = {
            "basic": base_num + (1 if remainder > 0 else 0),
            "intermediate": base_num + (1 if remainder > 1 else 0),
            "advanced": base_num
        }

        for difficulty, num_questions in difficulty_distribution.items():
            for _ in range(num_questions):
                question = self._generate_single_question(categories, difficulty)
                if not question:
                    question = self._fallback_from_storage(categories, difficulty)
                if question and question['id'] not in self.used_questions:
                    questions.append(question)
                    self.used_questions.add(question['id'])

        # Final fallback: fill remaining slots ignoring difficulty/category
        if len(questions) < count:
            needed = count - len(questions)
            storage = QuestionStorageAgent()
            extra = storage.get_questions_by_criteria(role=role, count=needed)
            for q in extra:
                if q['id'] not in self.used_questions:
                    questions.append(q)
                    self.used_questions.add(q['id'])

        # Reset used_questions to allow future interviews to regenerate all
        self.used_questions.clear()

        return questions[:count]

    def _fallback_from_storage(self, categories, difficulty):
        """Pull multiple questions from storage if template fails"""
        storage = load_storage_agent("dynamic_questions.json")
        qs = storage.get_questions_by_criteria(
            category=random.choice(categories),
            difficulty=difficulty,
            count=3  # fetch multiple to avoid shortage
        )
        for q in qs:
            if q['id'] not in self.used_questions:
                return q
        return None

    def _generate_single_question(self, categories: List[str], difficulty: str) -> Dict:
        """Generate a single question based on parameters"""
        if random.choice([True, False]):
            return self._use_template_question(categories, difficulty)
        else:
            return self._get_curated_question(categories, difficulty)

    def _use_template_question(self, categories: List[str], difficulty: str) -> Dict:
        suitable_templates = [
            t for t in self.question_bank.base_questions
            if t['category'] in categories and t['difficulty'] == difficulty
        ]
        if not suitable_templates:
            return None
        template = random.choice(suitable_templates)
        question_text = self._fill_template(template)
        return {
            "id": hash(question_text) % 10000,
            "question": question_text,
            "type": "formula" if "function" in question_text.lower() else "concept",
            "category": template['category'],
            "difficulty": difficulty,
            "keywords": self._extract_keywords(question_text),
            "generated": True,
            "timestamp": datetime.now().isoformat()
        }

    def _fill_template(self, template: Dict) -> str:
        question_text = template['template']
        for key, options in template['variations'].items():
            question_text = question_text.replace(f"{{{key}}}", random.choice(options))
        return question_text

    def _extract_keywords(self, question_text: str) -> List[str]:
        return [word for word in question_text.split() if word.isupper()]

    def _get_curated_question(self, categories: List[str], difficulty: str) -> Dict:
        """Currently not implemented, could fetch curated questions"""
        return None
