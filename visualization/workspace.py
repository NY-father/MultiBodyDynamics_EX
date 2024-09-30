from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPen, QBrush
from dataclasses import dataclass
from dynamics.body import Body
from dynamics.joint import Joint
from dynamics.load import Load

@dataclass
class BodyItem:
    body: Body
    graphics: QGraphicsEllipseItem

class Workspace(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.current_mode = None  # 'body', 'joint', 'load'
        self.temp_points = []
        self.bodies = []
        self.joints = []
        self.loads = []

    def create_body_mode(self):
        self.current_mode = 'body'
        self.setDragMode(QGraphicsView.NoDrag)

    def create_joint_mode(self):
        self.current_mode = 'joint'
        self.setDragMode(QGraphicsView.NoDrag)

    def create_load_mode(self):
        self.current_mode = 'load'
        self.setDragMode(QGraphicsView.NoDrag)

    def mousePressEvent(self, event):
        if self.current_mode == 'body':
            pos = self.mapToScene(event.position().toPoint())
            self.temp_points.append(pos)
            # Draw temporary points
            self.scene.addEllipse(pos.x() - 5, pos.y() - 5, 10, 10, QPen(Qt.black), QBrush(Qt.red))
            if len(self.temp_points) == 2:
                self.create_body(self.temp_points[0], self.temp_points[1])
                self.temp_points = []
        elif self.current_mode == 'joint':
            pos = self.mapToScene(event.position().toPoint())
            print("joint: ", pos)
            # Implement joint creation logic
            self.select_bodies_for_joint(pos)
        elif self.current_mode == 'load':
            pos = self.mapToScene(event.position().toPoint())
            print("load: ", pos)
            # Implement load application logic
            self.select_joint_for_load(pos)
        else:
            super().mousePressEvent(event)

    def create_body(self, point1, point2):
        # Calculate center
        center_x = (point1.x() + point2.x()) / 2
        center_y = (point1.y() + point2.y()) / 2
        center = QPointF(center_x, center_y)

        # Add center marker
        marker = self.scene.addEllipse(center_x - 3, center_y - 3, 6, 6, QPen(Qt.blue), QBrush(Qt.blue))

        # Open dialog to input mass and inertia
        from gui.body_dialog import BodyDialog
        dialog = BodyDialog()
        if dialog.exec():
            mass, inertia = dialog.get_parameters()
            # Create Body object
            body = Body(point1, point2, center, mass, inertia)
            # Create graphical representation
            line = self.scene.addLine(point1.x(), point1.y(), point2.x(), point2.y(), QPen(Qt.black))
            body_item = BodyItem(body, line)
            self.bodies.append(body_item)
            # Optionally, store marker
        else:
            # If canceled, remove temporary points and marker
            self.scene.removeItem(marker)
            # Remove the two temporary points
            for item in self.scene.items():
                if isinstance(item, QGraphicsEllipseItem) and item.rect().width() == 10:
                    self.scene.removeItem(item)

    def select_bodies_for_joint(self, pos):
        # Determine if click is near any body
        selected_bodies = []
        threshold = 10  # pixels
        for body_item in self.bodies:
            if self.distance(body_item.body.center, pos) < threshold:
                selected_bodies.append(body_item.body)
        if len(selected_bodies) >= 2:
            # Open JointDialog
            from gui.joint_dialog import JointDialog
            dialog = JointDialog([b.body for b in self.bodies])
            if dialog.exec():
                idx1, idx2 = dialog.get_selection()
                body1 = self.bodies[idx1].body
                body2 = self.bodies[idx2].body
                joint_position = pos  # Or compute based on bodies
                joint = Joint(body1, body2, joint_position)
                self.joints.append(joint)
                # Draw joint on workspace
                self.scene.addEllipse(joint_position.x() - 3, joint_position.y() - 3, 6, 6, QPen(Qt.green), QBrush(Qt.green))

    def select_joint_for_load(self, pos):
        # Determine if click is near any joint
        selected_joints = []
        threshold = 10  # pixels
        for joint in self.joints:
            if self.distance(joint.position, pos) < threshold:
                selected_joints.append(joint)
        if selected_joints:
            # Open LoadDialog
            from gui.load_dialog import LoadDialog
            dialog = LoadDialog(self.joints)
            if dialog.exec():
                joint_idx, torque = dialog.get_load()
                self.joints[joint_idx].torque = torque
                # Optionally, visualize the load
                self.scene.addLine(
                    self.joints[joint_idx].position.x(),
                    self.joints[joint_idx].position.y(),
                    self.joints[joint_idx].position.x() + torque,
                    self.joints[joint_idx].position.y(),
                    QPen(Qt.red)
                )
    def distance(self, point1, point2):
        return ((point1.x() - point2.x())**2 + (point1.y() - point2.y())**2)**0.5
