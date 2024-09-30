# dynamics/joint.py
from dataclasses import dataclass
from PySide6.QtCore import QPointF

@dataclass
class Joint:
    body1: 'Body'
    body2: 'Body'
    position: QPointF
    torque: float = 0.0
