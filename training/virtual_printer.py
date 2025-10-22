#!/usr/bin/env python3
"""
3D Printer Virtual Training Environment

This module creates a realistic simulation environment where the 3D Printer
Maintenance Agent can practice diagnosing and solving real-world problems,
gaining experience through thousands of scenarios.
"""

import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum


class PrinterType(Enum):
    """Types of 3D printers supported"""
    ENDER_3 = "Ender 3"
    ENDER_3_PRO = "Ender 3 Pro"
    ENDER_3_V2 = "Ender 3 V2"
    CR10 = "CR-10"
    COREXY_VORON = "Voron 2.4"
    IDEX = "IDEX Dual Extruder"


class ComponentCondition(Enum):
    """Condition states for components"""
    PERFECT = "perfect"
    GOOD = "good"
    WORN = "worn"
    DAMAGED = "damaged"
    FAILED = "failed"


class ProblemSeverity(Enum):
    """Severity levels for problems"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"


@dataclass
class PrinterComponent:
    """Represents a physical component of the printer"""
    name: str
    condition: ComponentCondition
    wear_level: float  # 0.0 (new) to 1.0 (completely worn)
    temperature: Optional[float] = None
    hours_used: int = 0

    def degrade(self, amount: float = 0.01):
        """Simulate component degradation over time"""
        self.wear_level = min(1.0, self.wear_level + amount)
        if self.wear_level > 0.8:
            self.condition = ComponentCondition.DAMAGED
        elif self.wear_level > 0.6:
            self.condition = ComponentCondition.WORN
        elif self.wear_level > 0.3:
            self.condition = ComponentCondition.GOOD

    def repair(self):
        """Repair or replace component"""
        self.wear_level = 0.0
        self.condition = ComponentCondition.PERFECT
        self.hours_used = 0


class VirtualPrinter:
    """
    Simulates a complete 3D printer with realistic physics and degradation.
    """

    def __init__(self, printer_type: PrinterType = PrinterType.ENDER_3):
        self.printer_type = printer_type
        self.total_hours = 0
        self.total_prints = 0

        # Initialize all components
        self.components = {
            # Mechanical
            "belt_x": PrinterComponent("X-axis Belt", ComponentCondition.PERFECT, 0.0),
            "belt_y": PrinterComponent("Y-axis Belt", ComponentCondition.PERFECT, 0.0),
            "leadscrew_z": PrinterComponent("Z Lead Screw", ComponentCondition.PERFECT, 0.0),
            "wheels_x": PrinterComponent("X-axis Wheels", ComponentCondition.PERFECT, 0.0),
            "wheels_y": PrinterComponent("Y-axis Wheels", ComponentCondition.PERFECT, 0.0),
            "wheels_z": PrinterComponent("Z-axis Wheels", ComponentCondition.PERFECT, 0.0),
            "extruder_gear": PrinterComponent("Extruder Gear", ComponentCondition.PERFECT, 0.0),
            "extruder_arm": PrinterComponent("Extruder Arm", ComponentCondition.PERFECT, 0.0),

            # Hotend
            "nozzle": PrinterComponent("Nozzle", ComponentCondition.PERFECT, 0.0, temperature=0),
            "heater_block": PrinterComponent("Heater Block", ComponentCondition.PERFECT, 0.0),
            "ptfe_tube": PrinterComponent("PTFE Tube", ComponentCondition.PERFECT, 0.0),
            "heat_break": PrinterComponent("Heat Break", ComponentCondition.PERFECT, 0.0),
            "cooling_fan": PrinterComponent("Hotend Cooling Fan", ComponentCondition.PERFECT, 0.0),

            # Bed
            "bed_surface": PrinterComponent("Bed Surface", ComponentCondition.PERFECT, 0.0),
            "bed_springs": PrinterComponent("Bed Springs", ComponentCondition.PERFECT, 0.0),
            "bed_heater": PrinterComponent("Bed Heater", ComponentCondition.PERFECT, 0.0),

            # Electronics
            "mainboard": PrinterComponent("Mainboard", ComponentCondition.PERFECT, 0.0),
            "power_supply": PrinterComponent("Power Supply", ComponentCondition.PERFECT, 0.0),
            "stepper_x": PrinterComponent("X Stepper Motor", ComponentCondition.PERFECT, 0.0),
            "stepper_y": PrinterComponent("Y Stepper Motor", ComponentCondition.PERFECT, 0.0),
            "stepper_z": PrinterComponent("Z Stepper Motor", ComponentCondition.PERFECT, 0.0),
            "stepper_e": PrinterComponent("Extruder Stepper Motor", ComponentCondition.PERFECT, 0.0),

            # Sensors
            "endstop_x": PrinterComponent("X Endstop", ComponentCondition.PERFECT, 0.0),
            "endstop_y": PrinterComponent("Y Endstop", ComponentCondition.PERFECT, 0.0),
            "endstop_z": PrinterComponent("Z Endstop", ComponentCondition.PERFECT, 0.0),
            "thermistor_hotend": PrinterComponent("Hotend Thermistor", ComponentCondition.PERFECT, 0.0),
            "thermistor_bed": PrinterComponent("Bed Thermistor", ComponentCondition.PERFECT, 0.0),
        }

        # CoreXY specific components
        if printer_type == PrinterType.COREXY_VORON:
            self.components["belt_a"] = PrinterComponent("CoreXY Belt A", ComponentCondition.PERFECT, 0.0)
            self.components["belt_b"] = PrinterComponent("CoreXY Belt B", ComponentCondition.PERFECT, 0.0)

        # IDEX specific components
        if printer_type == PrinterType.IDEX:
            self.components["extruder_2"] = PrinterComponent("Second Extruder", ComponentCondition.PERFECT, 0.0)
            self.components["nozzle_2"] = PrinterComponent("Second Nozzle", ComponentCondition.PERFECT, 0.0)

        # Printer settings
        self.settings = {
            "bed_level": 1.0,  # 1.0 = perfectly level
            "belt_tension_x": 110.0,  # Hz frequency
            "belt_tension_y": 110.0,
            "nozzle_temp": 0,
            "bed_temp": 0,
            "esteps": 93.0,
            "flow_rate": 100.0,
            "z_offset": 0.0,
        }

        # Current problems (empty at start)
        self.active_problems: List[Dict[str, Any]] = []

    def simulate_printing(self, hours: float = 1.0):
        """Simulate printing for a given number of hours"""
        self.total_hours += hours
        self.total_prints += 1

        # Degrade components based on usage
        for component in self.components.values():
            component.hours_used += hours

            # Different components wear at different rates
            if "belt" in component.name.lower():
                component.degrade(0.001 * hours)
            elif "wheel" in component.name.lower():
                component.degrade(0.002 * hours)
            elif "nozzle" in component.name.lower():
                component.degrade(0.005 * hours)
            elif "ptfe" in component.name.lower():
                component.degrade(0.003 * hours)
            elif "extruder" in component.name.lower():
                component.degrade(0.002 * hours)
            elif "spring" in component.name.lower():
                component.degrade(0.001 * hours)
            else:
                component.degrade(0.0005 * hours)

        # Settings drift over time
        self.settings["bed_level"] -= random.uniform(0.01, 0.03) * hours
        self.settings["belt_tension_x"] -= random.uniform(0.5, 2.0) * hours
        self.settings["belt_tension_y"] -= random.uniform(0.5, 2.0) * hours

    def introduce_problem(self, problem_type: str, severity: ProblemSeverity):
        """Introduce a specific problem to the printer"""
        problem = {
            "type": problem_type,
            "severity": severity,
            "introduced_at": self.total_hours,
            "components_affected": []
        }

        # Apply problem effects based on type
        if problem_type == "loose_belt":
            affected = random.choice(["belt_x", "belt_y"])
            self.settings["belt_tension_x" if "x" in affected else "belt_tension_y"] = random.uniform(60, 90)
            problem["components_affected"].append(affected)

        elif problem_type == "nozzle_clog":
            self.components["nozzle"].wear_level = 0.9
            self.components["nozzle"].condition = ComponentCondition.DAMAGED
            problem["components_affected"].append("nozzle")

        elif problem_type == "bed_adhesion":
            self.settings["bed_level"] = random.uniform(0.5, 0.8)
            self.components["bed_surface"].wear_level = random.uniform(0.4, 0.7)
            problem["components_affected"].extend(["bed_surface", "bed_springs"])

        elif problem_type == "under_extrusion":
            cause = random.choice(["clog", "esteps", "worn_gear"])
            if cause == "clog":
                self.components["nozzle"].wear_level = 0.6
            elif cause == "esteps":
                self.settings["esteps"] = random.uniform(80, 90)
            else:
                self.components["extruder_gear"].wear_level = 0.8
            problem["root_cause"] = cause

        elif problem_type == "layer_shift":
            cause = random.choice(["loose_belt", "loose_pulley", "overheating_driver"])
            affected = random.choice(["belt_x", "belt_y"])
            if cause == "loose_belt":
                self.settings[f"belt_tension_{affected[-1]}"] = 70
            problem["root_cause"] = cause
            problem["components_affected"].append(affected)

        elif problem_type == "heat_creep":
            self.components["cooling_fan"].wear_level = 0.7
            self.components["heat_break"].wear_level = 0.5
            problem["components_affected"].extend(["cooling_fan", "heat_break"])

        elif problem_type == "z_binding":
            self.components["wheels_z"].wear_level = 0.8
            self.components["leadscrew_z"].wear_level = 0.6
            problem["components_affected"].extend(["wheels_z", "leadscrew_z"])

        elif problem_type == "thermal_runaway":
            cause = random.choice(["loose_thermistor", "bad_pid"])
            if cause == "loose_thermistor":
                self.components["thermistor_hotend"].wear_level = 0.9
                problem["components_affected"].append("thermistor_hotend")
            problem["root_cause"] = cause

        elif problem_type == "psu_failure":
            self.components["power_supply"].condition = ComponentCondition.FAILED
            problem["components_affected"].append("power_supply")

        elif problem_type == "bltouch_failure":
            if "bltouch" not in self.components:
                self.components["bltouch"] = PrinterComponent("BLTouch", ComponentCondition.PERFECT, 0.0)
            self.components["bltouch"].condition = ComponentCondition.DAMAGED
            problem["components_affected"].append("bltouch")

        self.active_problems.append(problem)
        return problem

    def get_state_description(self) -> str:
        """Get a human-readable description of current printer state"""
        desc = f"Printer: {self.printer_type.value}\n"
        desc += f"Total Hours: {self.total_hours:.1f}\n"
        desc += f"Total Prints: {self.total_prints}\n\n"

        desc += "Component Conditions:\n"
        for name, comp in self.components.items():
            if comp.condition != ComponentCondition.PERFECT:
                desc += f"  - {comp.name}: {comp.condition.value} (wear: {comp.wear_level:.1%})\n"

        desc += "\nSettings:\n"
        desc += f"  - Bed Level: {self.settings['bed_level']:.1%}\n"
        desc += f"  - Belt Tension X: {self.settings['belt_tension_x']:.0f}Hz\n"
        desc += f"  - Belt Tension Y: {self.settings['belt_tension_y']:.0f}Hz\n"
        desc += f"  - E-steps: {self.settings['esteps']:.1f}\n"

        return desc

    def get_symptoms(self) -> List[str]:
        """Generate observable symptoms based on current problems"""
        symptoms = []

        for problem in self.active_problems:
            if problem["type"] == "loose_belt":
                symptoms.append("Layers are shifting during print")
                symptoms.append("Belt feels loose when manually checked")

            elif problem["type"] == "nozzle_clog":
                symptoms.append("Little to no filament coming out")
                symptoms.append("Extruder motor clicking/skipping")
                symptoms.append("Weak or missing layers")

            elif problem["type"] == "bed_adhesion":
                symptoms.append("First layer not sticking to bed")
                symptoms.append("Prints popping off mid-print")
                symptoms.append("Corners warping up")

            elif problem["type"] == "under_extrusion":
                symptoms.append("Thin layers with gaps")
                symptoms.append("Can see through walls")
                symptoms.append("Weak print strength")

            elif problem["type"] == "heat_creep":
                symptoms.append("Clogging during prints")
                symptoms.append("Extruder motor getting hot")
                symptoms.append("Filament soft above heat break")

            elif problem["type"] == "z_binding":
                symptoms.append("Z-axis moves with difficulty")
                symptoms.append("Layer lines uneven")
                symptoms.append("Grinding noise from Z-axis")

            elif problem["type"] == "thermal_runaway":
                symptoms.append("Thermal runaway error on display")
                symptoms.append("Temperature fluctuating")
                symptoms.append("Heater not reaching target")

            elif problem["type"] == "psu_failure":
                symptoms.append("Printer won't power on")
                symptoms.append("LCD screen stays dark")
                symptoms.append("No LED on power supply")

            elif problem["type"] == "bltouch_failure":
                symptoms.append("BLTouch pin not deploying")
                symptoms.append("Red flashing light on BLTouch")
                symptoms.append("Homing fails, nozzle crashes into bed")

        # Add some noise - not all symptoms always present
        if symptoms:
            num_symptoms = random.randint(max(1, len(symptoms) - 2), len(symptoms))
            symptoms = random.sample(symptoms, num_symptoms)

        return symptoms


class ScenarioGenerator:
    """
    Generates realistic troubleshooting scenarios for training.
    """

    def __init__(self):
        self.scenario_count = 0

        # Problem types with their realistic occurrence rates
        self.problem_types = {
            "nozzle_clog": 0.15,
            "bed_adhesion": 0.20,
            "under_extrusion": 0.12,
            "loose_belt": 0.10,
            "layer_shift": 0.08,
            "heat_creep": 0.06,
            "z_binding": 0.07,
            "thermal_runaway": 0.05,
            "psu_failure": 0.03,
            "bltouch_failure": 0.04,
            "stringing": 0.10,
        }

    def generate_scenario(self, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate a random scenario based on difficulty"""
        self.scenario_count += 1

        # Create a virtual printer
        printer_types = list(PrinterType)
        if difficulty == "easy":
            printer = VirtualPrinter(PrinterType.ENDER_3)
            num_problems = 1
        elif difficulty == "medium":
            printer = VirtualPrinter(random.choice(printer_types[:4]))  # Cartesian only
            num_problems = random.randint(1, 2)
        else:  # hard
            printer = VirtualPrinter(random.choice(printer_types))  # Any type
            num_problems = random.randint(2, 3)

        # Simulate some usage
        usage_hours = random.uniform(50, 1000)
        printer.simulate_printing(usage_hours)

        # Introduce problems
        problems = random.choices(
            list(self.problem_types.keys()),
            weights=list(self.problem_types.values()),
            k=num_problems
        )

        for problem in problems:
            severity = random.choice(list(ProblemSeverity))
            printer.introduce_problem(problem, severity)

        # Generate scenario
        scenario = {
            "id": f"SCENARIO_{self.scenario_count:04d}",
            "difficulty": difficulty,
            "printer": printer,
            "user_description": self._generate_user_description(printer),
            "symptoms": printer.get_symptoms(),
            "actual_problems": printer.active_problems,
            "created_at": datetime.now().isoformat(),
        }

        return scenario

    def _generate_user_description(self, printer: VirtualPrinter) -> str:
        """Generate a realistic user problem description"""
        symptoms = printer.get_symptoms()

        # Simulate different user communication styles
        styles = [
            "technical",  # Precise, uses correct terminology
            "casual",  # Informal, may misname parts
            "frustrated",  # Emotional, less detail
            "detailed",  # Very thorough, lots of context
        ]

        style = random.choice(styles)

        if style == "technical":
            desc = f"My {printer.printer_type.value} is experiencing the following issues: "
            desc += "; ".join(symptoms) + ". "
            desc += f"Printer has {printer.total_hours:.0f} hours of use. "

        elif style == "casual":
            symptom = random.choice(symptoms) if symptoms else "something weird"
            desc = f"Hey, my printer is doing {symptom.lower()}. "
            desc += "Not sure what's going on. "
            desc += random.choice([
                "Been printing fine until now.",
                "Just started happening today.",
                "It's been getting worse over time.",
            ])

        elif style == "frustrated":
            desc = "MY PRINTER ISN'T WORKING RIGHT!!! "
            desc += f"{symptoms[0] if symptoms else 'Nothing is working'}. "
            desc += "I've tried everything and I'm ready to throw it out the window."

        else:  # detailed
            desc = f"I have a {printer.printer_type.value} that I've been using for "
            desc += f"about {printer.total_hours:.0f} hours. Recently I've noticed: "
            desc += "; ".join(symptoms[:2] if len(symptoms) > 2 else symptoms) + ". "
            desc += "I've already tried re-leveling the bed and checking connections. "
            desc += "I mostly print with PLA at 200°C nozzle and 60°C bed."

        return desc

    def generate_batch(self, count: int = 10, difficulty: str = "medium") -> List[Dict]:
        """Generate multiple scenarios"""
        return [self.generate_scenario(difficulty) for _ in range(count)]


