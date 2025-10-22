# 3D Printer Maintenance Agent

A specialized Claude AI agent focused on diagnosing, troubleshooting, and repairing Ender 3 and related FDM 3D printers. This agent provides expert-level guidance for maintenance, problem diagnosis, and step-by-step repair instructions.

## Features

- **Intelligent Problem Diagnosis**: Analyzes symptoms to identify root causes with multiple potential solutions ranked by likelihood
- **Comprehensive Knowledge Base**: Deep expertise in Ender 3, Ender 3 Pro, Ender 3 V2, CR-10, and similar Cartesian FDM printers
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

- **Maintenance Schedules**: Preventive maintenance recommendations to avoid common issues
- **Upgrade Recommendations**: Cost-effective upgrade paths based on use case
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
│   └── printer_maintenance_agent.py     # Main agent implementation
├── cli.py                                # Interactive CLI interface
├── requirements.txt                      # Python dependencies
├── .env.example                          # Environment variables template
├── .gitignore                            # Git ignore rules
└── README.md                             # This file
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
| **Stringing** | Thin strings between parts | Poor retraction, temp too high, wet filament |
| **Clogs** | No extrusion, clicking | Partial clog, heat creep, debris |
| **Quality Issues** | Blobs, zits, ringing | Speed/accel settings, mechanical issues |

### Calibration Procedures

The agent can guide you through:

- **Bed Leveling**: Manual paper test, mesh leveling, auto bed leveling setup
- **E-Steps Calibration**: Ensuring accurate extrusion amounts
- **Flow Rate**: Fine-tuning extrusion multiplier
- **PID Tuning**: Stable temperature control
- **Retraction Settings**: Eliminating stringing and oozing
- **Acceleration/Jerk**: Improving print quality and speed

### Safety Features

The agent always includes appropriate safety warnings for:
- Hot components (200-260°C)
- Electrical hazards
- Moving parts
- Firmware modifications

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
- [ ] Web interface with Flask
- [ ] Multi-language support
- [ ] Image analysis for visual diagnostics
- [ ] Firmware configuration generator
- [ ] Print failure prediction
- [ ] Integration with OctoPrint/Klipper logs
- [ ] Video tutorial links for complex procedures
- [ ] Community knowledge base contributions

---

Happy Printing! 🖨️
