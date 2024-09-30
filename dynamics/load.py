# dynamics/load.py
from dataclasses import dataclass
from PySide6.QtCore import QPointF

@dataclass
class Load:
    joint: 'Joint'
    torque: float
