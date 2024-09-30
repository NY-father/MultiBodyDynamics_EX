from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit

class LoadDialog(QDialog):
    def __init__(self, joints, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Apply Load")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select Joint:"))
        self.joint_list = QListWidget()
        for i, joint in enumerate(joints):
            self.joint_list.addItem(f"Joint {i+1}")
        layout.addWidget(self.joint_list)

        layout.addWidget(QLabel("Torque:"))
        self.torque_input = QLineEdit()
        layout.addWidget(self.torque_input)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_load(self):
        joint_index = self.joint_list.currentRow()
        torque = float(self.torque_input.text())
        return joint_index, torque

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
