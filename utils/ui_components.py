from utils.stylesheet import Styles
from PySide2.QtWidgets import QLineEdit,QPushButton,QFrame,QVBoxLayout, QLabel, QWidget
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QCursor, QPalette, QColor

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
    
    def initialize_solutions_label_box(self):
        solutions_label = QLabel()
        solutions_label.setStyleSheet(self.Styles.get_solutions_label_style())
        return solutions_label
    
    def add_widgets_to_parent(self,parent,widgets):
        for widget in widgets:
            parent.addWidget(widget)

class LoadingOverlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 100))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.hide()
        
        # Create loading label
        self.loading_label = QLabel("Calculating...", self)
        self.loading_label.setStyleSheet("""
            QLabel {
                color: white;
                padding: 20px;
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 10px;
                font-size: 16px;
            }
        """)
        
    def showEvent(self, event):
        self.resize(self.parent().size())
        self.loading_label.move(
            self.width()//2 - self.loading_label.width()//2,
            self.height()//2 - self.loading_label.height()//2
        )

    def show_loading(self):
        self.show()
        QTimer.singleShot(100, lambda: self.raise_())
        
    def hide_loading(self):
        self.hide()