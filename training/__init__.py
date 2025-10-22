"""
3D Printer Maintenance Agent Training Environment

This package provides a comprehensive virtual training environment where the
3D Printer Maintenance Agent can practice diagnosing and solving real-world
3D printer problems through simulation.
"""

from .virtual_printer import (
    VirtualPrinter,
    PrinterType,
    ComponentCondition,
    ProblemSeverity,
    ScenarioGenerator,
    ScenarioEvaluator,
    save_training_session
)

from .train_agent import TrainingSession

__all__ = [
    'VirtualPrinter',
    'PrinterType',
    'ComponentCondition',
    'ProblemSeverity',
    'ScenarioGenerator',
    'ScenarioEvaluator',
    'TrainingSession',
    'save_training_session'
]

__version__ = '1.0.0'
