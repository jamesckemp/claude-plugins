#!/usr/bin/env python3
"""
Workflow command helpers for Pings Triage

These functions help Claude execute specific parts of the triage workflow.
Can be called individually or as part of the full triage process.
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path


class TriageWorkflow:
    """Helper class for executing triage workflow commands."""

    def __init__(self, config_path: str = None):
        """Initialize workflow with configuration."""
        if config_path is None:
            # Default to plugin config location
            config_path = Path(__file__).parent.parent.parent / "config" / "user-config.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load user configuration."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration not found at {self.config_path}. "
                "Run 'setup-triage' skill first."
            )

        with open(self.config_path) as f:
            return json.load(f)

    def get_analysis_context(self) -> str:
        """
        Get user context for analysis prompt variable substitution.

        Returns formatted context string to inject into analysis prompt.
        """
        user = self.config["user"]

        context_parts = []

        if user.get("role"):
            context_parts.append(f"- Role: {user['role']}")

        if user.get("context"):
            # Context can be a string or structured data
            if isinstance(user["context"], str):
                context_parts.append(f"- {user['context']}")
            elif isinstance(user["context"], dict):
                for key, value in user["context"].items():
                    context_parts.append(f"- {key}: {value}")

        return "\n".join(context_parts) if context_parts else "No specific context provided"

    def format_analysis_prompt(self, prompt_template: str) -> str:
        """
        Replace variables in analysis prompt template.

        Variables:
        - {USER_NAME}: User's name from config
        - {USER_CONTEXT}: User's role and context
        """
        user = self.config["user"]

        formatted = prompt_template.replace("{USER_NAME}", user.get("name", "the user"))
        formatted = formatted.replace("{USER_CONTEXT}", self.get_analysis_context())

        return formatted

    def get_enabled_platforms(self) -> List[str]:
        """Get list of enabled platform names."""
        platforms = self.config["platforms"]
        return [
            name for name, settings in platforms.items()
            if settings.get("enabled", False)
        ]

    def get_platform_config(self, platform: str) -> Dict:
        """Get configuration for a specific platform."""
        return self.config["platforms"].get(platform, {})

    def get_linear_team_id(self) -> str:
        """Get configured Linear team ID."""
        return self.config["linear"]["team_id"]

    def should_auto_close(self) -> bool:
        """Check if auto-close for responded pings is enabled."""
        return self.config["analysis"].get("auto_close_responded", True)

    def get_lookback_hours(self, platform: str) -> int:
        """Get lookback hours for a platform."""
        return self.config["platforms"].get(platform, {}).get("lookback_hours", 24)


def execute_fetch(workflow: TriageWorkflow) -> Dict:
    """
    Execute FETCH command: Collect pings from all enabled platforms.

    Returns summary of what was collected.
    """
    from state_manager import StateManager

    sm = StateManager()
    enabled_platforms = workflow.get_enabled_platforms()

    results = {
        "command": "fetch",
        "timestamp": datetime.now().isoformat(),
        "platforms": {},
        "total_collected": 0
    }

    for platform in enabled_platforms:
        lookback_hours = workflow.get_lookback_hours(platform)
        last_sync = sm.get_last_sync(platform)

        results["platforms"][platform] = {
            "enabled": True,
            "lookback_hours": lookback_hours,
            "last_sync": last_sync,
            "status": "ready_to_collect"
        }

    return results


def execute_dedupe(workflow: TriageWorkflow) -> Dict:
    """
    Execute DEDUPE command: Deduplicate threads and check for responses.

    Returns summary of deduplication results.
    """
    from state_manager import StateManager

    sm = StateManager()

    results = {
        "command": "dedupe",
        "timestamp": datetime.now().isoformat(),
        "threads_identified": len(sm.state["threads"]),
        "pings_checked": 0,
        "responses_detected": 0
    }

    # Check all unprocessed pings for responses
    unprocessed = sm.get_unprocessed_pings()
    results["pings_checked"] = len(unprocessed)

    return results


def execute_analyze(workflow: TriageWorkflow) -> Dict:
    """
    Execute ANALYZE command: Analyze all unprocessed pings.

    Returns summary of analysis results.
    """
    from state_manager import StateManager

    sm = StateManager()
    unprocessed = sm.get_unprocessed_pings()

    results = {
        "command": "analyze",
        "timestamp": datetime.now().isoformat(),
        "pings_to_analyze": len(unprocessed),
        "analysis_context": workflow.get_analysis_context()
    }

    return results


def execute_sync(workflow: TriageWorkflow) -> Dict:
    """
    Execute SYNC command: Sync analyzed pings to Linear.

    Returns summary of Linear sync results.
    """
    from state_manager import StateManager

    sm = StateManager()
    analyzed = [p for p in sm.state["pings"].values() if p["status"] == "analyzed"]
    handled = sm.get_handled_pings()

    results = {
        "command": "sync",
        "timestamp": datetime.now().isoformat(),
        "team_id": workflow.get_linear_team_id(),
        "pings_to_create": len([p for p in analyzed if not p.get("linear_issue_id")]),
        "pings_to_update": len([p for p in analyzed if p.get("linear_issue_id")]),
        "pings_to_close": len(handled) if workflow.should_auto_close() else 0
    }

    return results


def execute_triage(workflow: TriageWorkflow) -> Dict:
    """
    Execute TRIAGE command: Run complete workflow (fetch + dedupe + analyze + sync).

    Returns summary of full triage run.
    """
    results = {
        "command": "triage",
        "timestamp": datetime.now().isoformat(),
        "steps": {}
    }

    # Execute each step in sequence
    results["steps"]["fetch"] = execute_fetch(workflow)
    results["steps"]["dedupe"] = execute_dedupe(workflow)
    results["steps"]["analyze"] = execute_analyze(workflow)
    results["steps"]["sync"] = execute_sync(workflow)

    return results


if __name__ == "__main__":
    # Example usage
    workflow = TriageWorkflow()

    print("Enabled platforms:", workflow.get_enabled_platforms())
    print("Linear team:", workflow.get_linear_team_id())
    print("\nUser context:")
    print(workflow.get_analysis_context())
