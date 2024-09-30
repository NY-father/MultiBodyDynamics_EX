from dataclasses import dataclass, field
from PySide6.QtCore import QPointF

@dataclass
class Body:
    point1: QPointF
    point2: QPointF
    center: QPointF
    mass: float
    inertia: float
    selection_marker: any = None  # For storing selection marker

    length: float = field(init=False)

    def __post_init__(self):
        # Calculate the length of the body
        dx = self.point2.x() - self.point1.x()
        dy = self.point2.y() - self.point1.y()
        self.length = (dx**2 + dy**2)**0.5
