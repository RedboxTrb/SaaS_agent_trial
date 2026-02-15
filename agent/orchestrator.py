from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from agent.planner import TaskPlanner
from agent.executor import ActionExecutor
from agent.memory import StateManager
from agent.tracer import DecisionTracer


class StatefulAgent:
    def __init__(self, api_key: str = None):
        self.planner = TaskPlanner(api_key=api_key)
        self.executor = ActionExecutor(api_key=api_key)
        self.memory = StateManager()
        self.tracer = DecisionTracer()

        self.session_id = str(uuid.uuid4())
        self.memory.update_state("session_id", self.session_id)

    def run_task(self, task_description: str, context: Dict = None) -> Dict[str, Any]:
        print(f"\nSTARTING NEW TASK")
        print(f"Task: {task_description}\n")

        self.memory.update_state("current_task", task_description)
        self.memory.update_state("context", context or {})

        self.tracer.log_decision(
            step="Task Initiation",
            action="Received task request",
            reasoning="User provided a new task to execute",
            inputs={"task": task_description, "context": context}
        )

        print("PHASE 1: PLANNING")
        plan = self._plan_task(task_description, context)

        print("\n\nPHASE 2: EXECUTION")
        results = self._execute_plan(plan, context)

        print("\n\nPHASE 3: COMPLETION")
        summary = self._finalize_task(task_description, plan, results)

        return summary

    def _plan_task(self, task_description: str, context: Dict = None) -> Dict:
        relevant_past = self.memory.get_relevant_past_tasks(
            context.get("task_type", "general") if context else "general"
        )

        past_context = {}
        if relevant_past:
            past_context["previous_similar_tasks"] = len(relevant_past)
            past_context["learned_from_past"] = "Agent has experience with similar tasks"

        full_context = {**(context or {}), **past_context}

        print("Analyzing task and creating execution plan...")

        plan = self.planner.decompose_task(task_description, full_context)

        self.tracer.log_decision(
            step="Planning",
            action="Task decomposition",
            reasoning="Breaking down complex task into manageable steps for systematic execution",
            inputs={"task": task_description, "context": full_context},
            outputs={"plan": plan}
        )

        self.memory.update_state("plan", plan)
        self.memory.update_state("pending_steps", plan.get("steps", []))

        print(f"\nGoal: {plan.get('goal', 'N/A')}")
        print(f"\nPlanned {len(plan.get('steps', []))} steps:")
        for step in plan.get("steps", []):
            print(f"  {step['id']}. {step['action']}")

        decision = f"Created execution plan with {len(plan.get('steps', []))} steps"
        reasoning = "Task decomposition allows for systematic execution and progress tracking"
        self.memory.record_decision(decision, reasoning, {"plan": plan})

        return plan

    def _execute_plan(self, plan: Dict, context: Dict = None) -> List[Dict]:
        steps = plan.get("steps", [])
        results = []
        completed = []

        print(f"\nExecuting {len(steps)} planned steps...\n")

        for i, step in enumerate(steps, 1):
            print(f"\nStep {i}/{len(steps)}: {step['action']}")
            print(f"Description: {step['description']}")

            dependencies = step.get("dependencies", [])
            if dependencies:
                print(f"Dependencies: {dependencies}")

                dep_results = {r["step_id"]: r for r in results if r["step_id"] in dependencies}
                exec_context = {
                    **(context or {}),
                    "dependency_results": dep_results,
                    "previous_steps": completed
                }
            else:
                exec_context = {
                    **(context or {}),
                    "previous_steps": completed
                }

            self.tracer.log_decision(
                step=f"Execution - Step {i}",
                action=step['action'],
                reasoning=f"Executing planned step to achieve: {step.get('expected_output', 'step completion')}",
                inputs={"step": step, "context": exec_context}
            )

            try:
                result = self.executor.execute_step(step, exec_context)
                results.append(result)
                completed.append(step)

                self.memory.update_state("completed_steps", completed)
                pending = [s for s in steps if s not in completed]
                self.memory.update_state("pending_steps", pending)

                print(f"Status: {result['status']}")
                if result.get('result', {}).get('type'):
                    print(f"Output type: {result['result']['type']}")

                self.tracer.log_decision(
                    step=f"Execution Result - Step {i}",
                    action="Step completed successfully",
                    reasoning=f"Step produced expected output: {step.get('expected_output')}",
                    outputs=result
                )

            except Exception as e:
                error_result = {
                    "step_id": step.get("id"),
                    "action": step.get("action"),
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                results.append(error_result)

                print(f"Status: failed")
                print(f"Error: {str(e)}")

                self.tracer.log_decision(
                    step=f"Execution Error - Step {i}",
                    action="Step failed",
                    reasoning=f"Encountered error during execution: {str(e)}",
                    outputs=error_result
                )

        return results

    def _finalize_task(self, task_description: str, plan: Dict, results: List[Dict]) -> Dict:
        successful = [r for r in results if r.get("status") == "completed"]
        failed = [r for r in results if r.get("status") == "failed"]

        print(f"\nTask execution completed:")
        print(f"  Total steps: {len(results)}")
        print(f"  Successful: {len(successful)}")
        print(f"  Failed: {len(failed)}")

        task_record = {
            "task": task_description,
            "type": self.memory.get_state("context").get("task_type", "general"),
            "plan": plan,
            "results": results,
            "success_rate": len(successful) / len(results) if results else 0,
            "session_id": self.session_id
        }

        self.memory.add_completed_task(task_record)

        self.tracer.log_decision(
            step="Task Completion",
            action="Finalize and record task",
            reasoning=f"Task completed with {len(successful)}/{len(results)} steps successful",
            outputs={
                "summary": f"{len(successful)} steps completed successfully",
                "success_rate": task_record["success_rate"]
            }
        )

        summary = {
            "task": task_description,
            "goal": plan.get("goal"),
            "total_steps": len(results),
            "successful_steps": len(successful),
            "failed_steps": len(failed),
            "success_rate": task_record["success_rate"],
            "results": results,
            "decision_trace": self.tracer.get_trace()
        }

        return summary

    def get_decision_trace(self) -> str:
        return self.tracer.explain_decision_path()

    def export_session(self, filepath: str):
        self.tracer.export_trace(filepath)
        print(f"\nSession trace exported to: {filepath}")

    def start_new_session(self):
        self.session_id = str(uuid.uuid4())
        self.memory.clear_session()
        self.tracer.clear_trace()
        self.memory.update_state("session_id", self.session_id)
        print(f"\nNew session started: {self.session_id[:8]}...")
