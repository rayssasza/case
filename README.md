Smart AI Assistant (Technical Case)

Author: Rayssa

Context: AI Engineer Technical Challenge - Artefact

- Overview

This project implements a Smart AI Assistant capable of distinguishing between general knowledge queries and exact mathematical problems.

Instead of relying on high-level abstractions like LangChain or AutoGPT, I chose a First Principles approach. I manually implemented the "Router" logic (Intent Classification) and the tool execution flow. This demonstrates a clear understanding of how Agentic Workflows operate under the hood: Thought -> Plan -> Action.

Key Features

Explicit Routing: Uses the LLM as a zero-shot classifier to decide the intent (MATH vs GENERAL).

Deterministic Tools: Offloads math to a Python-based calculator to avoid LLM hallucinations on arithmetic.

Clean Architecture: Separation of concerns between the LLM Client, the Tools, and the Agent Orchestrator.

- Logic & Architecture

My background in Internet Systems and my ongoing research for ProfIAs (my thesis on Generative AI) have taught me that transparency is key in AI systems.

I structured the solution into three distinct layers:

The LLM Layer (MockLLMService):

A wrapper meant to communicate with APIs like OpenAI or Anthropic.

Decision: I mocked this for the challenge to ensure the code is immediately runnable without requiring you to set up an .env file or API keys, but the structure is ready for a drop-in replacement of openai.chat.completions.

The Tool Layer (CalculatorTool):

A safe execution environment for math.

Safety: I implemented regex sanitization to prevent code injection, adhering to security best practices.

The Orchestration Layer (SmartAssistant):

This is the "Brain". It receives the input, classifies the intent, and routes the request.

Why manual routing? Explicit if/else control flow based on intent is often more reliable and cheaper/faster in production than letting a model "hallucinate" a tool call loop autonomously for simple tasks.

- How to Run

- Prerequisites

Python 3.8+

Execution

Since the implementation uses standard libraries and a mocked LLM service for demonstration, no pip install is strictly necessary.

Clone the repository or download agent.py.

Run the script directly:

python agent.py


- Expected Output

You will see the logs demonstrating the decision-making process:

--- Processing Query: 'Quem foi Albert Einstein?' ---
[Log] Intent Identified: GENERAL
[Log] Routing to LLM Semantic Core (Probabilistic)...
Final Answer: Based on my internal knowledge base...

--- Processing Query: 'Quanto é 128 vezes 46?' ---
[Log] Intent Identified: MATH
[Log] Routing to CalculatorTool (Deterministic)...
Final Answer: Calculated Result: 5888


- Learnings & Future Improvements

What I Learned

Prompt Engineering for Routing: Getting an LLM to output a strict single-word classification ("MATH") requires precise system prompting to avoid chatty responses.

Trade-offs: Building from scratch gives total control but requires writing more boilerplate code compared to using LangChain's initialize_agent.

What I Would Do Differently (With More Time)

Real API Integration: Connect to gpt-3.5-turbo using the openai library and python-dotenv for key management.

Abstract Syntax Tree (AST): For the calculator, I would implement a full AST parser instead of eval() for production-grade security.

Conversation History: Implement a Memory class to allow follow-up questions (e.g., "And multiply that result by 2").

Thanks!
