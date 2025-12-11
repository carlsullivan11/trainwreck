from __future__ import annotations

from typing import Any


class Reflector:
    """Reflects on execution results and provides feedback."""

    def reflect(self, plan: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
        """
        Analyze the result and return a reflection with:
        - score (0.0 to 1.0)
        - feedback (string)
        - suggestions (list of strings)
        """
        score = self._score_result(result)
        feedback = self._generate_feedback(result)
        suggestions = self._generate_suggestions(result)

        return {
            "score": score,
            "feedback": feedback,
            "suggestions": suggestions,
        }

    def _score_result(self, result: dict[str, Any]) -> float:
        """Score the result (0.0 = failure, 1.0 = perfect)."""
        if "error" in result:
            return 0.0
        if result.get("returncode", 0) != 0:
            return 0.3
        if result.get("stderr"):
            return 0.6
        return 1.0

    def _generate_feedback(self, result: dict[str, Any]) -> str:
        """Generate human-readable feedback."""
        if "error" in result:
            return f"Error: {result['error']}"
        if result.get("returncode", 0) != 0:
            return f"Command failed with return code {result['returncode']}"
        if result.get("stderr"):
            return f"Command succeeded with warnings: {result['stderr']}"
        return "Success"

    def _generate_suggestions(self, result: dict[str, Any]) -> list[str]:
        """Generate suggestions for improvement."""
        suggestions = []
        if "error" in result:
            suggestions.append("Check the command syntax and try again")
        if result.get("returncode", 0) != 0:
            suggestions.append("Review the error output and adjust the command")
        if result.get("stderr"):
            suggestions.append("Consider addressing the warnings")
        return suggestions
