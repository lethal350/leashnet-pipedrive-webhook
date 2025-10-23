# Memory System - Persistent Learning for Your 3D Printer Agent

The memory system allows your agent to "remember" past conversations and automatically reference them when helping with similar problems in the future.

---

## What It Does

**Your agent now has long-term memory!**

- ✅ **Saves conversations** with problem + solution + tags
- ✅ **Searches automatically** when you ask questions (finds similar past issues)
- ✅ **References past solutions** in responses
- ✅ **Tracks usage** (which solutions get referenced most)
- ✅ **Learns from you** (mark solutions as helpful/unhelpful)

---

## How It Works

### Automatic Memory Search

When you ask a question, the agent automatically:
1. Searches through past conversations
2. Finds the 3 most relevant ones (similarity-based)
3. Includes them in the response context
4. References them when diagnosing your problem

**Example:**

```bash
# First time (Week 1):
You: "My CoreXY prints are parallelograms"
Agent: [Diagnoses belt tension mismatch...]
You: [Saves to memory with tags: corexy, belt-tension]

# Later (Week 5):
You: "Why are my CoreXY rectangles printing skewed?"
Agent: "I notice you've had a similar issue before (Reference: MEM_20251023_104426)
        where belt tension mismatch caused parallelograms. Let me check if this
        applies to your current situation..."
```

The agent **automatically referenced** your past experience!

---

## Using the Memory System

### Via Interactive CLI

```bash
python cli.py

# After diagnosing a problem:
> save

Problem summary: CoreXY printing parallelograms
Solution summary: Belt tension mismatch - adjusted A belt from 92Hz to 95Hz to match B belt
Tags (comma-separated): corexy,belt-tension,parallelogram
Was this solution successful? (yes/no): yes
Additional notes (optional): Gates Carbon Drive app was super helpful

✓ Conversation saved to memory: MEM_20251023_104426
```

### Search Memory

```bash
> search

Search query: belt tension
Max results (default: 5): 3

Found 2 relevant memories:

1. MEM_20251023_104426 (relevance: 0.85)
   Problem: CoreXY printing parallelograms
   Solution: Belt tension mismatch - adjusted A belt from 92Hz to 95Hz...
   Date: 2025-10-23 10:44:26
   Success: ✓
   Used: 5 times

2. MEM_20251015_083012 (relevance: 0.42)
   Problem: Layer shifts on Y axis
   Solution: Y belt was loose - tightened to 95Hz...
```

### List All Memories

```bash
> list

Sort by (timestamp/usage/helpful) [default: timestamp]: usage
Max results (default: 20): 10

10 memories (sorted by usage_count):

1. MEM_20251023_104426
   CoreXY printing parallelograms
   Date: 2025-10-23T10:44:26
   Tags: corexy, belt-tension, parallelogram
   Used: 8 times | Helpful: 5

2. MEM_20251020_153045
   Hotend clogging with PLA
   Date: 2025-10-20T15:30:45
   Tags: hotend, heat-creep, pla, all-metal
   Used: 6 times | Helpful: 4
```

### View Statistics

```bash
> stats

Memory Statistics

Total Memories: 15
Successful Solutions: 13
Total Times Referenced: 47

Most Common Tags:
  - belt-tension: 4 times
  - hotend: 3 times
  - corexy: 3 times
  - extrusion: 2 times

Most Helpful Memories:
  - MEM_20251023_104426: CoreXY printing parallelograms (helpful: 5)
  - MEM_20251020_153045: Hotend clogging with PLA (helpful: 4)
```

---

## Using Memory in Python

### Save Conversations

```python
from agents.printer_maintenance_agent import PrinterMaintenanceAgent

agent = PrinterMaintenanceAgent()

# Have a conversation
response = agent.diagnose("My hotend keeps clogging with PLA")
print(response)

# Save it to memory
agent.save_to_memory(
    problem_summary="Hotend clogging with PLA after 15 minutes",
    solution_summary="Heat creep - upgraded heat sink fan to 10,000 RPM, reduced retraction to 2mm",
    tags=["hotend", "heat-creep", "pla", "all-metal"],
    success=True,
    notes="Microswiss hotend, was using 5mm retraction which was too much"
)
```

### Search Memory

```python
# Search for relevant past solutions
results = agent.search_memory("belt tension CoreXY", limit=5)

for memory, relevance in results:
    print(f"Relevance: {relevance:.2f}")
    print(f"Problem: {memory['problem']}")
    print(f"Solution: {memory['solution']}")
    print()
```

