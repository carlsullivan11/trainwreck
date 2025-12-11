from __future__ import annotations

from typing import Any

from trainwreck.agent.executor import Executor
from trainwreck.agent.planner import Planner
from trainwreck.agent.reflector import Reflector
from trainwreck.memory.sqlite_store import SQLiteMemoryStore


class FeedbackLoop:
    """Main feedback loop: Plan → Execute → Reflect → Repeat."""

    def __init__(
        self,
        planner: Planner,
        executor: Executor,
        reflector: Reflector,
        memory: SQLiteMemoryStore | None = None,
    ) -> None:
        self.planner = planner
        self.executor = executor
        self.reflector = reflector
        self.memory = memory

    def iterate(self, goal: str, max_iters: int = 20) -> list[dict[str, Any]]:
        """Run the feedback loop until goal is met or max iterations reached."""
        history: list[dict[str, Any]] = []

        for i in range(max_iters):
            print(f"\n🔄 Iteration {i + 1}/{max_iters}")

            # Build context from history
            context = {
                "repo_state": self._get_repo_state(),
                "history": history,
            }

            # Plan
            plan = self.planner.plan(goal, context)
            print(f"📋 Plan: {plan.description}")

            # Execute
            result = self.executor.execute(plan)
            print(f"⚙️  Executed: {plan.action}")

            # Reflect
            reflection = self.reflector.reflect(plan.__dict__, result)
            print(f"💭 Reflection: {reflection['feedback']} (score: {reflection['score']:.2f})")

            # Record
            step = {
                "iteration": i + 1,
                "plan": plan.__dict__,
                "result": result,
                "reflection": reflection,
                "score": reflection["score"],
                "description": plan.description,
                "outcome": reflection["feedback"],
            }
            history.append(step)

            if self.memory:
                self.memory.add_step(step)

            # Check if goal is met
            if reflection["score"] >= 0.9:
                print("✅ Goal achieved!")
                break

        return history

    def _get_repo_state(self) -> str:
        """Get a summary of the repository state."""
        # This is a placeholder; extend with actual repo inspection
        return "Repository state: [placeholder]"
