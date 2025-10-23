# CoreXY Conversion Guide: 2 Ender 3 to CoreXY

## Quick Overview

**What You're Building**: A CoreXY printer using parts from 2 Ender 3 printers
**Time Required**: 4-5 days (25-35 hours total)
**Additional Cost**: $200-350
**Performance Gain**: 2-3x faster printing with better quality

---

## Understanding CoreXY

**Key Difference**: Two stationary motors control XY motion through coordinated belt movements
- **X Movement**: Motors A & B rotate opposite directions
- **Y Movement**: Motors A & B rotate same direction
- **Result**: Lower moving mass = faster speeds, better quality

---

## The Duender Project

**Best option for 2 Ender 3 conversion**: Available on Printables.com

**What it provides**:
- Complete 3D printable parts
- Build volume: 235x235x250mm
- Uses crossed belt configuration
- Detailed assembly instructions

---

## Parts List

### From Your 2 Ender 3s (Keep)
- ✅ 2x XY stepper motors (become A & B motors)
- ✅ 2x Z motors, 1x extruder motor
- ✅ 1x mainboard (use best one, or upgrade)
- ✅ 1x PSU
- ✅ 1x heated bed
- ✅ 1x hotend assembly
- ✅ All endstops, thermistors, fans
- ✅ Hardware (screws, nuts, etc.)

### New Parts Needed

**Frame (Choose one)**:
- Budget: 2020 extrusion kit (~$60)
- **Recommended**: 2040 extrusion kit (~$120) - 4x more rigid

**Belt System** (~$50):
- 10 meters GT2 belt (6mm width)
- 8-12x GT2 20T pulleys (5mm bore)
- 8-12x 20T smooth idlers

**Linear Motion (Choose one)**:
- Reuse V-slot wheels: $0
- **Recommended**: MGN12 linear rails 400mm: ~$100

**Hardware** (~$20):
- M5 T-nuts and screws
- Corner brackets

**Optional Upgrades**:
- BTT SKR board ($40) - silent, modern features
- BLTouch ($35)

**Total**: $200-350 depending on choices

---

## Critical Success Factors

### 1. Belt Tension (MOST IMPORTANT)

**Must have**:
- Both belts 90-98 Hz frequency
- **Within 2 Hz of each other** (use phone app: "Gates Carbon Drive")

**Why it matters**: Unequal tension causes diagonal shifts and parallelograms

### 2. Frame Squareness

- All diagonals within 0.5mm of each other
- Use carpenter's square at every corner
- Take your time - this determines everything else

### 3. Motor Configuration

**Firmware must define**:
```cpp
#define COREXY  // In Marlin Configuration.h
```
or
```ini
kinematics: corexy  # In Klipper printer.cfg
```

**Wiring**:
- Ender 3 X motor → Mainboard X driver (A motor)
- Ender 3 Y motor → Mainboard Y driver (B motor)

---

## Assembly Steps

### Day 1: Frame (4 hours)
1. Build bottom 400x400mm rectangle
2. Build top rectangle (identical)
3. Add 4 vertical posts (500mm)
4. Square the frame (measure all diagonals)
5. Tighten everything

### Day 2: Motion System (4 hours)
1. Install linear rails or V-slot wheels
2. Mount X-gantry to Y-axis
3. Mount toolhead to X-gantry
4. Test smooth movement by hand

### Day 3: Belts & Electronics (6 hours)
1. Mount A & B motors to top frame
2. Install pulleys and idlers
3. Route belts (crossed or stacked)
4. Initial tensioning (finger-tight)
5. Wire electronics
6. Flash firmware

### Day 4: Calibration (4 hours)
1. Test motor directions
2. Fine-tune belt tension to 90-98 Hz
3. Match belts within 2 Hz
4. PID tune hotend and bed
5. Level bed / Z-offset

### Day 5: Testing (variable)
1. Print calibration cube
2. Adjust if needed
3. Test prints at increasing speeds

---

## Firmware Configuration

### Marlin

**Configuration.h changes**:
```cpp
#define COREXY  // Line ~90

// May need to invert motors after testing
#define INVERT_X_DIR false  // Adjust if needed
#define INVERT_Y_DIR true   // Adjust if needed

// Start conservative
#define DEFAULT_MAX_FEEDRATE { 300, 300, 5, 25 }  // mm/s
#define DEFAULT_MAX_ACCELERATION { 3000, 3000, 100, 5000 }  // mm/s²

// Update bed size
#define X_BED_SIZE 300
#define Y_BED_SIZE 300
```

### Klipper (Recommended)

**Advantages**: Better performance, input shaping, easier tuning

**Basic printer.cfg**:
```ini
[printer]
kinematics: corexy
max_velocity: 300
max_accel: 3000

[stepper_x]  # A motor
step_pin: PC2
dir_pin: PB9  # Add ! if wrong direction
rotation_distance: 40  # GT2 20T pulley
position_max: 300

[stepper_y]  # B motor
step_pin: PB8
dir_pin: PB7  # Add ! if wrong direction
rotation_distance: 40
position_max: 300
```

---

## Common Problems & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| **Prints as parallelogram** | Unequal belt tension | Match to within 2 Hz |
| **Diagonal shifting** | Loose pulley or belt | Tighten set screws, tension belts |
| **Layer shifts** | Belts too loose | Increase to 90+ Hz |
| **Motor stalling** | Belts too tight | Reduce below 98 Hz |
| **Wrong movement direction** | Firmware config | Invert dir_pin in firmware |
| **Ringing/ghosting** | Frame not rigid | Upgrade to 2040, add bracing |

---

## Belt Tensioning Procedure

**This is the #1 most important calibration**:

1. Download "Gates Carbon Drive" app (free)
2. Pluck Belt A, measure frequency (e.g., 92 Hz)
3. Pluck Belt B, measure frequency (e.g., 95 Hz)
4. Calculate difference: 95 - 92 = 3 Hz (too much!)
5. Adjust tensioners until both 90-98 Hz AND within 2 Hz
6. Example good result: A=93Hz, B=94Hz ✓

**Test**: Print 20mm calibration cube
- Should be perfect square, not parallelogram
- All sides 20mm ± 0.1mm

---

## Performance Expectations

| Metric | Ender 3 | CoreXY Build |
|--------|---------|--------------|
| Print speed | 60 mm/s | 150-200 mm/s |
| Acceleration | 500 mm/s² | 3000-5000 mm/s² |
| Benchy time | 2h 15min | 45-60 min |
| Quality | Good | Excellent |

---

## Next Steps After Assembly

1. **First week**: Dial in belt tension perfectly
2. **First month**: Add input shaping (Klipper), build enclosure
3. **Long term**: Consider dual Z, direct drive, all-metal hotend

---

## Resources

- **Duender Project**: Printables.com (search "Duender CoreXY")
- **Teaching Tech**: Calibration website and YouTube
- **Klipper Docs**: klipper3d.org
- **Communities**: r/VORONDesign, r/ender3, Klipper Discord

---

## Key Takeaways

✅ **Take your time** - rushing causes mistakes
✅ **Belt tension matching is critical** - invest in phone app
✅ **Start slow** - increase speeds gradually after tuning
✅ **Frame must be square** - everything depends on this
✅ **Ask for help** - communities are friendly

**Budget**: $200-350 vs $1200+ for new CoreXY kit
**Result**: Professional-grade CoreXY printer from your Ender 3s

Good luck with your build!
