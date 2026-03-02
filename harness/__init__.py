"""
Agent Harness Lite - The AI Operating System for 2026

数据驱动的AI Agent运行时，为删除而写，为数据而生。
"""

from .core import Harness, TaskResult
from .data import DataCollector, Dataset

__version__ = "1.0.0"
__all__ = ["Harness", "TaskResult", "DataCollector", "Dataset"]
