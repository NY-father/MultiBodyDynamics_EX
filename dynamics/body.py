from dataclasses import dataclass
from PySide6.QtCore import QPointF

@dataclass
class Body:
    point1: QPointF
    point2: QPointF
    center: QPointF
    mass: float
    inertia: float
    selection_marker: any = None  # For storing selection marker