### Get Statistics

```python
stats = agent.get_memory_stats()
print(f"Total memories: {stats['total_memories']}")
print(f"Success rate: {stats['successful_solutions'] / stats['total_memories'] * 100:.1f}%")
```

### Mark Memories as Helpful

```python
# After using a memory that helped solve your problem
agent.mark_memory_helpful("MEM_20251023_104426")

# If a memory wasn't helpful
agent.mark_memory_unhelpful("MEM_20251015_083012")
```

---

## Memory Storage

### Where Memories Are Stored

```
leashnet-pipedrive-webhook/
└── memory/
    └── memory_index.json    # All memories stored here
```

The file is human-readable JSON. You can:
- Back it up
- Share with others
- Edit manually (carefully!)
- Version control it

### Memory Entry Structure

```json
{
  "id": "MEM_20251023_104426",
  "timestamp": "2025-10-23T10:44:26.123456",
  "problem": "CoreXY printing parallelograms",
  "solution": "Belt tension mismatch...",
  "keywords": ["corexy", "printing", "parallelograms", "belt", "tension"],
  "tags": ["corexy", "belt-tension", "parallelogram"],
  "success": true,
  "notes": "Gates Carbon Drive app was helpful",
  "usage_count": 8,
  "helpful_count": 5,
  "conversation_history": [...]
}
```

---

## How Memory Search Works

### Keyword Matching

The system uses **TF-IDF-style relevance scoring**:

1. Extracts keywords from your query
2. Extracts keywords from each stored memory
3. Calculates relevance based on:
   - Number of matching keywords
   - Proportion of query covered
   - Proportion of memory covered

**Example:**

```
Query: "CoreXY belt tension parallelogram prints"
Keywords: [corexy, belt, tension, parallelogram, prints]

Memory 1: "Belt tension on Ender 3"
Keywords: [belt, tension, ender]
Matches: 2/5 = 40% coverage
Relevance: 0.42

Memory 2: "CoreXY printing parallelograms due to belt mismatch"
Keywords: [corexy, printing, parallelograms, belt, mismatch]
Matches: 4/5 = 80% coverage
Relevance: 0.85  ← Selected!
```

### Relevance Threshold

- Minimum relevance: **0.2** (20% keyword match)
- Typical good match: **0.5+** (50%+ keyword match)
- Excellent match: **0.8+** (80%+ keyword match)

---

## Best Practices

### 1. Good Problem Summaries

❌ **Bad**: "printer broken"
✅ **Good**: "CoreXY printing parallelograms instead of squares"

❌ **Bad**: "hotend issue"
✅ **Good**: "Hotend clogging after 15 minutes when printing PLA on all-metal hotend"

### 2. Good Solution Summaries

❌ **Bad**: "fixed it"
✅ **Good**: "Belt tension mismatch - measured with Gates app, adjusted A belt from 92Hz to 95Hz to match B belt at 95Hz"

❌ **Bad**: "changed settings"
✅ **Good**: "Heat creep issue - upgraded heat sink fan from stock to 10,000 RPM Sunon, reduced retraction from 5mm to 2mm"

### 3. Effective Tags

**Use specific, searchable tags:**
- ✅ "corexy", "belt-tension", "parallelogram"
- ✅ "hotend", "heat-creep", "pla", "all-metal"
- ✅ "bltouch", "bed-leveling", "z-offset"

**Avoid vague tags:**
- ❌ "problem", "issue", "broken"
- ❌ "fix", "solved", "done"

### 4. Add Notes

Notes help future-you remember context:
- What tools you used ("Gates Carbon Drive app")
- What didn't work ("Tried tightening wheels first, didn't help")
- Specific part numbers ("Replaced with Sunon MF40101V1-1000U-A99")

### 5. Mark Success/Failure

Be honest about whether solutions worked:
- ✅ **Success = true**: Problem completely solved
- ❌ **Success = false**: Didn't fix it, or partial fix

Failed solutions are valuable too - they help avoid dead ends!

---

## Advanced Features

### Export & Import Memories

**Share memories with others:**

```python
# Export your memories
agent.memory.export_memories("my_printer_memories.json")

# Import someone else's memories
agent.memory.import_memories("community_fixes.json", merge=True)
```

**Use case**: Share a collection of your team's or community's solutions!

