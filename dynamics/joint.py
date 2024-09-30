from dataclasses import dataclass
from PySide6.QtCore import QPointF

@dataclass
class Joint:
    body1: 'Body'
    body2: 'Body'
    position: QPointF
    joint_type: str = 'Hinge'
    torque: float = 0.0
    graphics: any = None  # For storing QGraphicsEllipseItem
