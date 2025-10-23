# 3D Printer Maintenance Agent

A specialized Claude AI agent focused on diagnosing, troubleshooting, and repairing Ender 3 and related FDM 3D printers. This agent provides expert-level guidance for maintenance, problem diagnosis, and step-by-step repair instructions.

## Quick Start

**First time here?** See **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for complete setup instructions!

**Fast setup:**
```bash
# Clone the repository
git clone https://github.com/lethal350/leashnet-pipedrive-webhook.git
cd leashnet-pipedrive-webhook

# Run the quick start script
python3 quick_start.py
```

The script will:
- Check Python version and dependencies
- Help you configure your API key
- Run a test query
- Launch the interactive CLI

## What You Get

**An AI expert with 1,700+ lines of specialized knowledge:**
- Complete hotend repair (disassembly, component replacement, troubleshooting)
- CoreXY conversion guide (2 Ender 3s → CoreXY for $200-350)
- Hardware diagnostics for Cartesian, CoreXY, and IDEX systems
- Virtual training environment (practice on simulated printers)
- 12 real-world problem scenarios from the community
- **🧠 NEW: Persistent Memory System** - Agent remembers past solutions and references them automatically!

## Features

- **Intelligent Problem Diagnosis**: Analyzes symptoms to identify root causes with multiple potential solutions ranked by likelihood
- **Multi-Architecture Support**:
  - **Cartesian Printers**: Ender 3, 3 Pro, 3 V2, CR-10 series (Primary expertise)
  - **CoreXY Printers**: Voron, Hypercube, BLV MGN (Advanced knowledge)
  - **IDEX Systems**: Dual extruder calibration and multi-material printing
- **Step-by-Step Repair Guidance**: Clear, detailed instructions tailored to user's technical level
- **Common Issues Covered**:
  - Under-extrusion and over-extrusion
  - Bed adhesion problems
  - Layer shifting and print quality issues
  - Nozzle clogs and hotend problems
  - Stringing, warping, and artifacts
  - Calibration (bed leveling, e-steps, PID tuning)
  - Mechanical and electrical troubleshooting
  - Firmware configuration
- **Hardware-Specific Diagnostics**:
  - V-slot wheel and eccentric nut adjustment
  - Belt tensioning (Cartesian and CoreXY-specific)
  - Stepper motor and driver diagnosis
  - Power supply and mainboard troubleshooting
  - BLTouch/CR Touch sensor problems
  - Heat creep and PTFE degradation
  - IDEX tool offset calibration

- **Maintenance Schedules**: Preventive maintenance recommendations to avoid common issues
- **Hardware Upgrade Guidance**:
  - Priority-based upgrade paths (reliability → quality → speed)
  - Budget-conscious recommendations by use case
  - Specific product recommendations with pros/cons
  - When to upgrade (and when NOT to)
- **Dual Z-Axis Conversion**:
  - Complete step-by-step installation guide
  - 3 approaches compared (single driver, dual driver, belt-driven)
  - Firmware configuration (Marlin & Klipper)
  - Troubleshooting common issues
- **Conversation History**: Export and load diagnostic sessions for documentation

## Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lethal350/leashnet-pipedrive-webhook.git
cd leashnet-pipedrive-webhook
```

### 2. Set Up Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Or export it directly:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

### Interactive CLI Mode (Recommended)

The easiest way to use the agent is through the interactive CLI:

```bash
python cli.py
```

#### Available Commands:

- `diagnose` or `d` - Start a new diagnostic session
- `continue` or `c` - Continue current conversation
- `maintenance` or `m` - Get maintenance schedule
- `upgrades` or `u` - Get upgrade recommendations
- `reset` or `r` - Reset conversation and start fresh
- `export` or `e` - Export conversation to JSON file
- `help` or `h` - Show help message
- `quit` or `exit` - Exit the program

#### Example Session:

```
Command: diagnose
Problem description: My prints have gaps between the layers

