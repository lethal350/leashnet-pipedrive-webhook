# 3D Printer Maintenance Agent - Setup Guide

A complete guide to getting your AI-powered 3D printer maintenance assistant running on your computer.

---

## What You're Getting

An AI agent with expert knowledge in:
- 3D printer maintenance and repair (Ender 3, CoreXY, IDEX)
- Hotend repair and troubleshooting (complete disassembly/reassembly)
- Hardware diagnostics and upgrades
- CoreXY conversions from 2 Ender 3 printers
- Virtual training environment for practice scenarios

---

## Prerequisites

### 1. Python Installation

**Check if you have Python**:
```bash
python --version
# or
python3 --version
```

**Need Python 3.8 or higher**. If you don't have it:

**Windows**:
- Download from https://python.org/downloads/
- During install: CHECK "Add Python to PATH"

**Mac**:
```bash
brew install python3
```

**Linux** (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Anthropic API Key

You need an API key from Anthropic to use Claude:

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)
6. **IMPORTANT**: Keep this secret! Don't share it.

**Pricing** (as of 2025):
- Claude 3.5 Sonnet: ~$3 per million input tokens
- Typical diagnostic conversation: $0.02 - $0.10
- You get free credits when you sign up

---

## Installation Steps

### Step 1: Clone the Repository

**Open a terminal/command prompt** and run:

```bash
# Clone from GitHub
git clone https://github.com/lethal350/leashnet-pipedrive-webhook.git

# Navigate into the directory
cd leashnet-pipedrive-webhook
```

**Don't have git?**
- Download ZIP from GitHub: Click "Code" → "Download ZIP"
- Extract the ZIP file
- Open terminal in that folder

### Step 2: Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt

# Or if that doesn't work, try:
pip3 install -r requirements.txt
```

This installs:
- `anthropic` - Claude API client
- `flask` - Web framework (for future features)
- `rich` - Pretty terminal output
- `python-dotenv` - Environment variable management

### Step 3: Configure API Key

**Option A: Using .env file** (Recommended):

1. Copy the example file:
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

2. Edit `.env` file with any text editor:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
AGENT_MODEL=claude-3-5-sonnet-20241022
```

3. Replace `sk-ant-your-actual-key-here` with your real API key

**Option B: Environment variable** (Temporary):

**Windows (PowerShell)**:
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
```

**Mac/Linux**:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
```

---

## Running the Agent

### Method 1: Interactive CLI (Recommended)

```bash
python cli.py
```

You'll see a menu:
```
=== 3D Printer Maintenance Agent ===

Choose an option:
1. Diagnose a problem
2. Continue conversation
3. Get maintenance schedule
4. Ask about upgrades
5. Reset conversation
6. Export conversation
7. Exit
```

**Example Session**:
```
Your choice: 1

Describe your printer problem: My prints are coming out as parallelograms instead of squares

[Agent analyzes and responds with diagnosis]

Would you like to continue this conversation? (yes/no): yes

Follow-up question: How do I measure belt tension?

[Agent explains belt tensioning procedure]
```

### Method 2: Python Script

Create a file `test_agent.py`:

```python
from agents.printer_maintenance_agent import PrinterMaintenanceAgent

# Initialize agent
agent = PrinterMaintenanceAgent()

# Ask a question
response = agent.diagnose(
    "My Ender 3 hotend keeps clogging after 15 minutes of printing. "
    "The heat sink fan is running. What could be wrong?"
)

print(response)
```

Run it:
```bash
python test_agent.py
```

### Method 3: Direct Import

```python
from agents.printer_maintenance_agent import PrinterMaintenanceAgent

agent = PrinterMaintenanceAgent()

# Diagnose a problem
result = agent.diagnose("Under-extrusion on my Ender 3 Pro")
print(result)

# Continue the conversation
followup = agent.continue_conversation("Could it be a clogged nozzle?")
print(followup)

# Get maintenance schedule
schedule = agent.get_maintenance_schedule()
print(schedule)

# Ask about upgrades
upgrades = agent.suggest_upgrades("I want to print faster")
print(upgrades)
```

---

## Using the Training Environment

Train your agent on thousands of virtual scenarios:

```bash
cd training
python train_agent.py
```

