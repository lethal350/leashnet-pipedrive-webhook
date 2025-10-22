```markdown
# 3D Printer Agent Virtual Training Environment

A comprehensive simulation system where the Claude 3D Printer Maintenance Agent can practice diagnosing and solving thousands of realistic 3D printer problems, building real-world experience through virtual scenarios.

## Overview

This training environment provides:
- **Realistic Physics Simulation**: Virtual printers with accurate component wear and degradation
- **Scenario Generation**: Automatic creation of diverse troubleshooting scenarios
- **Performance Evaluation**: Automated scoring and feedback on agent responses
- **Real-World Scenarios**: Database of actual community-reported problems
- **Progressive Training**: Structured learning from easy to hard scenarios
- **Analytics Dashboard**: Detailed performance metrics and improvement tracking

## Quick Start

### Prerequisites

```bash
# Ensure you have the agent environment set up
cd /path/to/leashnet-pipedrive-webhook
source venv/bin/activate
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Run Your First Training Session

```bash
python training/train_agent.py
```

Choose option 1 for an interactive single scenario, or option 2 for a small batch.

## Training Modes

### 1. Single Scenario (Interactive)
Perfect for understanding how the system works:
```bash
python training/train_agent.py
# Select option 1
```

**Features**:
- Step-by-step walkthrough
- Full agent response displayed
- Detailed evaluation with feedback
- Shows actual problems for learning

### 2. Small Batch (10 scenarios)
Quick training session:
```bash
python training/train_agent.py
# Select option 2
```

**Features**:
- 10 scenarios at chosen difficulty
- Progress shown between scenarios
- Session summary at end
- ~15-20 minutes

### 3. Progressive Training
Structured learning path:
```bash
python training/train_agent.py
# Select option 5
```

**Features**:
- Starts easy, progresses to hard
- Configurable scenarios per level
- Performance tracking between levels
- ~30-45 minutes for 10 scenarios/level

### 4. Stress Test (100+ scenarios)
Comprehensive evaluation:
```bash
python training/train_agent.py
# Select option 6
```

**Features**:
- Large-scale testing (100-1000+ scenarios)
- Automatic checkpointing
- Statistical analysis
- ~2-4 hours for 100 scenarios

## System Architecture

### Components

```
training/
├── virtual_printer.py          # Printer simulation engine
├── train_agent.py             # Training orchestrator
├── scenario_database.py       # Real-world scenarios
├── __init__.py                # Package initialization
└── README.md                  # This file

Generated During Training:
├── training_results/          # Session summaries
├── checkpoints/               # Automatic saves
└── scenario_review/           # Export for human review
```

### Virtual Printer Simulator

The `VirtualPrinter` class simulates a complete 3D printer:

```python
from training.virtual_printer import VirtualPrinter, PrinterType

# Create a virtual Ender 3
printer = VirtualPrinter(PrinterType.ENDER_3)

# Simulate 100 hours of use
printer.simulate_printing(hours=100)

# Introduce a problem
printer.introduce_problem("nozzle_clog", ProblemSeverity.MAJOR)

# Get observable symptoms
symptoms = printer.get_symptoms()
# Output: ["Little to no filament coming out", "Extruder motor clicking", ...]
```

**Simulated Components** (25+ components):
- Mechanical: Belts, wheels, lead screws, extruder
- Hotend: Nozzle, PTFE tube, heat break, cooling fan
- Bed: Surface, springs, heater
- Electronics: Mainboard, PSU, stepper motors, drivers
- Sensors: Endstops, thermistors, BLTouch

**Realistic Physics**:
- Component wear over time
- Settings drift (bed level, belt tension)
- Temperature effects
- Multiple interacting problems

### Scenario Generator

Creates diverse troubleshooting scenarios:

```python
from training.virtual_printer import ScenarioGenerator

generator = ScenarioGenerator()

# Generate a medium difficulty scenario
scenario = generator.generate_scenario("medium")

# Generate batch
scenarios = generator.generate_batch(count=50, difficulty="hard")
```

**Features**:
- 11 major problem types
- Realistic occurrence rates
- Multiple printer architectures (Cartesian, CoreXY, IDEX)
- Varied user communication styles
- 1-3 simultaneous problems (difficulty-dependent)

### Performance Evaluator

Scores agent responses across 4 categories:

```python
from training.virtual_printer import ScenarioEvaluator

evaluator = ScenarioEvaluator()

# Evaluate response
evaluation = evaluator.evaluate_response(scenario, agent_response)

print(f"Score: {evaluation['total_score']}/100")
print(f"Grade: {evaluation['grade']}")
```

**Scoring Breakdown**:
- **Problem Identification** (40 pts): Did agent identify all issues?
- **Root Cause Analysis** (30 pts): Did agent find root causes?
- **Solution Quality** (20 pts): Are solutions comprehensive?
- **Communication** (10 pts): Is response clear and helpful?

**Grades**:
- A (90-100): Excellent - Production ready
- B (80-89): Good - Minor improvements needed
- C (70-79): Satisfactory - Continued training recommended
- D (60-69): Needs Improvement - More training required
- F (<60): Poor - Significant work needed

