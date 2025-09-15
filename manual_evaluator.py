#!/usr/bin/env python3
"""
Test script to verify the HybridEvaluator works (Gemini or rule-based fallback)
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_evaluator():
    """Test that evaluator works with or without API key"""
    try:
        from answer_evaluator import HybridEvaluator
        
        print("Testing HybridEvaluator without API key (rule-based fallback)...")
        evaluator = HybridEvaluator(api_key=None)
        print("Evaluator created successfully")

        # Example test question
        test_question = {
            "id": 1,
            "question": "What Excel function would you use to sum values in range A1:A10?",
            "type": "formula",
            "keywords": ["SUM", "formula", "range"],
            "difficulty": "basic"
        }

        # Example candidate response
        test_response = "I would use the SUM function in Excel. The formula would be =SUM(A1:A10) to add all values in that range."

        print("Testing evaluation...")
        result = evaluator.evaluate_comprehensive(test_question, test_response)

        print(f"Evaluation successful!")
        print(f"Score: {result['score']}/100")
        print(f"Source: {result['evaluation_source']}")
        print(f"Feedback: {result['overall_feedback']}")
        print(f"Strengths: {result['strengths']}")
        print(f"Improvements: {result['improvements']}")

        return True

    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_evaluator()
    sys.exit(0 if success else 1)
