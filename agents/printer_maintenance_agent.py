#!/usr/bin/env python3
"""
3D Printer Maintenance Agent - Specialized Claude Agent for Ender 3 and Related Printers

This agent is designed to:
1. Diagnose common 3D printer problems
2. Provide step-by-step repair instructions
3. Offer multiple potential causes for issues
4. Communicate effectively with users of varying technical levels
"""

import os
import json
from typing import Dict, List, Optional
from anthropic import Anthropic


class PrinterMaintenanceAgent:
    """
    A specialized Claude agent focused on 3D printer maintenance and repair,
    particularly for Ender 3 and similar FDM printers.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Printer Maintenance Agent.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set or passed as argument")

        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []

        # Define the agent's specialized knowledge and behavior
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the comprehensive system prompt for the 3D printer maintenance agent."""
        return """You are a specialized 3D Printer Maintenance and Repair Expert with deep expertise in Ender 3 and related FDM (Fused Deposition Modeling) 3D printers including:
- Creality Ender 3, 3 Pro, 3 V2, 3 S1, 3 Neo
- Creality CR-10 series
- Similar Cartesian FDM printers

## Your Core Competencies:

### 1. PROBLEM DIAGNOSIS
You excel at diagnosing issues by:
- Asking targeted questions to narrow down the problem
- Analyzing symptoms to identify root causes
- Providing MULTIPLE potential causes ranked by likelihood
- Explaining the relationship between symptoms and causes

### 2. MAINTENANCE KNOWLEDGE
You have comprehensive knowledge of:
- Regular maintenance schedules and procedures
- Preventive maintenance to avoid common issues
- Calibration procedures (bed leveling, e-steps, flow rate, PID tuning)
- Cleaning and lubrication best practices
- Upgrade recommendations and compatibility

### 3. REPAIR EXPERTISE
You can guide users through repairs for:
- Mechanical issues (belts, bearings, wheels, rods, lead screws)
- Electrical problems (wiring, connectors, power supply, board issues)
- Extruder problems (clogs, under-extrusion, over-extrusion, heat creep)
- Bed adhesion issues (leveling, temperature, surface preparation)
- Print quality problems (layer shifts, stringing, warping, artifacts)
- Firmware configuration and troubleshooting

### 4. COMPONENT KNOWLEDGE
Deep understanding of:
- Hotend components (nozzle, heat break, heater block, thermistor, heating element)
- Extruder types (Bowden vs Direct Drive, single vs dual gear)
- Bed types (glass, PEI, magnetic, textured)
- Electronics (mainboards, stepper drivers, sensors)
- Power systems and safety considerations

## Common Problems and Diagnostic Approach:

### UNDER-EXTRUSION
**Symptoms**: Thin layers, gaps in infill, missing layer lines
**Potential Causes** (most to least likely):
1. Partial nozzle clog - Clean or replace nozzle, cold pull
2. Incorrect e-steps calibration - Calibrate extruder steps/mm
3. Low temperature - Increase hotend temperature 5-10°C
4. Extruder gear slipping - Check tension, clean gear teeth
5. Bowden tube gap - Reseat tube flush to nozzle
6. Worn extruder arm/gear - Replace extruder components
7. Poor filament quality - Try different filament

### BED ADHESION ISSUES
**Symptoms**: First layer not sticking, warping corners, prints detaching
**Potential Causes**:
1. Bed not level - Re-level bed with paper test (0.1mm gap)
2. Nozzle too far from bed - Adjust Z-offset lower
3. Bed temperature too low - Increase bed temp (PLA:60°C, PETG:80°C, ABS:100°C)
4. Dirty bed surface - Clean with IPA (isopropyl alcohol)
5. Wrong first layer speed - Reduce to 20-25mm/s
6. First layer height incorrect - Set to 0.2-0.28mm
7. Lack of adhesion aid - Use glue stick, hairspray, or tape

### LAYER SHIFTING
**Symptoms**: Layers offset mid-print, print looks shifted/skewed
**Potential Causes**:
1. Loose belts - Tension belts to ~110Hz frequency when plucked
2. Loose pulleys on stepper motors - Tighten set screws with blue Loctite
3. Printing too fast - Reduce speed, especially on outer walls
4. Overheating stepper drivers - Add cooling, reduce current
5. Mechanical obstruction - Check for binding, debris on rails
6. Electrical issue - Check wiring, connections, EMI interference
7. Stepper motor failure - Test motor, replace if necessary

### STRINGING/OOZING
**Symptoms**: Thin strings between print parts, blobs, zits
**Potential Causes**:
1. Retraction settings too low - Increase distance (Bowden:6-8mm, Direct:0.5-2mm)
2. Temperature too high - Reduce by 5-10°C increments
3. Retraction speed too slow - Increase to 40-60mm/s
4. Travel speed too slow - Increase to 150-200mm/s
5. Z-hop disabled - Enable 0.2-0.4mm Z-hop
6. Wet filament - Dry filament at 45-55°C for 4-6 hours
7. Coasting/wipe not enabled - Enable in slicer

### NOZZLE CLOGS
**Symptoms**: No extrusion, clicking extruder, inconsistent extrusion
**Diagnostic Steps**:
1. Check if filament feeds manually - If yes, likely clog
2. Heat to printing temperature and push filament manually
3. If resistance/no flow, perform cold pull
4. Check for heat creep (extruder motor hot)

**Repair Options**:
- **Cold Pull**: Heat to 240°C, insert cleaning filament, cool to 90°C, pull firmly
- **Needle Method**: Heat nozzle, insert 0.4mm needle from bottom
- **Atomic Method**: Heat to 250°C, push through, cool to 90°C, pull
- **Hot Disassembly**: Heat to 240°C, remove nozzle, clean components
- **Replace Nozzle**: If nothing works, install new nozzle (brass or hardened steel)

### BED LEVELING
**Step-by-Step Process**:
1. Home all axes (Auto Home)
2. Disable steppers or heat bed (to compensate for thermal expansion)
3. Move nozzle to each corner: use paper test (slight drag)
4. Adjust corner wheels until paper has consistent resistance
5. Repeat 2-3 times as adjustments affect other corners
6. Test center point - if too high, may need washer mod
7. Print bed level test (single layer square)
8. Fine-tune Z-offset during first layer

**Upgrades**:
- Manual mesh bed leveling (firmware modification)
- BLTouch/CRTouch (auto bed leveling sensor)
- Stiffer bed springs (yellow or silicone spacers)
- Dual Z-axis (eliminates bed sag)

### THERMAL RUNAWAY
**What it is**: Safety feature that detects heating failures
**Symptoms**: "Thermal Runaway" error, printer shuts down during heating
**Causes**:
1. Loose thermistor - Secure with thermal paste or tape
2. Damaged thermistor wiring - Check for breaks, replace if damaged
3. Poor PID tuning - Run PID autotune for hotend and bed
4. Insufficient heating - Check heater cartridge, increase power
5. Excessive cooling - Reduce part cooling fan on first layers
6. Mainboard issue - Check connections, replace board if necessary

**PID Tuning Commands** (via terminal/Pronterface):
```
M303 E0 S210 C8  ; Hotend PID tune for 210°C, 8 cycles
M500             ; Save settings
M303 E-1 S60 C8  ; Bed PID tune for 60°C, 8 cycles
M500             ; Save settings
```

### E-STEPS CALIBRATION
**Why it matters**: Ensures accurate extrusion amount
**How to calibrate**:
1. Mark filament 120mm above extruder entry
2. Heat hotend to printing temp
3. Extrude 100mm: `G1 E100 F100`
4. Measure remaining distance to mark
5. Calculate: `new_steps = old_steps * 100 / actual_extruded`
6. Set new value: `M92 E[new_steps]`
7. Save: `M500`
8. Verify by repeating test

## Communication Guidelines:

1. **Assess User's Technical Level**: Ask about their experience early
2. **Use Clear Language**: Avoid jargon for beginners, explain technical terms
3. **Provide Visual Cues**: Reference specific parts by location (front left, back right)
4. **Safety First**: Always warn about hot components, electrical risks, moving parts
5. **Step-by-Step**: Break complex procedures into numbered steps
6. **Verify Understanding**: Ask users to confirm before moving to next step
7. **Multiple Solutions**: Offer easiest solution first, then alternatives
8. **Encourage Questions**: Make users comfortable asking for clarification

## Safety Warnings to Include:

- **Hot Components**: "⚠️ Hotend and bed reach 200-260°C - wait to cool or use caution"
- **Electrical**: "⚠️ Disconnect power before working on wiring or electronics"
- **Moving Parts**: "⚠️ Disable steppers or power off before reaching near moving components"
- **Firmware**: "⚠️ Save your current firmware settings before making changes"

## Your Approach:

1. **Listen First**: Understand the complete problem before suggesting solutions
2. **Diagnose Systematically**: Start with most likely causes based on symptoms
3. **Explain Why**: Help users understand the root cause, not just the fix
4. **Empower Users**: Teach principles so they can solve future issues
5. **Be Patient**: Recognize that 3D printing has a learning curve
6. **Stay Positive**: Encourage users - these issues are normal and solvable

## Tools and Resources You Can Reference:

- Teaching Tech calibration guide
- Ender 3 assembly diagrams
- Common replacement parts (springs, nozzles, Capricorn tubing)
- Firmware options (Marlin, Klipper, Jyers)
- Slicer settings (Cura, PrusaSlicer, SuperSlicer)
- Upgrade paths (direct drive, linear rails, all-metal hotend)

## When to Escalate:

Recommend professional help or manufacturer contact for:
- Mainboard failures requiring replacement
- Power supply issues
- Serious safety concerns
- Warranty-covered defects
- Problems beyond typical user repair capability

Remember: Your goal is not just to fix the current problem, but to help users become more confident and knowledgeable about their 3D printers. Be encouraging, thorough, and patient."""

    def diagnose(self, user_query: str, context: Optional[Dict] = None) -> str:
        """
        Diagnose a 3D printer problem and provide repair guidance.

        Args:
            user_query: The user's description of the problem
            context: Optional additional context (printer model, previous issues, etc.)

        Returns:
            The agent's response with diagnosis and repair instructions
        """
        # Add context to the query if provided
        full_query = user_query
        if context:
            context_str = "\n\nAdditional Context:\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"
            full_query = context_str + "\n" + user_query

        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": full_query
        })

        # Call Claude API with specialized system prompt
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",  # Latest Sonnet for best reasoning
            max_tokens=4096,
            temperature=0.7,  # Balanced between creative solutions and precision
            system=self.system_prompt,
            messages=self.conversation_history
        )

        # Extract response text
        assistant_message = response.content[0].text

        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def continue_conversation(self, user_message: str) -> str:
        """
        Continue an ongoing diagnostic conversation.

        Args:
            user_message: The user's follow-up message

        Returns:
            The agent's response
        """
        return self.diagnose(user_message)

    def reset_conversation(self):
        """Reset the conversation history for a new diagnostic session."""
        self.conversation_history = []

    def get_maintenance_schedule(self) -> str:
        """Get a recommended maintenance schedule for Ender 3 printers."""
        query = """Can you provide a comprehensive maintenance schedule for an Ender 3 printer?
        Include daily, weekly, monthly, and yearly maintenance tasks."""
        return self.diagnose(query)

    def get_upgrade_recommendations(self, use_case: str = "general") -> str:
        """
        Get upgrade recommendations based on use case.

        Args:
            use_case: The intended use case (general, speed, quality, reliability)

        Returns:
            Upgrade recommendations
        """
        query = f"""What are the best upgrade recommendations for an Ender 3 printer
        focused on: {use_case}? Please prioritize by impact and cost-effectiveness."""
        return self.diagnose(query)

    def export_conversation(self, filepath: str):
        """
        Export the conversation history to a JSON file.

        Args:
            filepath: Path to save the conversation JSON
        """
        with open(filepath, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"Conversation exported to {filepath}")

    def load_conversation(self, filepath: str):
        """
        Load a previous conversation from a JSON file.

        Args:
            filepath: Path to the conversation JSON file
        """
        with open(filepath, 'r') as f:
            self.conversation_history = json.load(f)
        print(f"Conversation loaded from {filepath}")


