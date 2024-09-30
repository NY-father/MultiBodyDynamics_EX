from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox
from PySide6.QtCore import QPointF

class JointDialog(QDialog):
    def __init__(self, body1, body2, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Joint")
        self.body1 = body1
        self.body2 = body2

        layout = QVBoxLayout()

        # Display body information
        layout.addWidget(QLabel(f"Connecting Body 1 at center ({body1.center.x():.2f}, {body1.center.y():.2f})"))
        layout.addWidget(QLabel(f"with Body 2 at center ({body2.center.x():.2f}, {body2.center.y():.2f})"))

        # Joint type selection
        self.joint_type_combo = QComboBox()
        self.joint_type_combo.addItems(["Hinge", "Slider", "Fixed"])
        layout.addWidget(QLabel("Select Joint Type:"))
        layout.addWidget(self.joint_type_combo)

        # Joint position inputs
        form_layout = QFormLayout()
        self.position_x_input = QLineEdit(str((body1.center.x() + body2.center.x()) / 2))
        self.position_y_input = QLineEdit(str((body1.center.y() + body2.center.y()) / 2))
        form_layout.addRow("Joint Position X:", self.position_x_input)
        form_layout.addRow("Joint Position Y:", self.position_y_input)

        layout.addLayout(form_layout)

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

    def get_joint_position(self):
        x = float(self.position_x_input.text())
        y = float(self.position_y_input.text())
        return QPointF(x, y)

    def get_joint_type(self):
        return self.joint_type_combo.currentText()