## Real-World Scenario Database

12 curated scenarios from actual community reports:

```python
from training.scenario_database import RealWorldScenarios

# Get all real scenarios
scenarios = RealWorldScenarios.get_all_scenarios()

# Filter by difficulty
easy_scenarios = RealWorldScenarios.get_beginner_scenarios()
hard_scenarios = RealWorldScenarios.get_advanced_scenarios()

# Filter by problem type
clog_scenarios = RealWorldScenarios.get_by_problem_type("nozzle_clog")
```

**Included Scenarios**:
1. Weak Layers and Gaps (Under-extrusion)
2. Random Layer Shifts (Loose pulley)
3. First Layer Won't Stick (Z-offset + dirty bed)
4. Thermal Runaway Error (Loose thermistor)
5. Extruder Clicking, No Extrusion (Heat creep)
6. Excessive Stringing (Temp + retraction)
7. BLTouch Won't Deploy (Firmware config)
8. Z-Axis Binding (Over-tightened wheels)
9. Dual Z Desync (Manual movement while off)
10. CoreXY Diagonal Shifts (Unequal belt tension)
11. Printer Won't Power On (Loose cable)
12. IDEX Misalignment (Thermal expansion)

## Understanding the Output

### During Training

```
==================================================================
Scenario 15: SCENARIO_0015
Difficulty: MEDIUM
Printer: Ender 3 Pro
==================================================================

User says: "My prints are coming out really weak..."

Observable symptoms:
  • Gaps between perimeter lines
  • Sparse infill
  • Transparent top layers

🤖 Agent is diagnosing...

──────────────────────────────────────────────────────────────────
AGENT RESPONSE:
──────────────────────────────────────────────────────────────────
Based on your symptoms, this appears to be under-extrusion...
[Full agent response]
──────────────────────────────────────────────────────────────────

📊 EVALUATION RESULTS:
   Overall Score: 85.0/100
   Grade: B - Good
   Response Time: 3.45s

   Breakdown:
     • Problem Identification: 40.0/40
     • Root Cause Analysis: 25.0/30
     • Solution Quality: 16.0/20
     • Communication: 4.0/10

   Feedback:
     ✓ Correctly identified all problems
     ⚠ Solutions could be more detailed
     ✓ Well-structured response

   Actual Problems (for review):
     • under_extrusion (moderate) - Root: partial_clog
```

### Session Summary

```
==================================================================
TRAINING SESSION SUMMARY
==================================================================

Session: training_20251022_143052
Duration: 15.3 minutes
Scenarios Completed: 25

📈 PERFORMANCE METRICS:
   Overall Average: 82.4/100
   Trend: Improving (+3.2 points)

📊 CATEGORY BREAKDOWN:
   • Problem Identification: 35.6/40 (89%)
   • Root Cause Analysis: 24.1/30 (80%)
   • Solution Quality: 16.5/20 (83%)
   • Communication: 6.2/10 (62%)

🎓 GRADE DISTRIBUTION:
   A: ████████████████ 16 (64%)
   B: ██████ 6 (24%)
   C: ██ 2 (8%)
   D:  1 (4%)
   F:  0 (0%)

💡 RECOMMENDATIONS:
   ⚠️  Enhance communication and user guidance
   ✅ Good performance. Minor improvements needed.

💾 Full session data saved to: training_results/training_20251022_143052.json
```

## Advanced Usage

### Custom Training Scripts

Create custom training scenarios:

```python
from agents.printer_maintenance_agent import PrinterMaintenanceAgent
from training import TrainingSession, ScenarioGenerator

# Initialize
agent = PrinterMaintenanceAgent()
session = TrainingSession(agent, session_name="custom_training")

# Generate specific scenario
generator = ScenarioGenerator()
scenario = generator.generate_scenario("hard")

# Modify scenario for specific test
scenario['user_description'] = "Your custom problem description..."
scenario['symptoms'] = ["Custom symptom 1", "Custom symptom 2"]

# Run scenario
evaluation = session.run_single_scenario(scenario, verbose=True)

# Check results
if evaluation['total_score'] >= 80:
    print("✅ Agent performed well!")
else:
    print("❌ Agent needs improvement")
```

### Batch Processing

Process multiple scenarios programmatically:

```python
from training import TrainingSession

agent = PrinterMaintenanceAgent()
session = TrainingSession(agent)

# Run stress test
session.run_stress_test(
    count=500,
    save_interval=50  # Checkpoint every 50 scenarios
)

# Get statistics
stats = session.evaluator.get_statistics()
print(f"Average Score: {stats['average_score']:.1f}")
print(f"Trend: {stats['improvement_trend']}")
```

### Export for Analysis

Export scenarios for human review or further analysis:

```python
session.export_scenarios_for_review("review_export.json")

# Load exported data
with open("review_export.json", 'r') as f:
    data = json.load(f)

# Analyze specific categories
for eval in data['scenarios']:
    if eval['scores']['communication'] < 5:
        print(f"Low communication score in {eval['scenario_id']}")
```

