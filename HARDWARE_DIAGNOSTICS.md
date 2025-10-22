# Hardware Diagnostics Enhancement Summary

## Overview
This document summarizes the comprehensive hardware diagnostic capabilities added to the 3D Printer Maintenance Agent based on extensive research into Ender 3, CoreXY, and IDEX printer systems.

## New Capabilities Added

### 1. Mechanical Hardware Diagnostics

#### V-Slot Wheels & Eccentric Nuts
- **Problem identification**: Binding, grinding noise, wobbling, uneven movement
- **Proper adjustment procedure**: Step-by-step tensioning guide
- **Over-tightening detection**: Specific symptoms and tests
- **Repair solutions**: Wheel replacement, bearing maintenance, cleaning procedures

**Key Diagnostic Tests:**
- Manual movement test (smooth with slight resistance)
- Visual inspection for flat spots and grooves
- Wobble test perpendicular to movement
- Rotation test for free wheel spinning

**Critical Insight**: If holding bed flat and spinning wheels moves the bed = TOO TIGHT

### 2. Belt System Diagnostics

#### Cartesian Printers (Ender 3)
- Belt tension measurement using pluck method (~110Hz target)
- Pulley set screw verification
- Visual inspection for damage
- Tensioning procedure with verification steps

#### CoreXY Printers (ADVANCED)
- **Critical Difference**: TWO separate belts requiring EQUAL tension
- **Distinctive Symptom**: Diagonal layer shifts indicate CoreXY belt issues
- Belt frequency measurement with phone apps (Gates Carbon Drive, Sonic Tools)
- Target: Both belts within 1-2Hz of each other (100-140Hz range)
- Iterative adjustment process (one belt affects the other)
- Belt routing verification (X-formation crossing)
- VFA (Vertical Fine Artifacts) troubleshooting specific to longer belt paths

**Key Insight**: In CoreXY, diagonal artifacts = belt sync problems, NOT Z-wobble

### 3. Stepper Motor Failure Diagnosis

#### Diagnostic Process
- **Swap Test**: Most reliable method - move motor cable to different driver port
- Thermal testing (warm OK, too hot to touch = problem)
- Electrical resistance measurement (1-3 ohms between coil pairs)
- Visual inspection for loose pulleys, damaged wiring

#### Common Failure Modes
- Overheating drivers → add cooling, reduce Vref
- Loose pulley set screws → blue Loctite on motor shaft flat
- Extruder motor most common failure (runs more than other motors)

#### Vref Adjustment
- Ender 3 typical values: X/Y = 0.7-0.9V, Z = 0.7-0.9V, E = 0.9-1.1V
- Too low: skipping steps, insufficient torque
- Too high: overheating motors and drivers

### 4. Power Supply & Mainboard Diagnostics

#### PSU Failure Symptoms
- No power (LCD dark, no lights)
- Intermittent power loss
- Needs USB + PSU to function = voltage regulator blown
- Clicking/buzzing sounds
- Burning smell

#### Diagnostic Steps
1. **LED Check**: Green LED on PSU should be lit
2. **Multimeter Test**: 24V for Ender 3/V2, 12V for older models
3. **Fuse Check**: Glass fuse on input (unplug first!)
4. **USB Test**: If LCD powers on USB only = mainboard OK, PSU bad
5. **Fan Test**: PSU fan should spin when powered

#### Common Issues
- Blown fuse (often voltage switch wrong: 115V vs 230V)
- Failed capacitors (bulging or leaking)
- Fan failure causing overheating
- Voltage regulator failure on mainboard

#### Mainboard Diagnostics
- Swap motor cables to identify bad drivers
- Measure heater resistance (~1-2Ω for 24V heaters)
- Check thermistor (should be ~100kΩ at 25°C for 100k thermistors)
- Visual inspection for burnt components, scorch marks

### 5. Auto Bed Leveling Sensor Problems

#### BLTouch/CR Touch Common Failures
- Sensor won't deploy (red flashing)
- Homing fails (nozzle crashes)
- Inconsistent readings
- "Failed to verify sensor state" error

#### Critical Wiring Issue
**Creality boards have C7 capacitor on Z-endstop that interferes with probe signal**

**Solutions:**
- Remove C7 capacitor (requires soldering)
- Use 5-pin probe wiring instead
- Upgrade to board without capacitor (SKR, Creality 4.2.7)

#### Firmware Configuration Errors
- Z-endstop still enabled (must disable for probe)
- `Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN` not commented out
- `USE_ZMIN_PLUG` not disabled for 5-pin probes
- Wrong pin definitions

#### Signal Inversion
- If Z-axis drops into bed: Swap black/white wires OR invert in firmware
- Klipper: Change `sensor_pin: PC14` to `sensor_pin: ^PC14`
- Marlin: Check `Z_MIN_PROBE_ENDSTOP_INVERTING`

