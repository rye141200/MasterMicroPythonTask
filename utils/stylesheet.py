from PySide2.QtCore import QPropertyAnimation, QEasingCurve, Property, QPoint

class Styles:
    def __init__(self,border_radius,margin):
        self.border_radius = border_radius
        self.margin = margin
    def setup_button_animation(self, button):
        # Create a unique animation instance for each button
        button.scale_anim = QPropertyAnimation(button, b"geometry")
        button.scale_anim.setDuration(300)
        button.scale_anim.setEasingCurve(QEasingCurve.InOutQuad)

        def on_hover(event):
            rect = button.geometry()
            center = rect.center()
            rect.setWidth(int(rect.width() * 1.1))
            rect.setHeight(int(rect.height() * 1.1))
            rect.moveCenter(center)
            button.scale_anim.setEndValue(rect)
            button.scale_anim.start()

        def on_leave(event):
            rect = button.geometry()
            center = rect.center()
            rect.setWidth(int(rect.width() / 1.1))
            rect.setHeight(int(rect.height() / 1.1))
            rect.moveCenter(center)
            button.scale_anim.setEndValue(rect)
            button.scale_anim.start()

        button.enterEvent = on_hover
        button.leaveEvent = on_leave
    def get_green_button_style(self):
        return f"""
            QPushButton {{
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: {self.border_radius}px;
                border: none;
                margin: {self.margin}px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #45a049;
            }}
        """
    def get_danger_button_style(self):
        return f"""
            QPushButton {{
                background-color: #ff4444;
                color: white;
                padding: 8px 16px;
                border-radius: {self.border_radius}px;
                border: none;
                margin: {self.margin}px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: #ff1a1a;
            }}
        """