## Performance Optimization

### Recommended Training Progression

**Week 1: Foundation** (50 scenarios)
- 30 easy scenarios
- 20 medium scenarios
- Goal: 75+ average score

**Week 2: Intermediate** (75 scenarios)
- 25 medium scenarios
- 50 hard scenarios
- Goal: 80+ average score

**Week 3: Advanced** (100 scenarios)
- 50 hard scenarios
- 50 mixed real-world scenarios
- Goal: 85+ average score

**Week 4: Mastery** (200+ scenarios)
- Stress test with all difficulties
- Real-world scenario database
- Goal: 90+ average score, A grade consistency

### Monitoring Progress

Track improvement over time:

```python
# Run weekly evaluations
week1_stats = session.evaluator.get_statistics()
# ... train more ...
week2_stats = session.evaluator.get_statistics()

# Compare
improvement = week2_stats['average_score'] - week1_stats['average_score']
print(f"Improvement: +{improvement:.1f} points")
```

## Troubleshooting

### Agent Not Initializing
```
Error: ANTHROPIC_API_KEY must be set
```
**Solution**: Set environment variable
```bash
export ANTHROPIC_API_KEY='your-key'
```

### Low Scores in Specific Category
```
Problem Identification: 20/40 (50%)
```
**Solution**: Agent may need updated knowledge base. Review scenarios where identification failed and enhance agent's problem recognition patterns.

### Inconsistent Performance
```
Trend: Declining (-5.2 points)
```
**Solution**: May indicate API rate limiting or fatigue. Take breaks between large batches. Check if scenarios are getting progressively harder.

## Best Practices

1. **Start Small**: Begin with 10-25 scenarios to understand the system
2. **Review Failures**: Examine scenarios where agent scored <70
3. **Progressive Difficulty**: Don't jump to hard mode immediately
4. **Regular Checkpoints**: Save progress frequently in long sessions
5. **Analyze Trends**: Look for patterns in failures (specific problem types)
6. **Iterate Knowledge**: Update agent based on consistent weaknesses
7. **Mix Real & Generated**: Combine database scenarios with generated ones
8. **Set Goals**: Define target scores before each session
9. **Document Learnings**: Keep notes on what the agent struggles with
10. **Celebrate Progress**: Recognize improvements in scores and grades

## Future Enhancements

Planned features:
- [ ] Image-based diagnostic scenarios
- [ ] Multi-turn conversation scenarios
- [ ] Comparative analysis vs human experts
- [ ] Community scenario contributions
- [ ] Automated agent knowledge base updates
- [ ] Integration with actual OctoPrint logs
- [ ] Video walkthrough generation
- [ ] Adversarial scenario generation

## Contributing

To add new scenarios to the database:

1. Document the scenario with:
   - Clear user description
   - Observable symptoms
   - Actual root causes
   - Expected solution
   - Lesson learned

2. Add to `scenario_database.py`:
```python
{
    "id": "REAL_013",
    "title": "Your Problem Title",
    "source": "Where you found it",
    "difficulty": "easy|medium|hard",
    "printer_type": "Printer model",
    "user_description": "User's problem description",
    "symptoms": ["List", "of", "symptoms"],
    "actual_problems": [
        {
            "type": "problem_type",
            "root_cause": "specific_cause",
            "severity": "minor|moderate|major|critical"
        }
    ],
    "solution_summary": "Brief solution",
    "lesson": "Key takeaway"
}
```

3. Test the scenario:
```python
from training.scenario_database import RealWorldScenarios
scenarios = RealWorldScenarios.get_all_scenarios()
# Verify your scenario is included
```

## FAQs

**Q: How long does training take?**
A: 10 scenarios: ~15 min, 100 scenarios: ~2-3 hours, 1000 scenarios: ~20-30 hours

**Q: Can I pause and resume training?**
A: Yes! The system auto-saves checkpoints. Stop with Ctrl+C and resume by loading the checkpoint.

**Q: What's a good target score?**
A: 75+ is good, 85+ is excellent, 90+ is expert level

**Q: How many scenarios needed for production readiness?**
A: Minimum 200-300 scenarios with 85+ average score and A/B grade consistency

**Q: Can I use custom problem types?**
A: Yes! Extend the `ScenarioGenerator` class with your own problem definitions

**Q: Does this improve the actual agent?**
A: The training evaluates current capabilities. To improve the agent, use insights to enhance the knowledge base in `printer_maintenance_agent.py`

## Resources

- **Agent Documentation**: `../README.md`
- **Hardware Diagnostics**: `../HARDWARE_DIAGNOSTICS.md`
- **Upgrade Guide**: `../UPGRADE_GUIDE.md`
- **Community**: r/3Dprinting, r/ender3, Voron Discord

## License

Part of the 3D Printer Maintenance Agent project. See main repository for license details.

---

**Ready to start training?** Run `python training/train_agent.py` and select a training mode!

*Last Updated: 2025-10-22*
*Training System Version: 1.0.0*
```
