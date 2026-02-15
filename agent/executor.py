import os
import json
from typing import Dict, Any, Callable
from datetime import datetime
import google.generativeai as genai


class ActionExecutor:
    def __init__(self, api_key: str = None, output_dir: str = "outputs"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.action_handlers = {
            "create_document": self._create_document,
            "analyze_data": self._analyze_data,
            "generate_content": self._generate_content,
            "research": self._research,
            "calculate_metrics": self._calculate_metrics
        }

    def execute_step(self, step: Dict, context: Dict = None) -> Dict[str, Any]:
        action = step.get("action", "").lower()
        description = step.get("description", "")

        # figure out what kind of action this is
        action_type = self._determine_action_type(action, description)

        # run the appropriate handler
        if action_type in self.action_handlers:
            result = self.action_handlers[action_type](step, context or {})
        else:
            result = self._generic_execute(step, context or {})

        return {
            "step_id": step.get("id"),
            "action": action,
            "status": "completed",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }

    def _determine_action_type(self, action: str, description: str) -> str:
        text = (action + " " + description).lower()

        if any(word in text for word in ["create", "write", "draft", "document"]):
            return "create_document"
        elif any(word in text for word in ["analyze", "evaluate", "assess"]):
            return "analyze_data"
        elif any(word in text for word in ["generate", "produce", "develop"]):
            return "generate_content"
        elif any(word in text for word in ["research", "investigate", "explore"]):
            return "research"
        elif any(word in text for word in ["calculate", "metric", "measure"]):
            return "calculate_metrics"
        else:
            return "generic"

    def _create_document(self, step: Dict, context: Dict) -> Dict:
        prompt = f"""Create a professional document based on this requirement:

Task: {step.get('action')}
Details: {step.get('description')}

Context: {json.dumps(context, indent=2)}

Generate a well-structured document with appropriate sections and content."""

        response = self.model.generate_content(prompt)
        content = response.text

        filename = f"document_{step.get('id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "type": "document",
            "filepath": filepath,
            "content_preview": content[:200] + "..." if len(content) > 200 else content
        }

    def _analyze_data(self, step: Dict, context: Dict) -> Dict:
        prompt = f"""Perform analysis based on this requirement:

Task: {step.get('action')}
Details: {step.get('description')}

Data context: {json.dumps(context, indent=2)}

Provide structured analysis with key findings, insights, and recommendations."""

        response = self.model.generate_content(prompt)
        analysis = response.text

        return {
            "type": "analysis",
            "findings": analysis,
            "summary": analysis[:300] + "..." if len(analysis) > 300 else analysis
        }

    def _generate_content(self, step: Dict, context: Dict) -> Dict:
        prompt = f"""Generate content for:

Task: {step.get('action')}
Requirements: {step.get('description')}

Context: {json.dumps(context, indent=2)}

Create high-quality, relevant content that meets the requirements."""

        response = self.model.generate_content(prompt)
        content = response.text

        filename = f"generated_{step.get('id', 'content')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "type": "generated_content",
            "filepath": filepath,
            "preview": content[:250] + "..." if len(content) > 250 else content
        }

    def _research(self, step: Dict, context: Dict) -> Dict:
        prompt = f"""Research and compile information on:

Topic: {step.get('action')}
Focus: {step.get('description')}

Context: {json.dumps(context, indent=2)}

Provide comprehensive research findings with sources and key points."""

        response = self.model.generate_content(prompt)
        research_output = response.text

        return {
            "type": "research",
            "findings": research_output
        }

    def _calculate_metrics(self, step: Dict, context: Dict) -> Dict:
        data = context.get("user_data", {})

        prompt = f"""Calculate relevant metrics based on:

Task: {step.get('action')}
Details: {step.get('description')}

Available data: {json.dumps(data, indent=2)}

Provide calculated metrics with formulas and interpretations."""

        response = self.model.generate_content(prompt)
        metrics_output = response.text

        return {
            "type": "metrics",
            "calculations": metrics_output,
            "data_used": data
        }

    def _generic_execute(self, step: Dict, context: Dict) -> Dict:
        prompt = f"""Execute this task step:

Action: {step.get('action')}
Description: {step.get('description')}

Context: {json.dumps(context, indent=2)}

Provide a detailed execution result."""

        response = self.model.generate_content(prompt)
        result = response.text

        return {
            "type": "generic",
            "output": result
        }
