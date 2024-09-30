from PySide6.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QVBoxLayout, QWidget, QToolBar, QStatusBar
from PySide6.QtCore import Qt
from visualization.workspace import Workspace

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multibody Dynamics Simulator")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Add buttons
        self.body_button = QPushButton("Body")
        self.joint_button = QPushButton("Joint")
        self.load_button = QPushButton("Load")
        self.run_button = QPushButton("Run")

        toolbar.addWidget(self.body_button)
        toolbar.addWidget(self.joint_button)
        toolbar.addWidget(self.load_button)
        toolbar.addWidget(self.run_button)

        # Initialize workspace
        self.workspace = Workspace()
        self.setCentralWidget(self.workspace)

        # Initialize status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Select a mode to begin.")

        # Connect signals
        self.body_button.clicked.connect(lambda: self.workspace.set_mode('body'))
        self.joint_button.clicked.connect(lambda: self.workspace.set_mode('joint'))
        self.load_button.clicked.connect(lambda: self.workspace.set_mode('load'))
        self.run_button.clicked.connect(self.run_simulation)

        # Connect Workspace signals to status bar
        self.workspace.status_message.connect(self.update_status_bar)

    def update_status_bar(self, message):
        self.status_bar.showMessage(message)

    def run_simulation(self):
        # Open simulation settings dialog
        from gui.simulation_settings_dialog import SimulationSettingsDialog
        dialog = SimulationSettingsDialog(self)
        if dialog.exec():
            settings = dialog.get_settings()
            # Pass settings to simulation module
            from dynamics.simulation import Simulation
            simulation = Simulation(settings, self.workspace.bodies, self.workspace.joints, self.workspace.loads)
            simulation.run()
