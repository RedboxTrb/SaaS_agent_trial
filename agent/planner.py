from typing import List, Dict, Any
import google.generativeai as genai
import os


class TaskPlanner:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    def decompose_task(self, task_description: str, context: Dict = None) -> Dict[str, Any]:
        context_str = ""
        if context:
            context_str = f"\n\nAdditional context:\n{self._format_context(context)}"

        prompt = f"""You are a task planning assistant. Break down the following task into a clear, executable plan.

Task: {task_description}{context_str}

Provide a structured breakdown with:
1. Main goal (one sentence)
2. List of concrete steps (3-8 steps, each actionable)
3. Expected outputs for each step
4. Any dependencies between steps

Format your response as JSON with this structure:
{{
  "goal": "main objective",
  "steps": [
    {{
      "id": 1,
      "action": "what to do",
      "description": "detailed explanation",
      "expected_output": "what this produces",
      "dependencies": []
    }}
  ],
  "success_criteria": "how to know task is complete"
}}"""

        response = self.model.generate_content(prompt)
        response_text = response.text

        import json
        try:
            # sometimes the model wraps response in code blocks, need to extract
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()

            plan = json.loads(json_str)
            return plan
        except json.JSONDecodeError:
            # fallback if parsing fails
            return {
                "goal": task_description,
                "steps": [{"id": 1, "action": "Execute task", "description": response_text,
                          "expected_output": "Task completion", "dependencies": []}],
                "success_criteria": "Task completed"
            }

    def _format_context(self, context: Dict) -> str:
        lines = []
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    def refine_step(self, step: Dict, feedback: str) -> Dict:
        prompt = f"""Refine this task step based on feedback.

Original step:
Action: {step.get('action')}
Description: {step.get('description')}

Feedback: {feedback}

Provide an improved version of this step as JSON:
{{
  "action": "refined action",
  "description": "refined description",
  "expected_output": "what this produces"
}}"""

        response = self.model.generate_content(prompt)
        response_text = response.text

        import json
        try:
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response_text.strip()

            refined = json.loads(json_str)
            return {**step, **refined}
        except:
            return step
