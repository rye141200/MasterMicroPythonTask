from PySide2.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                              QPushButton, QLineEdit, QFrame)
from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.stylesheet import Styles

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Styles = Styles("100",'10')
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MasterMicro Internship assessment (Two Functions Solver)")
        self.setGeometry(100, 100, 1000, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left sidebar
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)

        # Input fields with labels
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Enter f(x)")
        self.input1.setStyleSheet(self.Styles.get_text_input_style())

        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Enter g(x)")
        self.input2.setStyleSheet(self.Styles.get_text_input_style())

        #! Solve button
        self.solve_button = QPushButton("Solve")
        self.solve_button.setStyleSheet(self.Styles.get_green_button_style())
        
        
        #! Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet(self.Styles.get_danger_button_style())
        
        
        
        self.solve_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Add widgets to sidebar
        sidebar_layout.addWidget(self.input1)
        sidebar_layout.addWidget(self.input2)
        sidebar_layout.addWidget(self.solve_button)
        sidebar_layout.addWidget(self.clear_button)
        sidebar_layout.addStretch()

        # Right side - Graph area
        graph_container = QFrame()
        graph_layout = QVBoxLayout(graph_container)
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        graph_layout.addWidget(self.canvas)

        # Add sidebar and graph to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(graph_container, stretch=1)