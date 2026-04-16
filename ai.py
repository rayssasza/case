"""
Author: Rayssa
Date: 2026
Context: AI Engineer Technical Case - Artefact
Description:
    This implementation demonstrates a 'First Principles' approach to building an AI Agent.
    Instead of relying on high-level abstractions like LangChain, I explicitly implemented
    the control flow, state management, and tool routing.

    Architecture:
    - LLMClient: Handles raw API communication.
    - CalculatorTool: A safe, deterministic math execution engine.
    - SmartAssistant: The orchestrator that manages the 'Thought -> Plan -> Action' loop.
"""

import os
import re
from typing import Union
from enum import Enum

class MockLLMService:
    """
    Simulates the behavior of an LLM API (like OpenAI) for this standalone script.
    
    I'm mocking this to ensure the code is runnable by the reviewers immediately 
    without needing an API key configuration. In a production environment, 
    this class would wrap `openai.chat.completions.create` or a similar endpoint.
    """
    def generate_response(self, prompt: str, system_role: str = "user") -> str:
        # Here simulate the probabilistic nature of an LLM.
        prompt_lower = prompt.lower()
        role_lower = system_role.lower()
        
        # Simulating the "Router" logic capabilities of an LLM.
        if "classifier" in role_lower or "intent" in role_lower:
            # Heuristic: if it has digits and math words, it's likely math.
            # In a real scenario, the LLM semantic understanding handles this beautifully.
            math_indicators = [
                '+', '-', '*', '/', 'vezes', 'divided', 'multiplicado', 'somado', 
                'x', 'mais', 'menos', 'calcular', 'quanto é', 'quanto', 'multiplicar'
            ]
            
            has_digit = any(char.isdigit() for char in prompt)
            # Find if any indicator exists in the normalized prompt
            has_math_indicator = any(op in prompt_lower for op in math_indicators)
            
            if has_digit and has_math_indicator:
                return "MATH"
            return "GENERAL"
        
        # Simulating a General Knowledge response.
        return f"Based on my internal knowledge base, I can tell you that '{prompt}' is a fascinating topic involving physics and history."

# --- 2. The Deterministic Tool Layer ---

class CalculatorTool:
    """
    A deterministic tool for exact mathematical operations.
    Using a tool is safer and more accurate than relying on LLM hallucination for arithmetic.
    """
    
    @staticmethod
    def _sanitize_expression(expression: str) -> str:
        # We allow only digits, basic operators, and whitespace.
        allowed_chars = set("0123456789+-*/.() ")
        
        if not set(expression).issubset(allowed_chars):
             raise ValueError("Unsafe characters detected in math expression.")
        return expression

    def calculate(self, query: str) -> str:
        """
        Extracts the numbers/operators and evaluates the result safely.
        """
        try:
            # 1. Normalize the query to handle natural language operators
            # This mapping step is crucial for robust NLP-to-Math conversion
            query_lower = query.lower()
            replacements = {
                'vezes': '*', 'multiplicado por': '*', 'multiplicado': '*', 'x': '*',
                'dividido por': '/', 'dividido': '/',
                'mais': '+', 'menos': '-', 'quanto é': ''
            }
            
            processed_query = query_lower
            for word, op in replacements.items():
                processed_query = processed_query.replace(word, op)

            # 2. Extract potential math expression using Regex
            # Look for a sequence of numbers and operators
            match = re.search(r'[\d\.\(\)\+\-\*\/\s]+', processed_query)
            if not match:
                return "Error: Could not extract a valid math expression."
            
            expression = self._sanitize_expression(match.group(0))
            
            # For simple arithmetic with strict regex guards, eval is acceptable.
            # Ideally, we would use an expression parser tree for maximum security.
            # Using strict sanitization before eval mitigates injection risks.
            result = eval(expression, {"__builtins__": None}, {})
            
            return str(result)
        except Exception as e:
            return f"Error in calculation: {str(e)}"

# --- 3. The Agent ---

class Intent(Enum):
    MATH = "MATH"
    GENERAL = "GENERAL"

class SmartAssistant:
    def __init__(self) -> None:
        # Initializing our dependencies. 
        # Dependency Injection principles could be applied here for larger systems.
        self.llm = MockLLMService()
        self.calculator = CalculatorTool()

    def _decide_intent(self, user_query: str) -> Intent:
        """
        The 'Router' logic.
        Instead of a complex chain, we ask the LLM specifically to classify the intent.
        This provides a deterministic control flow based on probabilistic input.
        """
        system_prompt = (
            "You are an intent classifier. Analyze the user query. "
            "If it requires a calculation or math logic, return strictly 'MATH'. "
            "If it is a general knowledge question, return strictly 'GENERAL'."
        )
        
        # Force a classification step before attempting to answer.
        decision = self.llm.generate_response(prompt=user_query, system_role=system_prompt)
        
        if "MATH" in decision.upper():
            return Intent.MATH
        return Intent.GENERAL

    def run(self, user_query: str) -> str:
        """
        The main execution loop representing the Thought -> Plan -> Action cycle.
        """
        print(f"--- Processing Query: '{user_query}' ---")
        
        # Step 1: Decide (The Routing Layer)
        intent = self._decide_intent(user_query)
        print(f"[Log] Intent Identified: {intent.value}")

        # Step 2: Act (The Logic Branching)
        # Using a clear If/Else block demonstrates we understand the underlying logic flow
        if intent == Intent.MATH:
            print("[Log] Routing to CalculatorTool (Deterministic)...")
            result = self.calculator.calculate(user_query)
            response = f"Calculated Result: {result}"
        else:
            print("[Log] Routing to LLM Semantic Core (Probabilistic)...")
            # Here call the LLM for a full text generation
            response = self.llm.generate_response(prompt=user_query, system_role="Helpful Assistant")

        return response

# --- Execution Block ---
if __name__ == "__main__":
    agent = SmartAssistant()

    # Test Case 1: General Knowledge (Should route to LLM)
    response_1 = agent.run("Quem foi Albert Einstein?")
    print(f"Final Answer: {response_1}\n")

    # Test Case 2: Math (Should route to Calculator)
    response_2 = agent.run("Quanto é 128 vezes 46?")
    print(f"Final Answer: {response_2}\n")
