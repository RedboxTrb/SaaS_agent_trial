import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class DecisionTracer:
    def __init__(self, storage_dir="storage"):
        self.storage_dir = storage_dir
        self.trace_file = os.path.join(storage_dir, "decision_trace.json")
        self.current_trace = []
        self.load_trace()

    def load_trace(self):
        if os.path.exists(self.trace_file):
            with open(self.trace_file, 'r') as f:
                data = json.load(f)
                self.current_trace = data.get("trace", [])

    def save_trace(self):
        with open(self.trace_file, 'w') as f:
            json.dump({"trace": self.current_trace}, f, indent=2)

    def log_decision(self, step: str, action: str, reasoning: str,
                     inputs: Optional[Dict] = None, outputs: Optional[Dict] = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "action": action,
            "reasoning": reasoning,
            "inputs": inputs or {},
            "outputs": outputs or {}
        }
        self.current_trace.append(entry)
        self.save_trace()
        return entry

    def get_trace(self) -> List[Dict]:
        return self.current_trace

    def get_recent_decisions(self, n: int = 5) -> List[Dict]:
        return self.current_trace[-n:] if len(self.current_trace) >= n else self.current_trace

    def explain_decision_path(self) -> str:
        if not self.current_trace:
            return "No decisions recorded yet."

        explanation = "Decision Path:\n"
        explanation += "=" * 50 + "\n\n"

        for i, entry in enumerate(self.current_trace, 1):
            explanation += f"Step {i}: {entry['step']}\n"
            explanation += f"  Action: {entry['action']}\n"
            explanation += f"  Reasoning: {entry['reasoning']}\n"
            if entry.get('inputs'):
                explanation += f"  Inputs: {json.dumps(entry['inputs'], indent=4)}\n"
            if entry.get('outputs'):
                explanation += f"  Outputs: {json.dumps(entry['outputs'], indent=4)}\n"
            explanation += "\n"

        return explanation

    def clear_trace(self):
        self.current_trace = []
        self.save_trace()

    def export_trace(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump({
                "exported_at": datetime.now().isoformat(),
                "trace": self.current_trace
            }, f, indent=2)