**Training Menu**:
```
=== Agent Training System ===

Choose training mode:
1. Single scenario (quick test)
2. Small batch (10 scenarios)
3. Medium batch (50 scenarios)
4. Large batch (100 scenarios)
5. Progressive training (10 → 50 → 100)
6. Stress test (real-world scenarios)
7. View training statistics
8. Exit
```

**What it does**:
- Creates virtual 3D printers with random problems
- Agent diagnoses the issue
- System evaluates agent's accuracy
- Provides detailed feedback and scoring

**Example Output**:
```
Scenario: Ender 3 with heat creep issue
Agent Score: 87/100
- Problem Identification: 38/40 ✓
- Root Cause Analysis: 27/30 ✓
- Solution Quality: 17/20 ✓
- Communication: 5/10 (could be clearer)

Training Progress: 23/50 scenarios completed
Average Score: 84.2/100
```

---

## Quick Reference Commands

### Basic Diagnostics

```python
from agents.printer_maintenance_agent import PrinterMaintenanceAgent

agent = PrinterMaintenanceAgent()

# Common issues
agent.diagnose("First layer won't stick to bed")
agent.diagnose("Layer shifting on Y axis")
agent.diagnose("Temperature reading shows 999°C")
agent.diagnose("Prints are stringy and messy")
agent.diagnose("How do I convert 2 Ender 3s to CoreXY?")
agent.diagnose("Hotend clogging, how do I disassemble?")
```

### Maintenance & Upgrades

```python
# Get maintenance schedule
agent.get_maintenance_schedule()

# Upgrade recommendations
agent.suggest_upgrades("speed printing")
agent.suggest_upgrades("high temperature materials")
agent.suggest_upgrades("print quality on a budget")
```

### Conversation Management

```python
# Continue existing conversation
agent.continue_conversation("What if that doesn't work?")

# Reset for new problem
agent.reset_conversation()

# Export conversation history
history = agent.export_conversation()
print(history)
```

---

## Features Overview

### 1. Problem Diagnosis

Ask about ANY 3D printer problem:
- "Why are my prints warping?"
- "Temperature won't reach 200°C"
- "BLTouch keeps flashing red"
- "Dual Z-axis motors not synchronized"

Agent provides:
- Multiple potential causes (ranked by likelihood)
- Step-by-step diagnostic procedures
- Detailed repair instructions
- Safety warnings

### 2. CoreXY Conversion Guide

Get help converting 2 Ender 3 printers to CoreXY:
- Complete parts list and costs
- Belt tensioning procedures (within 2 Hz)
- Firmware configuration (Marlin & Klipper)
- Troubleshooting parallelogram prints

### 3. Hotend Repair Expert

Complete hotend knowledge:
- Step-by-step disassembly (10 steps)
- Component replacement (thermistor, heater, nozzle)
- Clog diagnosis (nozzle vs heat break vs cold end)
- PID tuning procedures
- Hotend-specific guides (MK8, V6, Microswiss, Volcano)

### 4. Hardware Upgrades

Get prioritized upgrade recommendations:
- Budget-based suggestions ($50, $200, $500)
- Use-case specific (speed, quality, high-temp)
- Dual Z-axis conversion (3 approaches)
- All-metal hotend upgrades

### 5. Training Environment

Practice with virtual printers:
- 12 real-world scenarios from community
- Automatic scenario generation
- 100-point evaluation system
- Performance tracking

---

## Troubleshooting Setup Issues

### "ModuleNotFoundError: No module named 'anthropic'"

```bash
pip install anthropic python-dotenv rich flask
```

### "API key not found"

Make sure `.env` file exists and contains:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

Or set environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

### "Permission denied" on Mac/Linux

```bash
chmod +x cli.py
python3 cli.py
```

### Import errors

Make sure you're in the project directory:
```bash
cd leashnet-pipedrive-webhook
python cli.py
```

### "Rich" formatting issues in Windows

If you see weird characters, the agent will automatically fall back to plain text.

---

## Cost Estimation

**Typical Usage Costs** (Claude 3.5 Sonnet):

| Task | Tokens | Cost |
|------|--------|------|
| Simple diagnosis | 2,000 | $0.006 |
| Complex troubleshooting | 5,000 | $0.015 |
| CoreXY conversion help | 8,000 | $0.024 |
| Hotend disassembly guide | 4,000 | $0.012 |
| Training (10 scenarios) | 20,000 | $0.060 |