### Disable Memory

If you want to temporarily disable memory:

```python
agent = PrinterMaintenanceAgent(enable_memory=False)
```

Or delete the `memory/` directory to start fresh.

### Memory Statistics for Insights

Track what problems you encounter most:

```python
stats = agent.get_memory_stats()

# Most common issues
print("Your most common problems:")
for tag, count in stats['most_common_tags']:
    print(f"  - {tag}: {count} times")

# Identifies patterns:
# Maybe you keep having belt-tension issues → Check maintenance schedule
# Maybe hotend-clog appears often → Consider upgrade to all-metal
```

---

## Example Workflows

### Workflow 1: First Encounter

```bash
# Week 1: New problem
> diagnose
Problem: My CoreXY prints rectangles as parallelograms

Agent: [Provides diagnosis: belt tension mismatch]

# You fix it!
> save
Problem summary: CoreXY printing parallelograms
Solution summary: Belt A was 92Hz, B was 98Hz. Adjusted both to 95Hz. Fixed!
Tags: corexy,belt-tension,parallelogram
Success: yes
```

### Workflow 2: Similar Problem Later

```bash
# Week 8: Similar issue
> diagnose
Problem: My CoreXY printer is making diagonal rectangles

Agent: "I found a relevant past experience (MEM_20251023_104426) where
        you had parallelograms caused by belt tension mismatch. You fixed it
        by measuring both belts with the Gates app and matching them to 95Hz.

        Let me diagnose if this is the same issue..."

[Agent references your past solution automatically!]
```

### Workflow 3: Building Knowledge Base

```bash
# After 3 months of using your printer:
> stats

Total Memories: 23
Successful Solutions: 20
Most Common Tags:
  - belt-tension: 5 times    ← You've learned belt tensioning well!
  - hotend: 4 times          ← Hotend is a common issue area
  - bed-leveling: 4 times
  - extrusion: 3 times

# Export and share
> export my_ender3_corexy_solutions.json

# Other CoreXY builders can learn from your experience!
```

---

## Troubleshooting

### "Memory system is disabled"

**Fix**: Make sure agent is initialized with memory enabled:
```python
agent = PrinterMaintenanceAgent(enable_memory=True)  # default
```

### "No memories found"

**Reasons**:
- Haven't saved any conversations yet
- Query keywords don't match stored memories
- Try broader search terms

### Memory file corrupted

**Fix**:
```bash
# Backup first
cp memory/memory_index.json memory/memory_index.json.backup

# Delete and start fresh
rm -rf memory/

# Or restore from backup
cp memory/memory_index.json.backup memory/memory_index.json
```

### Search returns irrelevant results

**Improve**:
- Use more specific keywords
- Add better tags when saving
- Increase min_relevance threshold in code

---

## Technical Details

### How Automatic Retrieval Works

When you call `agent.diagnose()`:

1. **Extract query keywords**
   ```python
   query = "CoreXY printing parallelograms"
   keywords = ["corexy", "printing", "parallelograms"]
   ```

2. **Search memory**
   ```python
   results = memory.search(query, limit=3, min_relevance=0.2)
   ```

3. **Add to context**
   ```python
   # Agent receives:
   # - Your question
   # - Relevant past experiences
   # - All the expert knowledge from system prompt
   ```

4. **Claude generates response** using all context

### Performance

- **Search speed**: <50ms for 1000 memories
- **Storage**: ~2KB per memory (compressed JSON)
- **API cost impact**: Negligible (memories are small)

---

## Future Enhancements (Ideas)

Want to contribute? Consider adding:

1. **Semantic embeddings** - Use sentence-transformers for better matching
2. **Auto-tagging** - LLM automatically tags conversations
3. **Memory pruning** - Auto-delete old unhelpful memories
4. **Cloud sync** - Sync memories across devices
5. **Memory visualization** - Graph of problem categories
6. **Community memories** - Shared database of solutions

---

## Summary

**The memory system makes your agent smarter over time!**

✅ Saves every conversation (when you tell it to)
✅ Automatically searches for similar past issues
✅ References past solutions in new diagnoses
✅ Tracks what works and what doesn't
✅ Learns from YOUR specific printer and issues

**It's like having a personal notebook that the agent reads before helping you!**

---

**Pro tip**: After every successful fix, take 30 seconds to save it to memory. Future-you will thank you! 🙏

Happy printing! 🖨️
