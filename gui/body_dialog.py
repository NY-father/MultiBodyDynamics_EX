from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout

class BodyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Body Parameters")
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.mass_input = QLineEdit()
        self.inertia_input = QLineEdit()
        form_layout.addRow("Mass:", self.mass_input)
        form_layout.addRow("Moment of Inertia:", self.inertia_input)

        layout.addLayout(form_layout)

        buttons_layout = QVBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_parameters(self):
        mass = float(self.mass_input.text())
        inertia = float(self.inertia_input.text())
        return mass, inertia