Printer model (e.g., Ender 3 Pro): Ender 3 Pro
Filament type (e.g., PLA): PLA
Nozzle temperature (e.g., 200): 200
Bed temperature (e.g., 60): 60

[Agent provides diagnosis and solutions]

Command: continue
Your message: How do I calibrate e-steps?

[Agent provides step-by-step e-steps calibration]

Command: export
Filename: my_diagnosis_2024.json
✓ Conversation exported to my_diagnosis_2024.json
```

### Python API Usage

You can also use the agent programmatically in your own Python scripts:

```python
from agents.printer_maintenance_agent import PrinterMaintenanceAgent

# Initialize the agent
agent = PrinterMaintenanceAgent()

# Diagnose a problem
response = agent.diagnose(
    user_query="My prints have gaps between layers and look weak",
    context={
        "printer_model": "Ender 3 Pro",
        "filament": "PLA",
        "nozzle_temp": "200°C",
        "bed_temp": "60°C"
    }
)

print(response)

# Continue the conversation
followup = agent.continue_conversation(
    "I'm a beginner. Can you explain how to do a cold pull?"
)

print(followup)

# Export conversation history
agent.export_conversation("diagnostic_session.json")

# Reset for new session
agent.reset_conversation()

# Get maintenance schedule
maintenance = agent.get_maintenance_schedule()
print(maintenance)

