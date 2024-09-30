from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PySide6.QtCore import Qt, QPointF, Signal
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
    # Define a custom signal to send status messages
    status_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.current_mode = None  # 'body', 'joint', 'load'
        self.temp_points = []
        self.bodies = []
        self.joints = []
        self.loads = []
        self.selected_bodies_for_joint = []
        self.selected_joint_for_load = None

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
        pos = self.mapToScene(event.position().toPoint())
        if self.current_mode == 'body':
            self.temp_points.append(pos)
            # Draw temporary points
            self.scene.addEllipse(pos.x() - 5, pos.y() - 5, 10, 10, QPen(Qt.black), QBrush(Qt.red))
            if len(self.temp_points) == 2:
                self.create_body(self.temp_points[0], self.temp_points[1])
                self.temp_points = []
            else:
                self.status_message.emit("Body Mode: Click the second point to complete the body.")
        elif self.current_mode == 'joint':
            self.select_bodies_for_joint(pos)
        elif self.current_mode == 'load':
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
            self.status_message.emit("Body created successfully. You can create more bodies or switch modes.")
        else:
            # If canceled, remove temporary points and marker
            self.scene.removeItem(marker)
            # Remove the two temporary points
            for item in self.scene.items():
                if isinstance(item, QGraphicsEllipseItem) and item.rect().width() == 10:
                    self.scene.removeItem(item)
            self.status_message.emit("Body creation canceled.")


    def select_bodies_for_joint(self, pos):
        # Determine if click is near any body center
        clicked_body = None
        threshold = 10  # pixels
        for body_item in self.bodies:
            if self.distance(body_item.body.center, pos) < threshold:
                clicked_body = body_item.body
                break
        if clicked_body and clicked_body not in self.selected_bodies_for_joint:
            self.selected_bodies_for_joint.append(clicked_body)
            # Highlight selected body
            marker = self.scene.addEllipse(
                clicked_body.center.x() - 6, clicked_body.center.y() - 6, 12, 12,
                QPen(Qt.green), QBrush(Qt.NoBrush)
            )
            clicked_body.selection_marker = marker
            if len(self.selected_bodies_for_joint) == 2:
                # Create joint between the two bodies
                self.create_joint(self.selected_bodies_for_joint[0], self.selected_bodies_for_joint[1])
                # Clear selections
                self.clear_joint_selection()
                self.status_message.emit("Joint created successfully.")
            else:
                self.status_message.emit("Joint Mode: Select another body to create a joint.")
        else:
            self.status_message.emit("Joint Mode: Click near a body center to select.")



    def select_bodies_for_joint(self, pos):
        # Determine if click is near any body center
        clicked_body = None
        threshold = 10  # pixels
        for body_item in self.bodies:
            if self.distance(body_item.body.center, pos) < threshold:
                clicked_body = body_item.body
                break
        if clicked_body and clicked_body not in self.selected_bodies_for_joint:
            self.selected_bodies_for_joint.append(clicked_body)
            # Highlight selected body
            marker = self.scene.addEllipse(
                clicked_body.center.x() - 6, clicked_body.center.y() - 6, 12, 12,
                QPen(Qt.green), QBrush(Qt.NoBrush)
            )
            clicked_body.selection_marker = marker
            if len(self.selected_bodies_for_joint) == 2:
                # Create joint between the two bodies
                self.create_joint(self.selected_bodies_for_joint[0], self.selected_bodies_for_joint[1])
                # Clear selections
                self.clear_joint_selection()
                self.status_message.emit("Joint created successfully.")
            else:
                self.status_message.emit("Joint Mode: Select the second body to create a joint.")
        else:
            if not clicked_body:
                self.status_message.emit("Joint Mode: Click near a body center to select.")
            else:
                self.status_message.emit("Joint Mode: Body already selected. Choose a different body.")



    def distance(self, point1, point2):
        return ((point1.x() - point2.x())**2 + (point1.y() - point2.y())**2)**0.5



    def create_joint(self, body1, body2):
        # Open JointDialog to specify joint properties
        from gui.joint_dialog import JointDialog
        dialog = JointDialog(body1, body2)
        if dialog.exec():
            joint_position = dialog.get_joint_position()
            joint_type = dialog.get_joint_type()
            # Create Joint object
            joint = Joint(body1, body2, joint_position, joint_type)
            self.joints.append(joint)
            # Draw joint on workspace
            joint_marker = self.scene.addEllipse(
                joint_position.x() - 3, joint_position.y() - 3, 6, 6,
                QPen(Qt.darkGreen), QBrush(Qt.darkGreen)
            )
            joint.graphics = joint_marker
            self.status_message.emit("Joint successfully created.")
        else:
            # User cancelled joint creation
            self.status_message.emit("Joint creation canceled.")


    def clear_joint_selection(self):
        for body in self.selected_bodies_for_joint:
            # Remove selection markers
            self.scene.removeItem(body.selection_marker)
            del body.selection_marker
        self.selected_bodies_for_joint = []


    def select_joint_for_load(self, pos):
        # Determine if click is near any joint
        clicked_joint = None
        threshold = 10  # pixels
        for joint in self.joints:
            if self.distance(joint.position, pos) < threshold:
                clicked_joint = joint
                break
        if clicked_joint:
            # Open LoadDialog to specify torque
            from gui.load_dialog import LoadDialog
            dialog = LoadDialog(clicked_joint)
            if dialog.exec():
                torque = dialog.get_torque()
                # Apply torque to joint
                clicked_joint.torque = torque
                # Visualize the load
                self.visualize_load_on_joint(clicked_joint)
                self.status_message.emit(f"Applied torque of {torque} Nm to the selected joint.")
            else:
                self.status_message.emit("Load Mode: Torque application canceled.")
        else:
            self.status_message.emit("Load Mode: Click near a joint to apply torque.")

    def visualize_load_on_joint(self, joint):
        # Change the joint marker color to indicate a load is applied
        joint.graphics.setBrush(QBrush(Qt.red))
        self.status_message.emit("Load visualized on the joint.")



    def set_mode(self, mode):
        self.current_mode = mode
        self.temp_points = []
        if mode == 'body':
            self.status_message.emit("Body Mode: Click two points to create a body.")
        elif mode == 'joint':
            self.status_message.emit("Joint Mode: Click on two bodies to create a joint.")
        elif mode == 'load':
            self.status_message.emit("Load Mode: Click on a joint to apply torque.")
        else:
            self.status_message.emit("Select a mode to begin.")

