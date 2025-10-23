#!/usr/bin/env python3
"""
Memory System for 3D Printer Maintenance Agent

This module provides persistent memory capabilities:
- Stores conversations with metadata
- Retrieves relevant past conversations
- Learns from user interactions
- Provides memory search and management
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
from collections import Counter
import math


class ConversationMemory:
    """Stores and retrieves conversation history with semantic search."""

    def __init__(self, memory_dir: str = "memory"):
        """
        Initialize the memory system.

        Args:
            memory_dir: Directory to store memory files
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)

        self.index_file = self.memory_dir / "memory_index.json"
        self.memories: List[Dict] = []
        self._load_index()

    def _load_index(self):
        """Load the memory index from disk."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                self.memories = json.load(f)
        else:
            self.memories = []

    def _save_index(self):
        """Save the memory index to disk."""
        with open(self.index_file, 'w') as f:
            json.dump(self.memories, f, indent=2)

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text.

        Args:
            text: Text to extract keywords from

        Returns:
            List of keywords
        """
        # Convert to lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)

        # Split into words
        words = text.split()

        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
            'what', 'when', 'where', 'why', 'how', 'who'
        }

        # Filter out stop words and short words
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        # Return unique keywords
        return list(set(keywords))

    def _calculate_relevance(self, query_keywords: List[str], memory_keywords: List[str]) -> float:
        """
        Calculate relevance score between query and memory.

        Uses TF-IDF-like scoring for relevance.

        Args:
            query_keywords: Keywords from the query
            memory_keywords: Keywords from the memory

        Returns:
            Relevance score (0.0 to 1.0)
        """
        if not query_keywords or not memory_keywords:
            return 0.0

        # Count matching keywords
        query_set = set(query_keywords)
        memory_set = set(memory_keywords)
        matches = query_set.intersection(memory_set)

        if not matches:
            return 0.0

        # Calculate score based on:
        # 1. Number of matches
        # 2. Proportion of query covered
        # 3. Proportion of memory covered

        match_count = len(matches)
        query_coverage = match_count / len(query_set)
        memory_coverage = match_count / len(memory_set)

        # Combined score (weighted towards query coverage)
        score = (query_coverage * 0.7) + (memory_coverage * 0.3)

        return score

    def add_conversation(
        self,
        problem: str,
        solution: str,
        conversation_history: List[Dict],
        tags: Optional[List[str]] = None,
        success: bool = True,
        notes: Optional[str] = None
    ) -> str:
        """
        Store a conversation in memory.

        Args:
            problem: The problem description
            solution: The solution or diagnosis
            conversation_history: Full conversation history
            tags: Optional tags for categorization
            success: Whether the solution was successful
            notes: Optional user notes

        Returns:
            Memory ID
        """
        # Generate unique ID
        memory_id = f"MEM_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Extract keywords for search
        problem_keywords = self._extract_keywords(problem)
        solution_keywords = self._extract_keywords(solution)
        all_keywords = list(set(problem_keywords + solution_keywords))

        # Create memory entry
        memory = {
            "id": memory_id,
            "timestamp": datetime.now().isoformat(),
            "problem": problem,
            "solution": solution,
            "conversation_history": conversation_history,
            "keywords": all_keywords,
            "tags": tags or [],
            "success": success,
            "notes": notes,
            "usage_count": 0,
            "helpful_count": 0
        }

        # Add to index
        self.memories.append(memory)
        self._save_index()

        return memory_id

    def search(
        self,
        query: str,
        limit: int = 5,
        min_relevance: float = 0.1,
        tags: Optional[List[str]] = None,
        success_only: bool = False
    ) -> List[Tuple[Dict, float]]:
        """
        Search for relevant past conversations.

        Args:
            query: Search query
            limit: Maximum number of results
            min_relevance: Minimum relevance score (0.0 to 1.0)
            tags: Filter by tags
            success_only: Only return successful solutions

        Returns:
            List of (memory, relevance_score) tuples, sorted by relevance
        """
        if not self.memories:
            return []

        query_keywords = self._extract_keywords(query)

        # Score all memories
        scored_memories = []
        for memory in self.memories:
            # Apply filters
            if success_only and not memory.get("success", True):
                continue

            if tags and not any(tag in memory.get("tags", []) for tag in tags):
                continue

            # Calculate relevance
            relevance = self._calculate_relevance(query_keywords, memory["keywords"])

            if relevance >= min_relevance:
                scored_memories.append((memory, relevance))

        # Sort by relevance (highest first)
        scored_memories.sort(key=lambda x: x[1], reverse=True)

        # Update usage count for retrieved memories
        for memory, _ in scored_memories[:limit]:
            memory["usage_count"] = memory.get("usage_count", 0) + 1

        self._save_index()

        return scored_memories[:limit]

    def get_memory(self, memory_id: str) -> Optional[Dict]:
        """
        Retrieve a specific memory by ID.

        Args:
            memory_id: The memory ID

        Returns:
            Memory dict or None if not found
        """
        for memory in self.memories:
            if memory["id"] == memory_id:
                return memory
        return None

    def mark_helpful(self, memory_id: str):
        """
        Mark a memory as helpful.

        Args:
            memory_id: The memory ID
        """
        memory = self.get_memory(memory_id)
        if memory:
            memory["helpful_count"] = memory.get("helpful_count", 0) + 1
            self._save_index()

    def mark_unhelpful(self, memory_id: str):
        """
        Mark a memory as unhelpful.

        Args:
            memory_id: The memory ID
        """
        memory = self.get_memory(memory_id)
        if memory:
            memory["helpful_count"] = memory.get("helpful_count", 0) - 1
            self._save_index()

    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory.

        Args:
            memory_id: The memory ID

        Returns:
            True if deleted, False if not found
        """
        for i, memory in enumerate(self.memories):
            if memory["id"] == memory_id:
                self.memories.pop(i)
                self._save_index()
                return True
        return False

    def get_statistics(self) -> Dict:
        """
        Get memory system statistics.

        Returns:
            Statistics dictionary
        """
        if not self.memories:
            return {
                "total_memories": 0,
                "successful_solutions": 0,
                "total_usage": 0,
                "most_common_tags": [],
                "most_helpful": []
            }

        # Calculate statistics
        total = len(self.memories)
        successful = sum(1 for m in self.memories if m.get("success", True))
        total_usage = sum(m.get("usage_count", 0) for m in self.memories)

        # Most common tags
        all_tags = []
        for m in self.memories:
            all_tags.extend(m.get("tags", []))
        tag_counts = Counter(all_tags)
        most_common_tags = tag_counts.most_common(10)

        # Most helpful memories
        most_helpful = sorted(
            self.memories,
            key=lambda m: m.get("helpful_count", 0),
            reverse=True
        )[:5]

        return {
            "total_memories": total,
            "successful_solutions": successful,
            "total_usage": total_usage,
            "most_common_tags": most_common_tags,
            "most_helpful": [
                {
                    "id": m["id"],
                    "problem": m["problem"][:100],
                    "helpful_count": m.get("helpful_count", 0)
                }
                for m in most_helpful
            ]
        }

    def list_all(self, limit: int = 20, sort_by: str = "timestamp") -> List[Dict]:
        """
        List all memories.

        Args:
            limit: Maximum number to return
            sort_by: Sort field ("timestamp", "usage_count", "helpful_count")

        Returns:
            List of memory summaries
        """
        if sort_by == "usage_count":
            sorted_memories = sorted(
                self.memories,
                key=lambda m: m.get("usage_count", 0),
                reverse=True
            )
        elif sort_by == "helpful_count":
            sorted_memories = sorted(
                self.memories,
                key=lambda m: m.get("helpful_count", 0),
                reverse=True
            )
        else:  # timestamp
            sorted_memories = sorted(
                self.memories,
                key=lambda m: m.get("timestamp", ""),
                reverse=True
            )

        return [
            {
                "id": m["id"],
                "timestamp": m["timestamp"],
                "problem": m["problem"][:100] + "..." if len(m["problem"]) > 100 else m["problem"],
                "tags": m.get("tags", []),
                "success": m.get("success", True),
                "usage_count": m.get("usage_count", 0),
                "helpful_count": m.get("helpful_count", 0)
            }
            for m in sorted_memories[:limit]
        ]

    def export_memories(self, filepath: str):
        """
        Export all memories to a file.

        Args:
            filepath: Path to export file
        """
        with open(filepath, 'w') as f:
            json.dump(self.memories, f, indent=2)

    def import_memories(self, filepath: str, merge: bool = True):
        """
        Import memories from a file.

        Args:
            filepath: Path to import file
            merge: If True, merge with existing. If False, replace.
        """
        with open(filepath, 'r') as f:
            imported = json.load(f)

        if merge:
            # Avoid duplicates by checking IDs
            existing_ids = {m["id"] for m in self.memories}
            new_memories = [m for m in imported if m["id"] not in existing_ids]
            self.memories.extend(new_memories)
        else:
            self.memories = imported

        self._save_index()

    def format_memory_for_agent(self, memory: Dict, include_full: bool = False) -> str:
        """
        Format a memory for inclusion in agent context.

        Args:
            memory: Memory dictionary
            include_full: Include full conversation history

        Returns:
            Formatted memory string
        """
        timestamp = datetime.fromisoformat(memory["timestamp"]).strftime("%Y-%m-%d %H:%M")

        output = f"""