**Monthly estimates**:
- Light use (10 questions/month): ~$0.50
- Medium use (50 questions/month): ~$2.50
- Heavy use (200 questions/month): ~$10.00

**Free tier**: Most Anthropic accounts include free credits to start.

---

## Example Workflows

### Workflow 1: Diagnosing a Clog

```bash
python cli.py
# Choose: 1 (Diagnose a problem)
# Input: "My Ender 3 stopped extruding mid-print, clicking noise from extruder"

# Agent will ask diagnostic questions:
# - Is the hotend hot?
# - Can you push filament manually?
# - Is the heat sink fan running?

# Then provide diagnosis and fix steps
```

### Workflow 2: Planning a CoreXY Build

```bash
python cli.py
# Choose: 1 (Diagnose a problem)
# Input: "I want to convert 2 Ender 3 printers to CoreXY using the Duender project"

# Agent provides:
# - Complete parts list with costs
# - Frame assembly instructions
# - Belt routing and tensioning (90-98 Hz, within 2 Hz)
# - Firmware configuration
```

### Workflow 3: Learning Hotend Repair

```bash
python cli.py
# Choose: 1
# Input: "How do I completely disassemble my Ender 3 hotend to replace the thermistor?"

# Agent provides:
# - Safety warnings
# - Tool list
# - 10-step disassembly procedure
# - Thermistor replacement steps
# - Reassembly with hot-tightening technique
```

### Workflow 4: Training the Agent

```bash
cd training
python train_agent.py
# Choose: 3 (Medium batch - 50 scenarios)

# Watch as agent practices:
# - Diagnosing under-extrusion
# - Troubleshooting layer shifts
# - Fixing thermal runaway
# - Solving heat creep issues

# Review performance:
# - Average score: 85/100
# - Strengths: Problem identification
# - Areas to improve: Solution detail
```

---

## File Structure

```
leashnet-pipedrive-webhook/
├── agents/
│   └── printer_maintenance_agent.py   # Main agent (1,700+ lines)
├── training/
│   ├── virtual_printer.py             # Virtual printer simulator
│   ├── train_agent.py                 # Training orchestrator
│   ├── scenario_database.py           # 12 real-world scenarios
│   └── README.md                      # Training documentation
├── cli.py                              # Interactive command-line interface
├── requirements.txt                    # Python dependencies
├── .env.example                        # API key template
├── README.md                           # Project overview
├── COREXY_CONVERSION.md               # CoreXY build guide
├── SETUP_GUIDE.md                     # This file
├── HARDWARE_DIAGNOSTICS.md            # Hardware diagnostics reference
└── UPGRADE_GUIDE.md                   # Upgrade priorities and guides
```

---

## Next Steps

1. **Start Simple**: Try `python cli.py` and ask a basic question
2. **Read Documentation**: Check out `COREXY_CONVERSION.md` and `UPGRADE_GUIDE.md`
3. **Practice Training**: Run some training scenarios to see how the agent learns
4. **Customize**: Modify `printer_maintenance_agent.py` to add your own knowledge
5. **Share**: Help others by contributing scenarios to the training database

---

## Getting Help

**Agent Issues**:
- Check API key is set correctly
- Verify internet connection (API requires internet)
- Review error messages carefully

**3D Printer Questions**:
- Just ask the agent! It has comprehensive knowledge
- Check the guide files (COREXY_CONVERSION.md, etc.)

**Want to Contribute**:
- Add new training scenarios to `training/scenario_database.py`
- Improve agent knowledge in `printer_maintenance_agent.py`
- Share your success stories and improvements

---

## What Makes This Agent Special

✅ **Expert Level Knowledge**: 1,700+ lines of curated expertise
✅ **Multiple Architectures**: Cartesian, CoreXY, IDEX
✅ **Complete Hotend Expertise**: Disassembly, repair, all components
✅ **CoreXY Conversion**: From 2 Ender 3s ($200-350 vs $1200+ new)
✅ **Training Environment**: Practice on virtual printers
✅ **Real-World Scenarios**: 12 curated community problems
✅ **Safety-Focused**: Includes warnings and proper procedures
✅ **Cost-Effective**: Anthropic API much cheaper than consultations

---

**You now have a personal 3D printer expert available 24/7!**

Happy printing! 🖨️