### 6. Hotend Heat Creep & PTFE Degradation

#### Heat Creep Symptoms
- Clogs forming above melt zone
- Extruder clicking but nozzle clear
- Soft filament in cold end
- Extruder motor hot to touch

#### Root Causes
- Insufficient heat break cooling
- Heat sink fan not running/blocked
- All-metal hotend without adequate cooling
- Printing too slow (heat soaks upward)

#### PTFE Temperature Limits (CRITICAL SAFETY)
- **Safe**: Up to 240°C
- **Caution**: 240-250°C (short term only)
- **DANGER**: 250°C+ releases toxic fumes, degrades PTFE

#### PTFE Degradation Symptoms
- Under-extrusion at higher temps
- Brown discoloration in PTFE
- Chemical smell when heating
- Clogs at PTFE/nozzle junction

#### PTFE Tube Gap Problem
- Filament leaks between tube and nozzle
- Fix: Hotend disassembly, reseat tube FLUSH to nozzle
- Prevention: Capricorn tubing (higher temp rating)

#### All-Metal Hotend Considerations
**Pros**: High-temp materials (ABS, Nylon, PC), no PTFE degradation
**Cons**: More prone to heat creep with PLA

**Solutions:**
- Upgrade heat sink fan (5000+ RPM)
- Reduce retraction distance
- Increase print speed slightly
- Bi-metal heat break for better thermal isolation

### 7. Dual Extruder / IDEX Specific Issues

#### Calibration Complexity
Unlike single extruder, requires THREE-dimensional calibration:
1. **X-Axis Offset**: Horizontal distance between nozzles
2. **Y-Axis Offset**: Front-to-back alignment
3. **Z-Axis Offset**: Height difference between nozzles

#### Misalignment Symptoms
- Dual-color prints don't line up
- Gaps or overlaps at color transitions
- Second nozzle dragging through first's work
- Poor layer adhesion in dual-material prints
- Random offset changes between prints

#### Calibration Process
1. Home both carriages
2. **Heat both nozzles to printing temp** (thermal expansion critical!)
3. Print calibration pattern with both extruders
4. Measure offset in X, Y, Z with calipers
5. Update firmware tool offsets: `M218 T1 X[offset] Y[offset] Z[offset]`
6. Save to EEPROM: `M500`
7. Verify with test print
8. **REPEAT** - mechanical changes affect calibration

#### IDEX-Specific Mechanical Issues
- Carriage collision: verify X_MIN_POS and X_MAX_POS
- Belt tension unequal: each carriage has own belt
- Loose printed parts: ABS deforms, use PETG with high infill
- Electrical interference: use shielded cables for long runs

#### Ooze Management
- Standby temperature too high: lower by 20-30°C
- Nozzle wipe before tool change
- Prime tower for consistent starting point
- Ooze shield as physical barrier

## Research Sources

This enhancement was based on comprehensive research including:
- 3D Printing Stack Exchange community solutions
- Teaching Tech calibration methodologies
- Duet3D and Klipper firmware documentation
- CoreXY mechanism design principles (Mark Rehorst's research)
- IDEX printer optimization guides
- Belt tensioning standards (Gates Carbon Drive specs)
- Creality board hardware analysis
- Community troubleshooting forums

## Impact

The agent can now:
- Diagnose CoreXY-specific issues (diagonal shifts from belt desync)
- Guide IDEX users through complex three-axis calibration
- Identify PSU vs mainboard failures through systematic testing
- Solve BLTouch/CR Touch problems with firmware and wiring specifics
- Warn about PTFE safety risks with temperature-specific guidance
- Distinguish between Cartesian and CoreXY diagnostic approaches
- Provide Vref adjustment guidance for stepper driver issues
- Explain eccentric nut adjustment with precise symptom identification

## Example Usage

```python
# CoreXY diagonal shift diagnosis
agent.diagnose(
    "My Voron 2.4 prints are shifting diagonally during fast movements",
    context={"printer_type": "CoreXY", "belt_tension": "unsure"}
)

# IDEX calibration assistance
agent.diagnose(
    "Dual color prints on my IDEX printer have a 0.5mm offset",
    context={"printer_type": "IDEX", "previous_calibration": "yes"}
)

# BLTouch installation issues
agent.diagnose(
    "BLTouch keeps flashing red and won't deploy on my Ender 3 with 1.1.5 board",
    context={"board": "Creality 1.1.5", "firmware": "Marlin"}
)
```

## Version History

- **v2.0.0** (Current): Added comprehensive hardware diagnostics for Cartesian, CoreXY, and IDEX systems
- **v1.0.0**: Initial release with basic Ender 3 troubleshooting

---

Generated: 2025-10-22
Agent: 3D Printer Maintenance Agent
