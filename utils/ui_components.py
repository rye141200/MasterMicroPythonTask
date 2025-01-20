from utils.stylesheet import Styles
from PySide2.QtWidgets import QLineEdit,QPushButton,QFrame,QVBoxLayout
from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor

class ComponentFactory:
    def __init__(self,border_radius="100",margin="10"):
        self.Styles = Styles(border_radius,margin)
    
    def initialize_text_input_component(self,placeholder):
        text_input = QLineEdit()
        text_input.setPlaceholderText(placeholder)
        text_input.setStyleSheet(self.Styles.get_text_input_style())
        return text_input
    
    def initialize_button(self,text, danger = False):
        button = QPushButton(text)
        button.setStyleSheet(self.Styles.get_danger_button_style() if danger 
        else self.Styles.get_green_button_style())
        button.setCursor(QCursor(Qt.PointingHandCursor))
        return button
    
    def initialize_side_bar(self,width=250):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(width)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        return (sidebar,sidebar_layout)
    
    def add_widgets_to_parent(self,parent,widgets):
        for widget in widgets:
            parent.addWidget(widget)
        
    