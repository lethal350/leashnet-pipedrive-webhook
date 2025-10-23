#!/usr/bin/env python3
"""
Interactive CLI for the 3D Printer Maintenance Agent
"""

import sys
import os
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from agents.printer_maintenance_agent import PrinterMaintenanceAgent


class PrinterAgentCLI:
    """Interactive command-line interface for the printer maintenance agent."""

    def __init__(self):
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None

        try:
            self.agent = PrinterMaintenanceAgent()
        except ValueError as e:
            self._print_error(str(e))
            self._print_info("\nPlease set your ANTHROPIC_API_KEY:")
            self._print_info("  export ANTHROPIC_API_KEY='your-api-key-here'")
            sys.exit(1)

    def _print_header(self, text: str):
        """Print a formatted header."""
        if self.console:
            self.console.print(Panel(text, style="bold cyan"))
        else:
            print(f"\n{'=' * 70}")
            print(f"  {text}")
            print('=' * 70)

    def _print_info(self, text: str):
        """Print informational text."""
        if self.console:
            self.console.print(text, style="blue")
        else:
            print(text)

    def _print_error(self, text: str):
        """Print error text."""
        if self.console:
            self.console.print(f"✗ {text}", style="bold red")
        else:
            print(f"ERROR: {text}")

    def _print_success(self, text: str):
        """Print success text."""
        if self.console:
            self.console.print(f"✓ {text}", style="bold green")
        else:
            print(f"✓ {text}")

    def _print_agent_response(self, text: str):
        """Print the agent's response with formatting."""
        if self.console:
            md = Markdown(text)
            self.console.print(Panel(md, title="[bold]Agent Response[/bold]",
                                   border_style="green"))
        else:
            print(f"\n{'=' * 70}")
            print("AGENT RESPONSE:")
            print('-' * 70)
            print(text)
            print('=' * 70)

    def _get_input(self, prompt: str) -> str:
        """Get user input with optional rich formatting."""
        if self.console:
            return Prompt.ask(f"[bold yellow]{prompt}[/bold yellow]")
        else:
            return input(f"{prompt}: ").strip()

    def show_help(self):
        """Display help information."""
        help_text = """
Available Commands:

  help              - Show this help message
  diagnose          - Start a new diagnostic session
  continue          - Continue current conversation
  maintenance       - Get maintenance schedule
  upgrades          - Get upgrade recommendations
  context           - Add printer context (model, filament, temps)
  reset             - Reset conversation and start fresh
  export            - Export conversation to JSON file

Memory Commands:
  save              - Save current conversation to memory
  search            - Search memory for past solutions
  list              - List all saved memories
  stats             - Show memory statistics

  quit / exit       - Exit the program

Example Usage:

  > diagnose
  > My prints have gaps between layers

  > save
  > Problem: gaps | Solution: increased flow rate | Tags: extrusion

  > search
  > belt tension issues

  > list
"""
        self._print_info(help_text)

    def run_diagnostic_session(self):
        """Run an interactive diagnostic session."""
        self._print_header("New Diagnostic Session")
        self._print_info("\nDescribe your 3D printer problem in detail.")
        self._print_info("Include symptoms, when it happens, and what you've tried.")
        print()

        problem = self._get_input("Problem description")

        if not problem:
            self._print_error("No problem description provided.")
            return

        # Ask for context
        self._print_info("\nOptional: Provide additional context (press Enter to skip)")
        printer_model = self._get_input("Printer model (e.g., Ender 3 Pro)")
        filament = self._get_input("Filament type (e.g., PLA)")
        nozzle_temp = self._get_input("Nozzle temperature (e.g., 200)")
        bed_temp = self._get_input("Bed temperature (e.g., 60)")

        # Build context dictionary
        context = {}
        if printer_model:
            context["printer_model"] = printer_model
        if filament:
            context["filament"] = filament
        if nozzle_temp:
            context["nozzle_temp"] = f"{nozzle_temp}°C"
        if bed_temp:
            context["bed_temp"] = f"{bed_temp}°C"

        # Get diagnosis
        print()
        self._print_info("Analyzing problem...")
        response = self.agent.diagnose(problem, context if context else None)
        print()
        self._print_agent_response(response)

    def continue_conversation(self):
        """Continue the current conversation."""
        if not self.agent.conversation_history:
            self._print_error("No active conversation. Start a new diagnosis first.")
            return

        print()
        message = self._get_input("Your message")

        if not message:
            return

        print()
        self._print_info("Processing...")
        response = self.agent.continue_conversation(message)
        print()
        self._print_agent_response(response)

    def get_maintenance_schedule(self):
        """Get maintenance schedule."""
        self._print_info("\nGetting maintenance schedule...")
        self.agent.reset_conversation()
        response = self.agent.get_maintenance_schedule()
        print()
        self._print_agent_response(response)

    def get_upgrades(self):
        """Get upgrade recommendations."""
        print()
        use_case = self._get_input("Use case (general/speed/quality/reliability)")

        if not use_case:
            use_case = "general"

        self._print_info(f"\nGetting upgrade recommendations for: {use_case}...")
        self.agent.reset_conversation()
        response = self.agent.get_upgrade_recommendations(use_case)
        print()
        self._print_agent_response(response)

    def export_conversation(self):
        """Export conversation history."""
        if not self.agent.conversation_history:
            self._print_error("No conversation to export.")
            return

        filename = self._get_input("Filename (default: conversation_history.json)")

        if not filename:
            filename = "conversation_history.json"

        if not filename.endswith('.json'):
            filename += '.json'

        try:
            self.agent.export_conversation(filename)
            self._print_success(f"Conversation exported to {filename}")
        except Exception as e:
            self._print_error(f"Failed to export: {str(e)}")

    def reset_conversation(self):
        """Reset the conversation."""
        self.agent.reset_conversation()
        self._print_success("Conversation reset. Starting fresh.")

    def save_conversation_to_memory(self):
        """Save current conversation to memory."""
        if not self.agent.conversation_history:
            self._print_error("No conversation to save")
            return

        print()
        self._print_info("Save this conversation to memory")
        problem = self._get_input("Problem summary")
        if not problem:
            self._print_error("Problem summary required")
            return

        solution = self._get_input("Solution summary")
        if not solution:
            self._print_error("Solution summary required")
            return

        tags_input = self._get_input("Tags (comma-separated, e.g., hotend,clog,pla)")
        tags = [t.strip() for t in tags_input.split(',')] if tags_input else []

        success_input = self._get_input("Was this solution successful? (yes/no)")
        success = success_input.lower() in ['yes', 'y', '']

        notes = self._get_input("Additional notes (optional)")

        self.agent.save_to_memory(
            problem_summary=problem,
            solution_summary=solution,
            tags=tags,
            success=success,
            notes=notes if notes else None
        )

    def search_memory_ui(self):
        """Search memory interface."""
        print()
        query = self._get_input("Search query")
        if not query:
            return

        limit_input = self._get_input("Max results (default: 5)")
        limit = int(limit_input) if limit_input and limit_input.isdigit() else 5

        print()
        self._print_info("Searching memory...")
        self.agent.search_memory(query, limit=limit, show_details=True)

    def list_memories_ui(self):
        """List all memories interface."""
        print()
        sort_input = self._get_input("Sort by (timestamp/usage/helpful) [default: timestamp]")
        sort_by = sort_input if sort_input in ['usage_count', 'helpful_count'] else 'timestamp'

        if sort_by == 'usage':
            sort_by = 'usage_count'
        elif sort_by == 'helpful':
            sort_by = 'helpful_count'

        limit_input = self._get_input("Max results (default: 20)")
        limit = int(limit_input) if limit_input and limit_input.isdigit() else 20

        print()
        self.agent.list_memories(limit=limit, sort_by=sort_by)

    def show_memory_stats(self):
        """Show memory statistics."""
        stats = self.agent.get_memory_stats()

        if "error" in stats:
            self._print_error(stats["error"])
            return

        print()
        self._print_header("Memory Statistics")
        print(f"\nTotal Memories: {stats['total_memories']}")
        print(f"Successful Solutions: {stats['successful_solutions']}")
        print(f"Total Times Referenced: {stats['total_usage']}")

        if stats['most_common_tags']:
            print(f"\nMost Common Tags:")
            for tag, count in stats['most_common_tags']:
                print(f"  - {tag}: {count} times")

        if stats['most_helpful']:
            print(f"\nMost Helpful Memories:")
            for mem in stats['most_helpful']:
                print(f"  - {mem['id']}: {mem['problem']} (helpful: {mem['helpful_count']})")
        print()

    def run(self):
        """Run the interactive CLI."""
        self._print_header("3D Printer Maintenance Agent")
        self._print_info("\nSpecialized assistant for Ender 3 and related 3D printers")
        self._print_info("Type 'help' for available commands, 'quit' to exit\n")

        while True:
            try:
                command = self._get_input("\nCommand").lower().strip()

                if not command:
                    continue

                if command in ['quit', 'exit', 'q']:
                    self._print_success("\nGoodbye! Happy printing!")
                    break

                elif command in ['help', 'h', '?']:
                    self.show_help()

                elif command in ['diagnose', 'd']:
                    self.run_diagnostic_session()

                elif command in ['continue', 'c']:
                    self.continue_conversation()

                elif command in ['maintenance', 'm']:
                    self.get_maintenance_schedule()

                elif command in ['upgrades', 'u']:
                    self.get_upgrades()

                elif command in ['reset', 'r']:
                    self.reset_conversation()

                elif command in ['export', 'e']:
                    self.export_conversation()

                elif command in ['save', 's']:
                    self.save_conversation_to_memory()

                elif command in ['search']:
                    self.search_memory_ui()

                elif command in ['list', 'l']:
                    self.list_memories_ui()

                elif command in ['stats']:
                    self.show_memory_stats()

                else:
                    self._print_error(f"Unknown command: {command}")
                    self._print_info("Type 'help' for available commands")

            except KeyboardInterrupt:
                print()
                self._print_info("\nUse 'quit' or 'exit' to close the program")
            except Exception as e:
                self._print_error(f"An error occurred: {str(e)}")


def main():
    """Main entry point for the CLI."""
    cli = PrinterAgentCLI()
    cli.run()


if __name__ == "__main__":
    main()