# Get upgrade recommendations
upgrades = agent.get_upgrade_recommendations(use_case="print quality")
print(upgrades)
```

### Running the Example Script

The main agent file includes example usage:

```bash
python agents/printer_maintenance_agent.py
```

This will run through several example scenarios:
1. Diagnosing under-extrusion
2. Follow-up question about cold pulls
3. Getting a maintenance schedule

## Project Structure

```
leashnet-pipedrive-webhook/
├── agents/
│   ├── __init__.py                      # Package initialization
│   └── printer_maintenance_agent.py     # Main agent implementation (1125 lines)
├── training/                             # Virtual training environment
│   ├── __init__.py                      # Training package init
│   ├── virtual_printer.py               # Printer simulator with realistic physics
│   ├── train_agent.py                   # Training orchestrator
│   ├── scenario_database.py             # Real-world scenario database (12 scenarios)
│   └── README.md                        # Training system documentation
├── cli.py                                # Interactive CLI interface
├── requirements.txt                      # Python dependencies
├── .env.example                          # Environment variables template
├── .gitignore                            # Git ignore rules
├── README.md                             # This file
├── HARDWARE_DIAGNOSTICS.md              # Hardware diagnostic capabilities documentation
└── UPGRADE_GUIDE.md                     # Complete hardware upgrade and dual Z-axis guide
```

## Agent Capabilities

### Diagnostic Approach

The agent uses a systematic diagnostic process:

1. **Symptom Analysis**: Understands the described problem
2. **Root Cause Identification**: Identifies most likely causes
3. **Multiple Solutions**: Provides ranked solutions by likelihood
4. **User-Appropriate Instructions**: Adapts communication to user's skill level
5. **Follow-up Support**: Answers questions and guides through repairs

### Common Problems Handled

| Problem | Symptoms | Example Causes |
|---------|----------|----------------|
| **Under-Extrusion** | Thin layers, gaps, weak prints | Clogged nozzle, wrong e-steps, low temp |
| **Bed Adhesion** | First layer not sticking | Unlevel bed, wrong Z-offset, dirty surface |
| **Layer Shifting** | Offset layers, skewed prints | Loose belts, loose pulleys, speed too high |
| **Layer Shifting (CoreXY)** | **Diagonal** shifts/skew | Unequal belt tension, belt desync |
| **Stringing** | Thin strings between parts | Poor retraction, temp too high, wet filament |
| **Clogs** | No extrusion, clicking | Partial clog, heat creep, debris |
| **Quality Issues** | Blobs, zits, ringing, VFAs | Speed/accel settings, mechanical issues |
| **Binding/Grinding** | Resistance, noise when moving | Over-tightened eccentric nuts, worn wheels |
| **Power Issues** | No power or intermittent | Failed PSU, blown fuse, mainboard voltage regulator |
| **Sensor Failures** | BLTouch won't deploy/trigger | Wiring (C7 capacitor), firmware config, pin stuck |
| **Heat Creep** | Clogs above melt zone | Insufficient cooling, all-metal hotend issues |
| **IDEX Misalignment** | Dual colors don't line up | Tool offset miscalibration, thermal expansion |

### Calibration Procedures

The agent can guide you through:

- **Bed Leveling**: Manual paper test, mesh leveling, auto bed leveling setup
- **E-Steps Calibration**: Ensuring accurate extrusion amounts
- **Flow Rate**: Fine-tuning extrusion multiplier
- **PID Tuning**: Stable temperature control
- **Retraction Settings**: Eliminating stringing and oozing
- **Acceleration/Jerk**: Improving print quality and speed
- **IDEX Tool Offsets**: X, Y, Z calibration for dual extruders
- **Belt Tension**: Frequency measurement (110Hz Cartesian, equal tension CoreXY)

### Hardware Diagnostic Capabilities

The agent provides expert-level hardware troubleshooting:

**Mechanical Systems:**
- V-slot wheel adjustment and eccentric nut tensioning
- Belt tension diagnosis (including CoreXY dual-belt synchronization)
- Binding and grinding noise troubleshooting
- Axis wobble and loose component identification

**Electrical Systems:**
- Power supply voltage testing and fuse diagnosis
- Mainboard failure detection (voltage regulator, driver failures)
- Stepper motor testing and driver current (Vref) adjustment
- Wiring and connector troubleshooting

**Sensor Systems:**
- BLTouch/CR Touch installation and firmware configuration
- C7 capacitor interference diagnosis on Creality boards
- Signal inversion issues and pin configuration
- Endstop and probe mounting problems

**Thermal Systems:**
- Heat creep diagnosis and cooling solutions
- PTFE tube degradation detection (temperature limits, toxic fume warnings)
- All-metal hotend configuration and heat break selection
- Hotend assembly and PTFE-to-nozzle gap problems

**CoreXY-Specific:**
- Diagonal layer shift diagnosis (belt desync)
- Belt frequency matching (within 1-2Hz)
- VFA (Vertical Fine Artifact) troubleshooting
- Belt routing and motor synchronization verification

**IDEX-Specific:**
- Three-axis tool offset calibration (X, Y, Z)
- Carriage collision prevention
- Ooze and stringing management with standby temperatures
- Mechanical alignment and thermal expansion compensation

### Safety Features

The agent always includes appropriate safety warnings for:
- Hot components (200-260°C)
- Electrical hazards (PSU, mainboard work)
- Moving parts
- Firmware modifications
- PTFE toxic fume risks above 250°C

## Advanced Usage

### Conversation Management

```python
# Export a diagnostic session for documentation
agent.export_conversation("session_2024_01_15.json")

# Load a previous session to continue later
agent.load_conversation("session_2024_01_15.json")

# Reset conversation for a new issue
agent.reset_conversation()
```

### Custom Context

Provide detailed context for better diagnosis:

```python
context = {
    "printer_model": "Ender 3 V2",
    "firmware": "Marlin 2.0.9.3",
    "filament": "eSUN PLA+",
    "nozzle_size": "0.4mm",
    "nozzle_temp": "215°C",
    "bed_temp": "65°C",
    "print_speed": "50mm/s",
    "retraction": "6mm @ 45mm/s",
    "previous_attempts": "Tried releveling bed, cleaned nozzle"
}

response = agent.diagnose("Prints have elephant's foot", context=context)
```

## Troubleshooting

### API Key Issues

If you get `ValueError: ANTHROPIC_API_KEY must be set`:

```bash
# Set temporarily (current session only)
export ANTHROPIC_API_KEY='your-api-key-here'

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Import Errors

