#!/usr/bin/env python3
"""
State Manager for Pings Triage Plugin

Manages the persistent state database of pings, threads, and Linear issues.
Uses JSON for simplicity and portability.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class StateManager:
    """Manages persistent state for ping triage system."""

    def __init__(self, state_file: str = "~/.pings-triage/state.json"):
        """Initialize state manager with path to state file."""
        self.state_file = Path(state_file).expanduser()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Load state from JSON file, or initialize if doesn't exist."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {
            "pings": {},
            "threads": {},
            "linear_issues": {},
            "last_sync": {},
            "metadata": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat()
            }
        }

    def save_state(self):
        """Save current state to JSON file."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    @staticmethod
    def generate_ping_id(platform: str, message_id: str, timestamp: str) -> str:
        """Generate unique ping ID from platform, message ID, and timestamp."""
        content = f"{platform}:{message_id}:{timestamp}"
        return f"ping-{hashlib.sha256(content.encode()).hexdigest()[:32]}"

    @staticmethod
    def generate_thread_id(platform: str, thread_identifier: str) -> str:
        """Generate thread ID for grouping related pings."""
        return f"{platform}-{thread_identifier}"

    def add_ping(
        self,
        platform: str,
        message_id: str,
        timestamp: str,
        author: str,
        content: str,
        thread_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Add a new ping to state.

        Returns:
            ping_id: Unique identifier for this ping
        """
        ping_id = self.generate_ping_id(platform, message_id, timestamp)

        # Check if ping already exists
        if ping_id in self.state["pings"]:
            return ping_id

        self.state["pings"][ping_id] = {
            "id": ping_id,
            "platform": platform,
            "message_id": message_id,
            "timestamp": timestamp,
            "author": author,
            "content": content,
            "thread_id": thread_id,
            "status": "new",  # new, analyzed, handled, closed
            "analysis": None,
            "linear_issue_id": None,
            "response_detected": False,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        # Add to thread if thread_id provided
        if thread_id:
            self._add_to_thread(thread_id, ping_id)

        self.save_state()
        return ping_id

    def _add_to_thread(self, thread_id: str, ping_id: str):
        """Add ping to thread group."""
        if thread_id not in self.state["threads"]:
            self.state["threads"][thread_id] = {
                "id": thread_id,
                "ping_ids": [],
                "linear_issue_id": None,
                "status": "active",  # active, handled, closed
                "created_at": datetime.now().isoformat()
            }

        if ping_id not in self.state["threads"][thread_id]["ping_ids"]:
            self.state["threads"][thread_id]["ping_ids"].append(ping_id)

    def get_ping(self, ping_id: str) -> Optional[Dict]:
        """Get ping by ID."""
        return self.state["pings"].get(ping_id)

    def get_thread_pings(self, thread_id: str) -> List[Dict]:
        """Get all pings in a thread."""
        thread = self.state["threads"].get(thread_id)
        if not thread:
            return []

        return [
            self.state["pings"][pid]
            for pid in thread["ping_ids"]
            if pid in self.state["pings"]
        ]

    def update_ping_analysis(self, ping_id: str, analysis: Dict):
        """Update ping with analysis results."""
        if ping_id in self.state["pings"]:
            self.state["pings"][ping_id]["analysis"] = analysis
            self.state["pings"][ping_id]["status"] = "analyzed"
            self.state["pings"][ping_id]["updated_at"] = datetime.now().isoformat()
            self.save_state()

    def mark_ping_responded(self, ping_id: str):
        """Mark ping as having been responded to."""
        if ping_id in self.state["pings"]:
            self.state["pings"][ping_id]["response_detected"] = True
            self.state["pings"][ping_id]["status"] = "handled"
            self.state["pings"][ping_id]["updated_at"] = datetime.now().isoformat()
            self.save_state()

    def link_linear_issue(self, ping_id: str, linear_issue_id: str):
        """Link ping to Linear issue."""
        if ping_id in self.state["pings"]:
            self.state["pings"][ping_id]["linear_issue_id"] = linear_issue_id
            self.state["pings"][ping_id]["updated_at"] = datetime.now().isoformat()

            # Also update thread if ping is part of thread
            thread_id = self.state["pings"][ping_id].get("thread_id")
            if thread_id and thread_id in self.state["threads"]:
                self.state["threads"][thread_id]["linear_issue_id"] = linear_issue_id

            self.save_state()

    def get_unprocessed_pings(self) -> List[Dict]:
        """Get all pings that need processing (status=new)."""
        return [
            ping for ping in self.state["pings"].values()
            if ping["status"] == "new"
        ]

    def get_handled_pings(self) -> List[Dict]:
        """Get pings that have been responded to."""
        return [
            ping for ping in self.state["pings"].values()
            if ping["response_detected"]
        ]

    def set_last_sync(self, platform: str, timestamp: str):
        """Record last sync time for a platform."""
        self.state["last_sync"][platform] = timestamp
        self.save_state()

    def get_last_sync(self, platform: str) -> Optional[str]:
        """Get last sync time for a platform."""
        return self.state["last_sync"].get(platform)

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about current state."""
        total_pings = len(self.state["pings"])
        new_pings = len([p for p in self.state["pings"].values() if p["status"] == "new"])
        analyzed_pings = len([p for p in self.state["pings"].values() if p["status"] == "analyzed"])
        handled_pings = len([p for p in self.state["pings"].values() if p["response_detected"]])
        total_threads = len(self.state["threads"])

        return {
            "total_pings": total_pings,
            "new_pings": new_pings,
            "analyzed_pings": analyzed_pings,
            "handled_pings": handled_pings,
            "total_threads": total_threads
        }


if __name__ == "__main__":
    # Example usage
    sm = StateManager()

    # Add a test ping
    ping_id = sm.add_ping(
        platform="slack",
        message_id="1234567890.123456",
        timestamp="2024-01-15T10:30:00Z",
        author="John Doe",
        content="Hey @james, can you review this?",
        thread_id="slack-C12345-1234567890",
        metadata={"channel": "C12345", "channel_name": "product-team"}
    )

    print(f"Created ping: {ping_id}")
    print(f"Stats: {sm.get_stats()}")
