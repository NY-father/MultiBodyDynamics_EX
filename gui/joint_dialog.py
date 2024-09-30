from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QLabel

class JointDialog(QDialog):
    def __init__(self, bodies, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Joint")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select Body 1:"))
        self.body1_list = QListWidget()
        for i, body in enumerate(bodies):
            self.body1_list.addItem(f"Body {i+1}")
        layout.addWidget(self.body1_list)

        layout.addWidget(QLabel("Select Body 2:"))
        self.body2_list = QListWidget()
        for i, body in enumerate(bodies):
            self.body2_list.addItem(f"Body {i+1}")
        layout.addWidget(self.body2_list)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_selection(self):
        body1_index = self.body1_list.currentRow()
        body2_index = self.body2_list.currentRow()
        return body1_index, body2_index
