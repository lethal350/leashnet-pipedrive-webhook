#!/usr/bin/env python3
"""
Agent Training Orchestrator

This script runs the 3D Printer Maintenance Agent through hundreds or thousands
of virtual scenarios to build real-world experience and improve diagnostic capabilities.
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Add parent directory to path to import agent
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.printer_maintenance_agent import PrinterMaintenanceAgent
from training.virtual_printer import (
    ScenarioGenerator,
    ScenarioEvaluator,
    save_training_session,
    PrinterType
)


class TrainingSession:
    """
    Manages a complete training session for the agent.
    """

    def __init__(self, agent: PrinterMaintenanceAgent, session_name: str = None):
        self.agent = agent
        self.session_name = session_name or f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.generator = ScenarioGenerator()
        self.evaluator = ScenarioEvaluator()
        self.scenarios_completed = 0
        self.start_time = None

    def run_single_scenario(self, scenario: Dict, verbose: bool = True) -> Dict:
        """Run agent through a single scenario"""
        if verbose:
            print(f"\n{'=' * 70}")
            print(f"Scenario {self.scenarios_completed + 1}: {scenario['id']}")
            print(f"Difficulty: {scenario['difficulty'].upper()}")
            print(f"Printer: {scenario['printer'].printer_type.value}")
            print('=' * 70)
            print(f"\nUser says: \"{scenario['user_description']}\"")
            print("\nObservable symptoms:")
            for symptom in scenario['symptoms']:
                print(f"  • {symptom}")

        # Build context for agent
        context = {
            "printer_model": scenario['printer'].printer_type.value,
            "total_hours": f"{scenario['printer'].total_hours:.0f}",
            "observable_symptoms": ", ".join(scenario['symptoms']),
        }

        # Get agent's diagnosis
        if verbose:
            print("\n🤖 Agent is diagnosing...")

        start_time = time.time()
        agent_response = self.agent.diagnose(scenario['user_description'], context)
        response_time = time.time() - start_time

        if verbose:
            print(f"\n{'─' * 70}")
            print("AGENT RESPONSE:")
            print('─' * 70)
            print(agent_response)
            print('─' * 70)

        # Evaluate response
        evaluation = self.evaluator.evaluate_response(scenario, agent_response)
        evaluation['response_time'] = response_time

        if verbose:
            print(f"\n📊 EVALUATION RESULTS:")
            print(f"   Overall Score: {evaluation['total_score']:.1f}/100")
            print(f"   Grade: {evaluation['grade']}")
            print(f"   Response Time: {response_time:.2f}s")
            print(f"\n   Breakdown:")
            for category, score in evaluation['scores'].items():
                max_score = {
                    'problem_identification': 40,
                    'root_cause_analysis': 30,
                    'solution_quality': 20,
                    'communication': 10
                }[category]
                print(f"     • {category.replace('_', ' ').title()}: {score:.1f}/{max_score}")

            print(f"\n   Feedback:")
            for feedback in evaluation['feedback']:
                print(f"     {feedback}")

            print(f"\n   Actual Problems (for review):")
            for problem in scenario['actual_problems']:
                prob_str = f"     • {problem['type']} ({problem['severity'].value})"
                if 'root_cause' in problem:
                    prob_str += f" - Root: {problem['root_cause']}"
                print(prob_str)

        self.scenarios_completed += 1

        # Reset agent conversation for next scenario
        self.agent.reset_conversation()

        return evaluation

    def run_training_batch(self, count: int = 10, difficulty: str = "medium", verbose: bool = True):
        """Run agent through multiple scenarios"""
        print(f"\n{'=' * 70}")
        print(f"STARTING TRAINING BATCH: {count} scenarios at {difficulty} difficulty")
        print('=' * 70)

        self.start_time = time.time()

        for i in range(count):
            # Generate scenario
            scenario = self.generator.generate_scenario(difficulty)

            # Run scenario
            try:
                evaluation = self.run_single_scenario(scenario, verbose)

                # Pause between scenarios
                if verbose and i < count - 1:
                    print("\nPress Enter for next scenario (or Ctrl+C to stop)...")
                    input()

            except KeyboardInterrupt:
                print("\n\nTraining interrupted by user.")
                break
            except Exception as e:
                print(f"\n⚠️ Error in scenario: {e}")
                continue

        # Show session summary
        self.show_summary()

    def run_progressive_training(self, scenarios_per_level: int = 10):
        """
        Run progressive training starting from easy and increasing difficulty.
        """
        print(f"\n{'=' * 70}")
        print("PROGRESSIVE TRAINING MODE")
        print('=' * 70)
        print(f"Will run {scenarios_per_level} scenarios at each difficulty level")
        print("Agent will progress from EASY → MEDIUM → HARD")
        print()

        for difficulty in ["easy", "medium", "hard"]:
            print(f"\n{'🎯' * 35}")
            print(f"DIFFICULTY LEVEL: {difficulty.upper()}")
            print(f"{'🎯' * 35}\n")

            self.run_training_batch(scenarios_per_level, difficulty, verbose=False)

            # Show progress
            stats = self.evaluator.get_statistics()
            print(f"\nCurrent Average Score: {stats['average_score']:.1f}/100")

            input(f"\nPress Enter to continue to next difficulty level...")

        print(f"\n{'🏆' * 35}")
        print("PROGRESSIVE TRAINING COMPLETE!")
        print(f"{'🏆' * 35}\n")

    def run_stress_test(self, count: int = 100, save_interval: int = 25):
        """
        Run a large number of scenarios to stress test the agent.
        """
        print(f"\n{'=' * 70}")
        print(f"STRESS TEST MODE: {count} scenarios")
        print('=' * 70)

        self.start_time = time.time()
        difficulties = ["easy", "medium", "hard"]

        for i in range(count):
            difficulty = difficulties[i % 3]  # Rotate through difficulties
            scenario = self.generator.generate_scenario(difficulty)

            try:
                # Run without verbose output for speed
                evaluation = self.run_single_scenario(scenario, verbose=False)

                # Progress indicator
                if (i + 1) % 10 == 0:
                    elapsed = time.time() - self.start_time
                    rate = (i + 1) / elapsed
                    remaining = (count - i - 1) / rate if rate > 0 else 0

                    print(f"Progress: {i + 1}/{count} scenarios "
                          f"({(i + 1) / count * 100:.1f}%) "
                          f"- ETA: {remaining / 60:.1f} min "
                          f"- Avg Score: {self.evaluator.get_statistics()['average_score']:.1f}")

                # Save checkpoint
                if (i + 1) % save_interval == 0:
                    checkpoint_file = f"checkpoints/{self.session_name}_checkpoint_{i + 1}.json"
                    os.makedirs("checkpoints", exist_ok=True)
                    save_training_session(self.evaluator, checkpoint_file)
                    print(f"  💾 Checkpoint saved: {checkpoint_file}")

            except Exception as e:
                print(f"  ⚠️ Error in scenario {i + 1}: {e}")
                continue

        print(f"\n{'🏁' * 35}")
        print("STRESS TEST COMPLETE!")
        print(f"{'🏁' * 35}\n")

    def show_summary(self):
        """Show detailed training session summary"""
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        stats = self.evaluator.get_statistics()

        print(f"\n{'=' * 70}")
        print("TRAINING SESSION SUMMARY")
        print('=' * 70)

        print(f"\nSession: {self.session_name}")
        print(f"Duration: {elapsed_time / 60:.1f} minutes")
        print(f"Scenarios Completed: {self.scenarios_completed}")

        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"   Overall Average: {stats['average_score']:.1f}/100")
        print(f"   Trend: {stats['improvement_trend']}")

        print(f"\n📊 CATEGORY BREAKDOWN:")
        for category, score in stats['category_averages'].items():
            max_scores = {
                'problem_identification': 40,
                'root_cause_analysis': 30,
                'solution_quality': 20,
                'communication': 10
            }
            max_score = max_scores[category]
            percentage = (score / max_score) * 100
            print(f"   • {category.replace('_', ' ').title()}: {score:.1f}/{max_score} ({percentage:.0f}%)")

        print(f"\n🎓 GRADE DISTRIBUTION:")
        for grade in ['A', 'B', 'C', 'D', 'F']:
            count = stats['grade_distribution'].get(grade, 0)
            percentage = (count / self.scenarios_completed) * 100 if self.scenarios_completed > 0 else 0
            bar = '█' * int(percentage / 2)
            print(f"   {grade}: {bar} {count} ({percentage:.1f}%)")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if stats['category_averages']['problem_identification'] < 30:
            print("   ⚠️  Focus on improving problem identification skills")
        if stats['category_averages']['root_cause_analysis'] < 20:
            print("   ⚠️  Work on root cause analysis depth")
        if stats['category_averages']['solution_quality'] < 15:
            print("   ⚠️  Provide more comprehensive solution steps")
        if stats['category_averages']['communication'] < 7:
            print("   ⚠️  Enhance communication and user guidance")

        if stats['average_score'] >= 85:
            print("   ✅ Excellent performance! Ready for production use.")
        elif stats['average_score'] >= 75:
            print("   ✅ Good performance. Minor improvements needed.")
        elif stats['average_score'] >= 65:
            print("   ⚠️  Satisfactory. Continued training recommended.")
        else:
            print("   ⚠️  Needs significant improvement. More training required.")

        # Save session
        save_path = f"training_results/{self.session_name}.json"
        os.makedirs("training_results", exist_ok=True)
        save_training_session(self.evaluator, save_path)
        print(f"\n💾 Full session data saved to: {save_path}")

    def export_scenarios_for_review(self, filename: str = None):
        """Export scenarios with agent responses for human review"""
        if not filename:
            filename = f"scenario_review_{self.session_name}.json"

        review_data = {
            "session": self.session_name,
            "timestamp": datetime.now().isoformat(),
            "scenarios": self.evaluator.evaluation_history
        }

        with open(filename, 'w') as f:
            json.dump(review_data, f, indent=2)

        print(f"Scenarios exported for review: {filename}")


def main():
    """Main training interface"""
    print("=" * 70)
    print("3D PRINTER MAINTENANCE AGENT - TRAINING SYSTEM")
    print("=" * 70)
    print()

    # Initialize agent
    try:
        agent = PrinterMaintenanceAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\nPlease set ANTHROPIC_API_KEY environment variable")
        return

    # Training mode selection
    print("\n📚 TRAINING MODES:")
    print("   1. Single Scenario (Interactive)")
    print("   2. Small Batch (10 scenarios)")
    print("   3. Medium Batch (25 scenarios)")
    print("   4. Large Batch (50 scenarios)")
    print("   5. Progressive Training (Easy → Medium → Hard)")
    print("   6. Stress Test (100+ scenarios)")
    print("   7. Custom Configuration")
    print()

    try:
        choice = input("Select training mode (1-7): ").strip()

        session = TrainingSession(agent)

        if choice == "1":
            difficulty = input("Difficulty (easy/medium/hard): ").strip() or "medium"
            scenario = session.generator.generate_scenario(difficulty)
            session.run_single_scenario(scenario, verbose=True)

        elif choice == "2":
            difficulty = input("Difficulty (easy/medium/hard): ").strip() or "medium"
            session.run_training_batch(10, difficulty, verbose=True)

        elif choice == "3":
            difficulty = input("Difficulty (easy/medium/hard): ").strip() or "medium"
            session.run_training_batch(25, difficulty, verbose=False)

        elif choice == "4":
            difficulty = input("Difficulty (easy/medium/hard): ").strip() or "medium"
            session.run_training_batch(50, difficulty, verbose=False)

        elif choice == "5":
            scenarios_per_level = int(input("Scenarios per difficulty level (default 10): ").strip() or "10")
            session.run_progressive_training(scenarios_per_level)

        elif choice == "6":
            count = int(input("Number of scenarios (default 100): ").strip() or "100")
            session.run_stress_test(count)

        elif choice == "7":
            count = int(input("Number of scenarios: ").strip())
            difficulty = input("Difficulty (easy/medium/hard): ").strip() or "medium"
            verbose = input("Verbose output? (y/n): ").strip().lower() == "y"
            session.run_training_batch(count, difficulty, verbose)

        else:
            print("Invalid choice")
            return

        # Offer to export for review
        export = input("\nExport scenarios for human review? (y/n): ").strip().lower()
        if export == "y":
            session.export_scenarios_for_review()

        print("\n✅ Training session complete!")

    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