class ScenarioEvaluator:
    """
    Evaluates agent responses against known correct solutions.
    """

    def __init__(self):
        self.evaluation_history = []

    def evaluate_response(self, scenario: Dict, agent_response: str) -> Dict[str, Any]:
        """
        Evaluate how well the agent diagnosed and solved the problem.
        """
        actual_problems = scenario["actual_problems"]
        response_lower = agent_response.lower()

        evaluation = {
            "scenario_id": scenario["id"],
            "timestamp": datetime.now().isoformat(),
            "difficulty": scenario["difficulty"],
            "scores": {},
            "total_score": 0,
            "feedback": []
        }

        # Score 1: Problem Identification (40 points)
        problems_identified = 0
        for problem in actual_problems:
            problem_keywords = self._get_problem_keywords(problem["type"])
            if any(keyword in response_lower for keyword in problem_keywords):
                problems_identified += 1

        identification_score = (problems_identified / len(actual_problems)) * 40
        evaluation["scores"]["problem_identification"] = identification_score

        if problems_identified == len(actual_problems):
            evaluation["feedback"].append("✓ Correctly identified all problems")
        elif problems_identified > 0:
            evaluation["feedback"].append(f"⚠ Identified {problems_identified}/{len(actual_problems)} problems")
        else:
            evaluation["feedback"].append("✗ Failed to identify the actual problems")

        # Score 2: Root Cause Analysis (30 points)
        root_causes_found = 0
        total_root_causes = sum(1 for p in actual_problems if "root_cause" in p)

        for problem in actual_problems:
            if "root_cause" in problem:
                cause = problem["root_cause"]
                if cause in response_lower or any(synonym in response_lower for synonym in self._get_cause_synonyms(cause)):
                    root_causes_found += 1

        if total_root_causes > 0:
            root_cause_score = (root_causes_found / total_root_causes) * 30
        else:
            root_cause_score = 30  # Full points if no specific root causes to find
        evaluation["scores"]["root_cause_analysis"] = root_cause_score

        # Score 3: Solution Quality (20 points)
        solution_keywords = [
            "replace", "adjust", "calibrate", "clean", "tighten",
            "loosen", "check", "measure", "test", "verify"
        ]

        solution_actions = sum(1 for keyword in solution_keywords if keyword in response_lower)
        solution_score = min(20, solution_actions * 4)  # Max 20 points
        evaluation["scores"]["solution_quality"] = solution_score

        if solution_score >= 16:
            evaluation["feedback"].append("✓ Provided comprehensive solutions")
        elif solution_score >= 8:
            evaluation["feedback"].append("⚠ Solutions could be more detailed")
        else:
            evaluation["feedback"].append("✗ Insufficient solution guidance")

        # Score 4: Communication Quality (10 points)
        communication_score = 0

        # Check for structured response
        if any(marker in response_lower for marker in ["step", "1.", "first", "next"]):
            communication_score += 3
            evaluation["feedback"].append("✓ Well-structured response")

        # Check for safety warnings
        if any(warning in response_lower for warning in ["caution", "warning", "careful", "⚠️"]):
            communication_score += 3
            evaluation["feedback"].append("✓ Included safety warnings")

        # Check for user-friendly language
        if "let's" in response_lower or "we'll" in response_lower or "i'll help" in response_lower:
            communication_score += 2
            evaluation["feedback"].append("✓ Friendly, helpful tone")

        # Check for diagnostic questions
        if "?" in agent_response:
            communication_score += 2
            evaluation["feedback"].append("✓ Asked clarifying questions")

        evaluation["scores"]["communication"] = communication_score

        # Calculate total score
        evaluation["total_score"] = sum(evaluation["scores"].values())

        # Overall grade
        if evaluation["total_score"] >= 90:
            evaluation["grade"] = "A - Excellent"
        elif evaluation["total_score"] >= 80:
            evaluation["grade"] = "B - Good"
        elif evaluation["total_score"] >= 70:
            evaluation["grade"] = "C - Satisfactory"
        elif evaluation["total_score"] >= 60:
            evaluation["grade"] = "D - Needs Improvement"
        else:
            evaluation["grade"] = "F - Poor"

        self.evaluation_history.append(evaluation)
        return evaluation

    def _get_problem_keywords(self, problem_type: str) -> List[str]:
        """Get keywords that indicate problem identification"""
        keywords_map = {
            "nozzle_clog": ["clog", "blocked", "nozzle", "obstruction"],
            "bed_adhesion": ["adhesion", "stick", "bed level", "first layer"],
            "under_extrusion": ["under-extru", "under extru", "thin layer", "gap"],
            "loose_belt": ["belt", "tension", "loose"],
            "layer_shift": ["layer shift", "shift", "misalign"],
            "heat_creep": ["heat creep", "cooling", "heat break"],
            "z_binding": ["binding", "z-axis", "lead screw"],
            "thermal_runaway": ["thermal runaway", "thermistor", "temperature"],
            "psu_failure": ["power supply", "psu", "no power"],
            "bltouch_failure": ["bltouch", "probe", "sensor"],
            "stringing": ["string", "ooze", "blob"],
        }
        return keywords_map.get(problem_type, [problem_type])

    def _get_cause_synonyms(self, cause: str) -> List[str]:
        """Get synonyms for root causes"""
        synonyms_map = {
            "clog": ["blockage", "obstruction"],
            "esteps": ["e-step", "extruder steps", "calibration"],
            "worn_gear": ["worn", "damaged gear", "slipping"],
            "loose_belt": ["belt tension", "loose"],
            "loose_pulley": ["pulley", "set screw"],
            "overheating_driver": ["driver", "overheating", "stepper"],
            "loose_thermistor": ["thermistor", "sensor", "loose"],
            "bad_pid": ["pid", "tuning", "temperature control"],
        }
        return synonyms_map.get(cause, [])

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall performance statistics"""
        if not self.evaluation_history:
            return {"message": "No evaluations yet"}

        total_evals = len(self.evaluation_history)
        avg_score = sum(e["total_score"] for e in self.evaluation_history) / total_evals

        category_averages = {
            "problem_identification": sum(e["scores"]["problem_identification"] for e in self.evaluation_history) / total_evals,
            "root_cause_analysis": sum(e["scores"]["root_cause_analysis"] for e in self.evaluation_history) / total_evals,
            "solution_quality": sum(e["scores"]["solution_quality"] for e in self.evaluation_history) / total_evals,
            "communication": sum(e["scores"]["communication"] for e in self.evaluation_history) / total_evals,
        }

        grade_distribution = {}
        for eval in self.evaluation_history:
            grade = eval["grade"][0]  # Just the letter
            grade_distribution[grade] = grade_distribution.get(grade, 0) + 1

        return {
            "total_scenarios": total_evals,
            "average_score": avg_score,
            "category_averages": category_averages,
            "grade_distribution": grade_distribution,
            "improvement_trend": self._calculate_trend(),
        }

    def _calculate_trend(self) -> str:
        """Calculate if performance is improving"""
        if len(self.evaluation_history) < 5:
            return "Not enough data"

        recent_scores = [e["total_score"] for e in self.evaluation_history[-10:]]
        older_scores = [e["total_score"] for e in self.evaluation_history[-20:-10]] if len(self.evaluation_history) >= 20 else recent_scores

        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)

        diff = recent_avg - older_avg
        if diff > 5:
            return f"Improving (+{diff:.1f} points)"
        elif diff < -5:
            return f"Declining ({diff:.1f} points)"
        else:
            return "Stable"


def save_training_session(evaluator: ScenarioEvaluator, filename: str = "training_session.json"):
    """Save training session results"""
    session_data = {
        "timestamp": datetime.now().isoformat(),
        "statistics": evaluator.get_statistics(),
        "evaluations": evaluator.evaluation_history
    }

    with open(filename, 'w') as f:
        json.dump(session_data, f, indent=2)

    print(f"Training session saved to {filename}")


if __name__ == "__main__":
    print("=" * 70)
    print("3D PRINTER VIRTUAL TRAINING ENVIRONMENT")
    print("=" * 70)
    print()

    # Demonstrate the system
    print("Creating virtual printer and scenarios...")
    generator = ScenarioGenerator()
    evaluator = ScenarioEvaluator()

    # Generate a sample scenario
    scenario = generator.generate_scenario("medium")

    print(f"\nScenario ID: {scenario['id']}")
    print(f"Difficulty: {scenario['difficulty']}")
    print(f"Printer Type: {scenario['printer'].printer_type.value}")
    print(f"\nUser Description:")
    print(f'"{scenario["user_description"]}"')
    print(f"\nObservable Symptoms:")
    for symptom in scenario['symptoms']:
        print(f"  - {symptom}")

    print(f"\nActual Problems (Hidden from Agent):")
    for problem in scenario['actual_problems']:
        print(f"  - {problem['type']} ({problem['severity'].value})")
        if 'root_cause' in problem:
            print(f"    Root cause: {problem['root_cause']}")

    print("\n" + "=" * 70)
    print("SYSTEM READY FOR TRAINING")
    print("=" * 70)
    print("\nThe agent can now practice with thousands of realistic scenarios!")
    print("Use train_agent.py to run training sessions.")