If you get import errors, ensure you're in the correct directory and virtual environment:

```bash
cd /path/to/leashnet-pipedrive-webhook
source venv/bin/activate
pip install -r requirements.txt
```

### Rich CLI Not Available

The interactive CLI uses the `rich` library for enhanced formatting. If not installed, it will fall back to basic text output. To get the full experience:

```bash
pip install rich
```

## Dependencies

Core dependencies:
- `anthropic` - Claude API client
- `python-dotenv` - Environment variable management

Optional dependencies for enhanced features:
- `rich` - Enhanced CLI interface with colors and formatting
- `flask` - For building web interfaces
- `click` - For advanced CLI features

## Examples

### Example 1: Quick Diagnosis

```bash
$ python cli.py
Command: d
Problem description: First layer not sticking to bed
Printer model: Ender 3
Filament type: PLA
Nozzle temperature: 200
Bed temperature: 60

[Agent analyzes and provides diagnosis with multiple potential causes]
```

### Example 2: Maintenance Schedule

```bash
$ python cli.py
Command: m

[Agent provides comprehensive daily, weekly, monthly maintenance tasks]
```

### Example 3: Upgrade Advice

```bash
$ python cli.py
Command: u
Use case: reliability

[Agent recommends cost-effective reliability upgrades]
```

## Contributing

Contributions are welcome! Areas for improvement:
- Additional printer models and configurations
- Web interface for easier access
- Integration with Pipedrive webhooks for support ticketing
- Knowledge base expansion for exotic materials
- Klipper-specific guidance

## License

This project is provided as-is for educational and practical use in 3D printer maintenance.

## Support

For issues, questions, or suggestions:
1. Open an issue in the GitHub repository
2. Provide detailed information about your problem
3. Include conversation history exports if relevant

## Acknowledgments

- Built with [Claude](https://anthropic.com/claude) by Anthropic
- Knowledge based on Teaching Tech, Ender 3 community, and r/3Dprinting resources
- Inspired by the need for accessible, expert-level 3D printing support

## Roadmap

Planned features:
- [x] Web interface with Flask
- [x] Multi-language support
- [x] Image analysis for visual diagnostics
- [ ] Firmware configuration generator
- [ ] Print failure prediction
- [ ] Integration with OctoPrint/Klipper logs
- [ ] Video tutorial links for complex procedures
- [ ] Community knowledge base contributions
- [x] **Virtual Training Environment** - Agent can practice with thousands of scenarios

## Virtual Training Environment

The agent includes a comprehensive training system where it can practice diagnosing and solving thousands of realistic 3D printer problems through simulation.

### Features

- **Realistic Printer Simulation**: Virtual printers with accurate physics and component wear
- **Scenario Generation**: Automatic creation of diverse troubleshooting scenarios
- **Performance Evaluation**: Automated scoring across 4 categories (100-point scale)
- **Real-World Database**: 12 curated scenarios from actual community reports
- **Progressive Training**: Easy → Medium → Hard difficulty progression
- **Analytics Dashboard**: Detailed performance metrics and improvement tracking

### Quick Start

```bash
# Run training session
python training/train_agent.py

# Training modes:
# 1. Single Scenario - Interactive walkthrough
# 2. Small Batch - 10 scenarios (~15 minutes)
# 3. Progressive Training - Structured learning path
# 4. Stress Test - 100+ scenarios for comprehensive evaluation
```

### Training Results

The agent is evaluated on:
- **Problem Identification** (40 pts): Correctly identifying all issues
- **Root Cause Analysis** (30 pts): Finding root causes, not just symptoms
- **Solution Quality** (20 pts): Providing comprehensive repair steps
- **Communication** (10 pts): Clear, helpful, user-friendly responses

**Grades**: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)

**Target**: 200-300 scenarios with 85+ average for production readiness

See `training/README.md` for complete documentation.

---

Happy Printing! 🖨️
