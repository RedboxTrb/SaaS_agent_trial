import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class StateManager:
    # handles both current session state and long term memory
    def __init__(self, storage_dir="storage"):
        self.storage_dir = storage_dir
        self.state_file = os.path.join(storage_dir, "agent_state.json")
        self.memory_file = os.path.join(storage_dir, "long_term_memory.json")

        # make sure storage directory exists
        os.makedirs(storage_dir, exist_ok=True)

        self.current_state = self._load_state()
        self.long_term = self._load_memory()

    def _load_state(self) -> Dict:
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {
            "current_task": None,
            "plan": [],
            "completed_steps": [],
            "pending_steps": [],
            "context": {},
            "session_id": None
        }

    def _load_memory(self) -> Dict:
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {
            "past_tasks": [],
            "learned_patterns": {},
            "user_preferences": {},
            "decisions": []
        }

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.current_state, f, indent=2)

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.long_term, f, indent=2)

    def update_state(self, key: str, value: Any):
        self.current_state[key] = value
        self.save_state()

    def get_state(self, key: str) -> Any:
        return self.current_state.get(key)

    def record_decision(self, decision: str, reasoning: str, context: Dict):
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "reasoning": reasoning,
            "context": context
        }
        self.long_term["decisions"].append(decision_record)
        self.save_memory()
        return decision_record

    def store_user_preference(self, key: str, value: Any):
        self.long_term["user_preferences"][key] = value
        self.save_memory()

    def get_user_preference(self, key: str) -> Optional[Any]:
        return self.long_term["user_preferences"].get(key)

    def add_completed_task(self, task_info: Dict):
        task_record = {
            **task_info,
            "completed_at": datetime.now().isoformat()
        }
        self.long_term["past_tasks"].append(task_record)
        self.save_memory()

    def get_relevant_past_tasks(self, task_type: str) -> List[Dict]:
        return [t for t in self.long_term["past_tasks"]
                if t.get("type") == task_type]

    def clear_session(self):
        self.current_state = {
            "current_task": None,
            "plan": [],
            "completed_steps": [],
            "pending_steps": [],
            "context": {},
            "session_id": None
        }
        self.save_state()
