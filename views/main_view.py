from PySide2.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                               QFrame,QLabel,QMessageBox)
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.stylesheet import Styles
from utils.toastr import Toast
from utils.ui_components import ComponentFactory, LoadingOverlay

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ComponentFactory = ComponentFactory()
        # self.Styles = Styles("100",'10')
        self.init_ui()
        self.loading_overlay = LoadingOverlay(self)

    def show_success(self, message):
        toast = Toast.get_instance(self)
        toast.show_message(message)

    def update_solutions(self, solutions):
        if solutions:
            solutions_text = "Solutions: " + ", ".join([f"x = {float(sol)}" for sol in solutions])
            self.solutions_label.setText(solutions_text)
        else:
            self.solutions_label.setText("No intersections found")
            
    def init_ui(self):
        self.setWindowTitle("MasterMicro Internship assessment (Two Functions Solver)")
        self.setGeometry(100, 100, 1000, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        #! Left sidebar
        (sidebar,sidebar_layout) = self.ComponentFactory.initialize_side_bar()

        self.input1 = self.ComponentFactory.initialize_text_input_component("Enter f(x)")
        
        self.input2 = self.ComponentFactory.initialize_text_input_component("Enter g(x)")

        self.solve_button = self.ComponentFactory.initialize_button("Solve")
        
        self.clear_button = self.ComponentFactory.initialize_button("Clear",True)
        
        
        # Add widgets to sidebar
        self.ComponentFactory.add_widgets_to_parent(sidebar_layout,[self.input1,self.input2,self.solve_button,self.clear_button])
        
        # Add stretch to push logo to bottom
        sidebar_layout.addStretch()
        
        # Add logo at the bottom of sidebar
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/mastermicrologo.png")
        scaled_pixmap = logo_pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        # Right side - Graph area
        graph_container = QFrame()
        graph_layout = QVBoxLayout(graph_container)
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        graph_layout.addWidget(self.canvas)

        # Add sidebar and graph to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(graph_container, stretch=1)
        
        #! Solutions box
        self.solutions_label = self.ComponentFactory.initialize_solutions_label_box()
        graph_layout.addWidget(self.solutions_label)