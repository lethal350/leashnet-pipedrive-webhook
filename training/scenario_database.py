#!/usr/bin/env python3
"""
Real-World Scenario Database

This module contains actual scenarios reported by the 3D printing community,
providing realistic training data based on real user experiences.
"""

from typing import List, Dict


class RealWorldScenarios:
    """
    Database of real-world scenarios from 3D printing community forums,
    support tickets, and documented cases.
    """

    @staticmethod
    def get_all_scenarios() -> List[Dict]:
        """Get all real-world scenarios"""
        return [
            # Scenario 1: Classic Under-Extrusion
            {
                "id": "REAL_001",
                "title": "Weak Layers and Gaps in Walls",
                "source": "r/ender3",
                "difficulty": "medium",
                "printer_type": "Ender 3 Pro",
                "user_description": """
                My prints are coming out really weak. I can see gaps between the
                perimeter lines and the infill is sparse. Sometimes the top layers
                are almost transparent. I'm using PLA at 200°C and 60°C bed. Been
                printing fine for 3 months until this week.
                """,
                "symptoms": [
                    "Gaps between perimeter lines",
                    "Sparse infill",
                    "Transparent top layers",
                    "Weak print strength"
                ],
                "actual_problems": [
                    {
                        "type": "under_extrusion",
                        "root_cause": "partial_clog",
                        "severity": "moderate"
                    }
                ],
                "solution_summary": "Perform cold pull, verify nozzle temp, calibrate e-steps",
                "lesson": "Progressive under-extrusion often indicates partial nozzle clog"
            },

            # Scenario 2: Layer Shift Mystery
            {
                "id": "REAL_002",
                "title": "Random Layer Shifts Mid-Print",
                "source": "Creality Support Ticket",
                "difficulty": "medium",
                "printer_type": "Ender 3",
                "user_description": """
                Help! My prints keep failing. About halfway through, the layers
                suddenly shift to the side and ruin everything. It's random - sometimes
                X direction, sometimes Y. Belts seem tight when I check them.
                """,
                "symptoms": [
                    "Sudden layer shifts mid-print",
                    "Shifts in random directions (X or Y)",
                    "Usually occurs mid-height",
                    "Belts appear normal"
                ],
                "actual_problems": [
                    {
                        "type": "layer_shift",
                        "root_cause": "loose_pulley",
                        "severity": "major",
                        "component": "stepper_pulley_x"
                    }
                ],
                "solution_summary": "Check and tighten all pulley set screws, use blue Loctite",
                "lesson": "Layer shifts with tight belts suggest loose pulleys on motor shafts"
            },

            # Scenario 3: First Layer Nightmare
            {
                "id": "REAL_003",
                "title": "Can't Get First Layer to Stick",
                "source": "r/3Dprinting",
                "difficulty": "easy",
                "printer_type": "Ender 3 V2",
                "user_description": """
                I'm a complete beginner and I can't get ANYTHING to stick to the bed.
                I've leveled it like 10 times. The filament just gets dragged around
                by the nozzle. Using the glass bed that came with it.
                """,
                "symptoms": [
                    "First layer not adhering",
                    "Filament dragged by nozzle",
                    "Print pops off immediately",
                    "Multiple leveling attempts failed"
                ],
                "actual_problems": [
                    {
                        "type": "bed_adhesion",
                        "root_cause": "z_offset_too_high",
                        "severity": "minor"
                    },
                    {
                        "type": "bed_adhesion",
                        "root_cause": "dirty_bed_surface",
                        "severity": "minor"
                    }
                ],
                "solution_summary": "Lower Z-offset, clean bed with IPA, use glue stick",
                "lesson": "Multiple causes can compound - Z-offset AND cleanliness both matter"
            },

            # Scenario 4: Thermal Runaway Terror
            {
                "id": "REAL_004",
                "title": "Thermal Runaway Error Keeps Appearing",
                "source": "Teaching Tech Discord",
                "difficulty": "hard",
                "printer_type": "Ender 3",
                "user_description": """
                My printer shuts down with "thermal runaway" error every time I try
                to print. Sometimes during heating, sometimes 10 minutes in. The
                temperature graph looks crazy - jumps up and down. I installed an
                all-metal hotend last week and it worked fine for 2 prints.
                """,
                "symptoms": [
                    "Thermal runaway error",
                    "Temperature fluctuations",
                    "Errors during heating or mid-print",
                    "Started after hotend upgrade"
                ],
                "actual_problems": [
                    {
                        "type": "thermal_runaway",
                        "root_cause": "loose_thermistor",
                        "severity": "critical",
                        "component": "thermistor_hotend"
                    },
                    {
                        "type": "thermal_runaway",
                        "root_cause": "missing_pid_tune",
                        "severity": "moderate"
                    }
                ],
                "solution_summary": "Secure thermistor with Kapton tape, run PID autotune",
                "lesson": "After hotend changes, ALWAYS run PID tune and verify thermistor mounting"
            },

            # Scenario 5: The Mystery Clog
            {
                "id": "REAL_005",
                "title": "Extruder Clicking, No Extrusion",
                "source": "All3DP Forums",
                "difficulty": "medium",
                "printer_type": "Ender 3 Pro",
                "user_description": """
                My extruder motor keeps clicking and barely any filament comes out.
                I've replaced the nozzle twice. The hotend is at 210°C. I can push
                filament through manually when cold, but not when hot. The extruder
                motor itself feels pretty warm.
                """,
                "symptoms": [
                    "Extruder motor clicking/skipping",
                    "Little to no extrusion",
                    "Can push filament when cold",
                    "Cannot push when hot",
                    "Extruder motor warm/hot"
                ],
                "actual_problems": [
                    {
                        "type": "heat_creep",
                        "root_cause": "failed_cooling_fan",
                        "severity": "major",
                        "component": "cooling_fan"
                    }
                ],
                "solution_summary": "Replace hotend cooling fan, check heat break",
                "lesson": "Heat creep causes clogs above the melt zone - check cooling system"
            },

            # Scenario 6: Stringing Madness
            {
                "id": "REAL_006",
                "title": "Excessive Stringing Between Parts",
                "source": "Prusa Forums",
                "difficulty": "easy",
                "printer_type": "Ender 3 V2",
                "user_description": """
                Every print comes out with tons of thin strings between all the parts.
                Looks like spider webs. I'm using PLA at 200°C. Retraction is set to
                6mm at 25mm/s (default Cura settings). The filament is brand new.
                """,
                "symptoms": [
                    "Thin strings between parts",
                    "Spider web appearance",
                    "Otherwise good print quality",
                    "Using default slicer settings"
                ],
                "actual_problems": [
                    {
                        "type": "stringing",
                        "root_cause": "temperature_too_high",
                        "severity": "minor"
                    },
                    {
                        "type": "stringing",
                        "root_cause": "retraction_speed_slow",
                        "severity": "minor"
                    }
                ],
                "solution_summary": "Lower temp to 190-195°C, increase retraction speed to 40-50mm/s",
                "lesson": "Stringing usually has multiple factors - temp AND retraction settings"
            },

            # Scenario 7: BLTouch Won't Deploy
            {
                "id": "REAL_007",
                "title": "BLTouch Red Light, Won't Deploy",
                "source": "r/ender3",
                "difficulty": "hard",
                "printer_type": "Ender 3 Pro",
                "user_description": """
                Just installed a BLTouch on my Ender 3 Pro with the 4.2.7 board.
                Followed a YouTube tutorial. When I power on, the BLTouch flashes red
                and the pin doesn't come down. When I try to home, the nozzle crashes
                into the bed. The wiring looks right to me. Running stock Creality firmware.
                """,
                "symptoms": [
                    "BLTouch flashing red LED",
                    "Pin not deploying",
                    "Homing causes bed crash",
                    "Recently installed",
                    "Stock firmware"
                ],
                "actual_problems": [
                    {
                        "type": "bltouch_failure",
                        "root_cause": "firmware_not_configured",
                        "severity": "major"
                    },
                    {
                        "type": "bltouch_failure",
                        "root_cause": "z_endstop_still_enabled",
                        "severity": "major"
                    }
                ],
                "solution_summary": "Flash BLTouch-compatible firmware, disable Z endstop in config",
                "lesson": "BLTouch requires firmware changes - can't just plug and play"
            },

            # Scenario 8: Z-Axis Binding
            {
                "id": "REAL_008",
                "title": "Z-Axis Moves Rough, Uneven Layers",
                "source": "Facebook 3D Printing Group",
                "difficulty": "medium",
                "printer_type": "Ender 3",
                "user_description": """
                The Z-axis feels really stiff when I move it by hand. Sometimes it
                binds completely. Prints have uneven layers and sometimes the nozzle
                seems to dig into lower layers. I just tightened all my eccentric nuts
                because someone said they were too loose.
                """,
                "symptoms": [
                    "Z-axis stiff movement",
                    "Occasional binding",
                    "Uneven layer lines",
                    "Nozzle digging into print",
                    "Recently adjusted eccentric nuts"
                ],
                "actual_problems": [
                    {
                        "type": "z_binding",
                        "root_cause": "eccentric_nuts_too_tight",
                        "severity": "moderate",
                        "component": "wheels_z"
                    }
                ],
                "solution_summary": "Loosen Z eccentric nuts - wheels should turn freely",
                "lesson": "Over-tightening causes more problems than under-tightening"
            },

            # Scenario 9: Dual Z Desync
            {
                "id": "REAL_009",
                "title": "Dual Z Motors Out of Sync",
                "source": "TH3D Support",
                "difficulty": "hard",
                "printer_type": "Ender 3 Pro",
                "user_description": """
                I installed a dual Z-axis kit (Y-splitter, single driver). Everything
                worked great for a week. Now one side of the X-gantry is higher than
                the other. When I try to home, the motors sound weird and one side
                barely moves. I think they're fighting each other.
                """,
                "symptoms": [
                    "X-gantry unlevel (one side high)",
                    "Motors sound strained",
                    "One side moves less than other",
                    "Worked initially, problem developed",
                    "Single driver setup"
                ],
                "actual_problems": [
                    {
                        "type": "dual_z_desync",
                        "root_cause": "manual_movement_while_off",
                        "severity": "moderate"
                    },
                    {
                        "type": "z_binding",
                        "root_cause": "lead_screw_binding",
                        "severity": "minor"
                    }
                ],
                "solution_summary": "Power off, manually level gantry with blocks, power on",
                "lesson": "Single driver dual Z can desync if moved while powered off"
            },

            # Scenario 10: CoreXY Belt Nightmare
            {
                "id": "REAL_010",
                "title": "Voron Prints Shifted Diagonally",
                "source": "Voron Discord",
                "difficulty": "hard",
                "printer_type": "Voron 2.4",
                "user_description": """
                My Voron 2.4 build is printing, but rectangles come out as parallelograms.
                Everything shifts diagonally to the right. I've checked belt paths and
                they look correct. Belts are tensioned to about 110Hz on both A and B.
                Using Klipper. This is my first CoreXY.
                """,
                "symptoms": [
                    "Diagonal shifting pattern",
                    "Rectangles become parallelograms",
                    "Consistent diagonal offset",
                    "Belt paths appear correct",
                    "Similar belt tensions"
                ],
                "actual_problems": [
                    {
                        "type": "corexy_belt_desync",
                        "root_cause": "unequal_belt_tension",
                        "severity": "major"
                    }
                ],
                "solution_summary": "Measure each belt separately, adjust to within 1-2Hz of each other",
                "lesson": "CoreXY diagonal shifts = belt sync problem, not Z-wobble"
            },

            # Scenario 11: Power Supply Blues
            {
                "id": "REAL_011",
                "title": "Printer Won't Turn On At All",
                "source": "Creality Support",
                "difficulty": "easy",
                "printer_type": "Ender 3",
                "user_description": """
                My printer just died. Worked fine yesterday, today nothing. No lights,
                no LCD, completely dead. I checked the power outlet with my phone charger
                and it works. The power supply has a green light on it though.
                """,
                "symptoms": [
                    "No power to printer",
                    "LCD dark",
                    "No LED lights",
                    "Power supply LED is on",
                    "Wall outlet works"
                ],
                "actual_problems": [
                    {
                        "type": "power_connection",
                        "root_cause": "loose_cable_connection",
                        "severity": "minor"
                    }
                ],
                "solution_summary": "Check all power cable connections, especially PSU to mainboard",
                "lesson": "PSU LED on but no printer power = check cables, not PSU itself"
            },

            # Scenario 12: IDEX Misalignment
            {
                "id": "REAL_012",
                "title": "Dual Color Prints Don't Line Up",
                "source": "Duet3D Forums",
                "difficulty": "hard",
                "printer_type": "IDEX Custom",
                "user_description": """
                My IDEX printer is printing, but when I do dual color prints, the second
                extruder is offset by about 0.5mm in X and 0.3mm in Y. I've calibrated
                the tool offsets multiple times. Sometimes the offset seems to change
                between prints. Both hotends at 200°C.
                """,
                "symptoms": [
                    "Dual color misalignment",
                    "Visible offset between extruders",
                    "Offset measurements: 0.5mm X, 0.3mm Y",
                    "Inconsistent between prints",
                    "Tool offsets calibrated"
                ],
                "actual_problems": [
                    {
                        "type": "idex_misalignment",
                        "root_cause": "thermal_expansion_not_accounted",
                        "severity": "moderate"
                    },
                    {
                        "type": "idex_misalignment",
                        "root_cause": "loose_carriage_bolts",
                        "severity": "minor"
                    }
                ],
                "solution_summary": "Calibrate offsets with both hotends at printing temp, tighten carriages",
                "lesson": "IDEX calibration must account for thermal expansion - calibrate at print temp"
            },

        ]

    @staticmethod
    def get_by_difficulty(difficulty: str) -> List[Dict]:
        """Get scenarios filtered by difficulty"""
        all_scenarios = RealWorldScenarios.get_all_scenarios()
        return [s for s in all_scenarios if s.get('difficulty') == difficulty]

    @staticmethod
    def get_by_problem_type(problem_type: str) -> List[Dict]:
        """Get scenarios with a specific problem type"""
        all_scenarios = RealWorldScenarios.get_all_scenarios()
        matching = []
        for scenario in all_scenarios:
            for problem in scenario.get('actual_problems', []):
                if problem.get('type') == problem_type:
                    matching.append(scenario)
                    break
        return matching

    @staticmethod
    def get_beginner_scenarios() -> List[Dict]:
        """Get scenarios suitable for beginners"""
        return RealWorldScenarios.get_by_difficulty('easy')

    @staticmethod
    def get_advanced_scenarios() -> List[Dict]:
        """Get scenarios for advanced troubleshooting"""
        return RealWorldScenarios.get_by_difficulty('hard')


if __name__ == "__main__":
    # Display scenario database info
    scenarios = RealWorldScenarios.get_all_scenarios()

    print("=" * 70)
    print("REAL-WORLD SCENARIO DATABASE")
    print("=" * 70)
    print(f"\nTotal Scenarios: {len(scenarios)}")

    # Count by difficulty
    difficulties = {}
    for s in scenarios:
        diff = s.get('difficulty', 'unknown')
        difficulties[diff] = difficulties.get(diff, 0) + 1

    print(f"\nBy Difficulty:")
    for diff, count in difficulties.items():
        print(f"  - {diff.title()}: {count}")

    # List problem types
    problem_types = set()
    for s in scenarios:
        for problem in s.get('actual_problems', []):
            problem_types.add(problem.get('type'))

    print(f"\nProblem Types Covered: {len(problem_types)}")
    for ptype in sorted(problem_types):
        count = len(RealWorldScenarios.get_by_problem_type(ptype))
        print(f"  - {ptype}: {count} scenarios")

    print("\n" + "=" * 70)
    print("Use this database for realistic training scenarios")
    print("=" * 70)