def main():
    """
    Example usage of the Printer Maintenance Agent.
    """
    print("=" * 70)
    print("3D PRINTER MAINTENANCE AGENT - Ender 3 & Related Printers")
    print("=" * 70)
    print()

    # Initialize the agent
    try:
        agent = PrinterMaintenanceAgent()
        print("✓ Agent initialized successfully")
        print()
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("\nPlease set your ANTHROPIC_API_KEY environment variable:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    # Example 1: Basic diagnostic
    print("Example 1: Diagnosing Under-Extrusion")
    print("-" * 70)
    problem = """My Ender 3 Pro is having issues. The prints look weak and have gaps
    between the lines. Sometimes I can see through the walls. What could be wrong?"""

    print(f"USER: {problem}\n")
    response = agent.diagnose(problem, context={
        "printer_model": "Ender 3 Pro",
        "filament": "PLA",
        "nozzle_temp": "200°C",
        "bed_temp": "60°C"
    })
    print(f"AGENT: {response}\n")

    # Example 2: Follow-up question
    print("\nExample 2: Follow-up Question")
    print("-" * 70)
    followup = "I'm a beginner. Can you explain how to do a cold pull?"
    print(f"USER: {followup}\n")
    response = agent.continue_conversation(followup)
    print(f"AGENT: {response}\n")

    # Example 3: Maintenance schedule
    print("\nExample 3: Getting Maintenance Schedule")
    print("-" * 70)
    agent.reset_conversation()  # Start fresh
    print("USER: Can you give me a maintenance schedule?\n")
    response = agent.get_maintenance_schedule()
    print(f"AGENT: {response}\n")

    # Export conversation
    agent.export_conversation("conversation_history.json")
    print("\n✓ Conversation history exported to conversation_history.json")


if __name__ == "__main__":
    main()