### Past Experience (Reference: {memory["id"]})
**Date**: {timestamp}
**Problem**: {memory["problem"]}
**Solution**: {memory["solution"]}
**Success**: {'✓ Yes' if memory.get("success") else '✗ No'}
**Times Referenced**: {memory.get("usage_count", 0)}
"""

        if memory.get("notes"):
            output += f"**User Notes**: {memory['notes']}\n"

        if memory.get("tags"):
            output += f"**Tags**: {', '.join(memory['tags'])}\n"

        if include_full and memory.get("conversation_history"):
            output += "\n**Full Conversation**:\n"
            for msg in memory["conversation_history"]:
                role = msg.get("role", "unknown").upper()
                content = msg.get("content", "")[:200]
                output += f"- {role}: {content}...\n"

        return output


def main():
    """Test the memory system."""
    print("Testing Memory System...")

    memory = ConversationMemory()

    # Add test memories
    print("\n1. Adding test memories...")

    memory_id1 = memory.add_conversation(
        problem="Prints coming out as parallelograms instead of squares on CoreXY",
        solution="Belt tension mismatch. Measured both belts - A was 92Hz, B was 98Hz. Adjusted to both 95Hz, problem solved.",
        conversation_history=[
            {"role": "user", "content": "My CoreXY prints are parallelograms"},
            {"role": "assistant", "content": "This is belt tension mismatch..."}
        ],
        tags=["corexy", "belt-tension", "parallelogram"],
        success=True,
        notes="Gates Carbon Drive app was super helpful for measuring"
    )
    print(f"  ✓ Added: {memory_id1}")

    memory_id2 = memory.add_conversation(
        problem="Hotend clogging after 15 minutes with PLA on all-metal hotend",
        solution="Heat creep issue. Heat sink fan was only running at 50%. Set to 100% in firmware, added better fan. No more clogs.",
        conversation_history=[
            {"role": "user", "content": "PLA keeps clogging in my Microswiss hotend"},
            {"role": "assistant", "content": "All-metal hotends need better cooling for PLA..."}
        ],
        tags=["hotend", "heat-creep", "pla", "all-metal"],
        success=True,
        notes="Also reduced retraction from 5mm to 2mm which helped"
    )
    print(f"  ✓ Added: {memory_id2}")

    # Search for relevant memories
    print("\n2. Searching for relevant memories...")

    query1 = "My CoreXY printer is printing rectangles as diamonds"
    results1 = memory.search(query1, limit=3)
    print(f"\n  Query: '{query1}'")
    print(f"  Found {len(results1)} relevant memories:")
    for mem, score in results1:
        print(f"    - {mem['id']}: {mem['problem'][:60]}... (relevance: {score:.2f})")

    query2 = "PLA clogging in all-metal hotend"
    results2 = memory.search(query2, limit=3)
    print(f"\n  Query: '{query2}'")
    print(f"  Found {len(results2)} relevant memories:")
    for mem, score in results2:
        print(f"    - {mem['id']}: {mem['problem'][:60]}... (relevance: {score:.2f})")

    # Get statistics
    print("\n3. Memory statistics:")
    stats = memory.get_statistics()
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Successful solutions: {stats['successful_solutions']}")
    print(f"  Total usage: {stats['total_usage']}")
    print(f"  Most common tags: {stats['most_common_tags']}")

    # List all memories
    print("\n4. All memories:")
    all_memories = memory.list_all(limit=10)
    for m in all_memories:
        print(f"  - {m['id']}: {m['problem']}")

    print("\n✓ Memory system test complete!")


if __name__ == "__main__":
    main()
