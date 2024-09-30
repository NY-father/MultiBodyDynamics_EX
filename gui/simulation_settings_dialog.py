from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout

class SimulationSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulation Settings")
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.time_step_input = QLineEdit("0.01")
        self.duration_input = QLineEdit("10.0")
        form_layout.addRow("Time Step:", self.time_step_input)
        form_layout.addRow("Duration:", self.duration_input)

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

    def get_settings(self):
        time_step = float(self.time_step_input.text())
        duration = float(self.duration_input.text())
        return {'time_step': time_step, 'duration': duration}
