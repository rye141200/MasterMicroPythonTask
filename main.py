import sys
from PySide2.QtWidgets import QApplication
from views.main_view import MainView
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    
    # Initialize MVC components
    view = MainView()
    controller = MainController(view)
    
    # Show the GUI
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()