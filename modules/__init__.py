# modules/__init__.py
"""
AI Red-Teaming Toolkit - Core Modules
"""

from .jailbreak_tester import JailbreakTester, JailbreakType
from .prompt_injection import PromptInjectionTester, InjectionType
from .vulnerability_classifier import VulnerabilityClassifier, VulnerabilityCategory, Severity
from .report_generator import ReportGenerator

__version__ = "1.0.0"

__all__ = [
    'JailbreakTester',
    'JailbreakType',
    'PromptInjectionTester',
    'InjectionType',
    'VulnerabilityClassifier',
    'VulnerabilityCategory',
    'Severity',
    'ReportGenerator'
]
