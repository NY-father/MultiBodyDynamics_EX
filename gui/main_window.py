from PySide6.QtWidgets import QMainWindow, QPushButton, QGraphicsView, QVBoxLayout, QWidget, QToolBar
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

        # Connect signals
        self.body_button.clicked.connect(self.workspace.create_body_mode)
        self.joint_button.clicked.connect(self.workspace.create_joint_mode)
        self.load_button.clicked.connect(self.workspace.create_load_mode)
        self.run_button.clicked.connect(self.run_simulation)

    def run_simulation(self):
        # Open simulation settings dialog
        from gui.simulation_settings_dialog import SimulationSettingsDialog
        dialog = SimulationSettingsDialog(self)
        if dialog.exec():
            settings = dialog.get_settings()
            # Pass settings to simulation module
            from dynamics.simulation import Simulation
            simulation = Simulation(settings)
            simulation.run()
