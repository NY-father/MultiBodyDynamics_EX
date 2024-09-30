from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class LoadDialog(QDialog):
    def __init__(self, joint, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Apply Load")
        self.joint = joint

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Applying torque to Joint between Body 1 and Body 2 at position ({joint.position.x():.2f}, {joint.position.y():.2f})"))

        # Torque input
        self.torque_input = QLineEdit("0.0")
        layout.addWidget(QLabel("Torque (Nm):"))
        layout.addWidget(self.torque_input)

        # OK and Cancel buttons
        buttons_layout = QVBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_torque(self):
        return float(self.torque_input.text())
