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
  quit / exit       - Exit the program

Example Usage:

  > diagnose
  > My prints have gaps between layers

  > continue
  > How do I calibrate e-steps?

  > context
  > Printer: Ender 3 Pro, Filament: PLA, Temp: 200C
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
