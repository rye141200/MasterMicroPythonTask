from PySide2.QtWidgets import QLabel, QGraphicsOpacityEffect
from PySide2.QtCore import QTimer, QPropertyAnimation
from .stylesheet import Styles
class Toast(QLabel):
    _instance = None
    
    @classmethod
    def get_instance(cls, parent):
        if cls._instance is None:
            cls._instance = cls(parent)
        elif cls._instance.parent != parent:
            # Update parent if needed
            cls._instance.setParent(parent)
        return cls._instance
    
    def show_success(self, message):
        self.setStyleSheet(Styles.get_success_toastr_style())
        self.show_message(message)
    
    def show_danger(self,message):
        self.setStyleSheet(Styles.get_danger_toastr_style())
        self.show_message(message)
        
        
    def __init__(self, parent):
        if Toast._instance is not None:
            raise Exception("Toast is a singleton! Use get_instance() instead.")
            
        super().__init__(parent)
        self.parent = parent

        
        # Setup fade animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(300)
        Toast._instance = self
        
    def show_message(self, message, duration=3000):
        # Reset opacity
        self.opacity_effect.setOpacity(1.0)
        
        # Update text and position
        self.setText(message)
        self.adjustSize()
        parent_rect = self.parent.rect()
        self.move(
            parent_rect.width() - self.width() - 20,
            20
        )
        
        # Show and start timer
        self.show()
        QTimer.singleShot(duration, self.fade_out)
    
    def fade_out(self):
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.finished.connect(self.hide)  # Hide the toast when animation finishes
        self.fade_anim.start()