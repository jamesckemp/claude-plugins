#!/usr/bin/env python3
"""
Ping Analyzer for Pings Triage Plugin

Formats ping data for analysis and processes analysis results.
The actual LLM analysis is performed by Claude using the analysis prompt.
"""

import json
from typing import Dict, List, Optional
from datetime import datetime


class PingAnalyzer:
    """Formats pings for analysis and validates analysis results."""

    @staticmethod
    def format_for_analysis(ping: Dict, thread_context: Optional[List[Dict]] = None) -> str:
        """
        Format a ping and its context for LLM analysis.

        Args:
            ping: Ping data from state manager
            thread_context: Optional list of previous pings in the thread

        Returns:
            Formatted string ready for analysis prompt
        """
        author = ping.get("author", "Unknown")
        content = ping.get("content", "")
        platform = ping.get("platform", "unknown")
        timestamp = ping.get("timestamp", "")

        # Format main message
        analysis_input = f"""Author: {author}
Message: {content}
Source: {platform}
Time: {timestamp}"""

        # Add thread context if available
        if thread_context and len(thread_context) > 0:
            context_messages = []
            for ctx_ping in thread_context:
                ctx_author = ctx_ping.get("author", "Unknown")
                ctx_content = ctx_ping.get("content", "")
                ctx_time = ctx_ping.get("timestamp", "")
                context_messages.append(f"[{ctx_time}] {ctx_author}: {ctx_content}")

            additional_context = "\n".join(context_messages)
            analysis_input += f"\n\nAdditional Context (earlier messages in thread):\n{additional_context}"

        return analysis_input

    @staticmethod
    def validate_analysis(analysis: Dict) -> bool:
        """
        Validate that analysis contains required fields.

        Required fields:
        - title: str
        - summary: str
        - suggested_action: str (one of: Acknowledge, Review, Reply, Decide, Delegate)
        - priority: int (0-4)
        - specific_guidance: str (can be empty)
        """
        required_fields = ["title", "summary", "suggested_action", "priority"]

        # Check all required fields present
        for field in required_fields:
            if field not in analysis:
                return False

        # Validate suggested_action is one of allowed values
        valid_actions = ["Acknowledge", "Review", "Reply", "Decide", "Delegate"]
        if analysis["suggested_action"] not in valid_actions:
            return False

        # Validate priority is 0-4
        try:
            priority = int(analysis["priority"])
            if priority < 0 or priority > 4:
                return False
        except (ValueError, TypeError):
            return False

        # Ensure specific_guidance exists (can be empty string)
        if "specific_guidance" not in analysis:
            analysis["specific_guidance"] = ""

        return True

    @staticmethod
    def normalize_analysis(analysis: Dict) -> Dict:
        """
        Normalize analysis format for consistent storage.

        Ensures:
        - Priority is an integer
        - All fields have consistent types
        - Timestamps are added
        """
        normalized = {
            "title": str(analysis.get("title", "")).strip(),
            "summary": str(analysis.get("summary", "")).strip(),
            "suggested_action": str(analysis.get("suggested_action", "")).strip(),
            "priority": int(analysis.get("priority", 3)),
            "specific_guidance": str(analysis.get("specific_guidance", "")).strip(),
            "analyzed_at": datetime.now().isoformat()
        }

        return normalized

    @staticmethod
    def extract_urgency_signals(content: str) -> Dict[str, bool]:
        """
        Extract urgency signals from message content.

        Returns dict with boolean flags for different urgency indicators.
        """
        content_lower = content.lower()

        signals = {
            "urgent": any(word in content_lower for word in [
                "urgent", "asap", "immediately", "critical", "emergency"
            ]),
            "blocking": any(word in content_lower for word in [
                "blocking", "blocked", "blocker", "waiting on"
            ]),
            "deadline_today": any(phrase in content_lower for phrase in [
                "today", "by eod", "end of day", "this afternoon"
            ]),
            "deadline_this_week": any(phrase in content_lower for phrase in [
                "this week", "by friday", "end of week"
            ]),
            "question_mark": "?" in content,
            "exclamation": "!" in content
        }

        return signals

    @staticmethod
    def suggest_priority(content: str, analysis_priority: Optional[int] = None) -> int:
        """
        Suggest priority based on content signals and analysis.

        If analysis_priority provided, use it as base and adjust based on signals.
        Otherwise, determine priority from signals alone.
        """
        signals = PingAnalyzer.extract_urgency_signals(content)

        # Start with analysis priority or default to 3 (Normal)
        priority = analysis_priority if analysis_priority is not None else 3

        # Bump priority based on urgency signals
        if signals["urgent"] or signals["blocking"]:
            priority = min(priority, 1)  # Ensure at least Urgent
        elif signals["deadline_today"]:
            priority = min(priority, 1)  # Today deadline = Urgent
        elif signals["deadline_this_week"]:
            priority = min(priority, 2)  # This week = High

        return priority

    @staticmethod
    def create_analysis_payload(ping: Dict, analysis: Dict) -> Dict:
        """
        Create complete payload combining ping data and analysis.

        This is the format that will be stored in state and used for Linear sync.
        """
        return {
            "ping_id": ping["id"],
            "platform": ping["platform"],
            "author": ping["author"],
            "timestamp": ping["timestamp"],
            "thread_id": ping.get("thread_id"),
            "analysis": analysis,
            "metadata": ping.get("metadata", {})
        }


if __name__ == "__main__":
    # Example usage
    analyzer = PingAnalyzer()

    # Example ping
    test_ping = {
        "id": "ping-abc123",
        "platform": "slack",
        "author": "John Doe",
        "content": "Hey @james, can you review this design urgently? We're blocked.",
        "timestamp": "2024-01-15T10:30:00Z",
        "thread_id": "slack-C12345-1234567890",
        "metadata": {"channel": "C12345"}
    }

    # Format for analysis
    formatted = analyzer.format_for_analysis(test_ping)
    print("Formatted for analysis:")
    print(formatted)
    print()

    # Extract urgency signals
    signals = analyzer.extract_urgency_signals(test_ping["content"])
    print(f"Urgency signals: {signals}")
    print()

    # Example analysis result
    test_analysis = {
        "title": "John Doe: Review design urgently",
        "summary": "John is asking you to review a design. The team is blocked waiting for your feedback.",
        "suggested_action": "Review",
        "priority": 1,
        "specific_guidance": "Design review needed to unblock the team"
    }

    # Validate and normalize
    if analyzer.validate_analysis(test_analysis):
        normalized = analyzer.normalize_analysis(test_analysis)
        print(f"Normalized analysis: {json.dumps(normalized, indent=2)}")
    else:
        print("Analysis validation failed")
