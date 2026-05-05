"""
Enterprise Incentive Intelligence System - Core Modules
"""

from .dataset_generator import DatasetGenerator
from .incentive_engine import IncentiveEngine
from .validation import DataValidator
from .anomaly_detection import AnomalyDetector
from .database import DatabaseManager
from .analytics import Analytics
from .reporting import Reporter

__version__ = "1.0.0"
__author__ = "Enterprise Intelligence Team"

__all__ = [
    'DatasetGenerator',
    'IncentiveEngine',
    'DataValidator',
    'AnomalyDetector',
    'DatabaseManager',
    'Analytics',
    'Reporter'
]
