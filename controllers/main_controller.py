from model.function_model import FunctionModel
from utils.plotter import Plotter
from utils.toastr import Toast
from PySide2.QtCore import Qt, QTimer

class MainController:
    def __init__(self, view):
        self.view = view
        self.setup_connections()
        
        self.plotter = Plotter(self.view.canvas,2)
        self.toast = Toast.get_instance(self.view)
        
    def setup_connections(self):
        self.view.solve_button.clicked.connect(self.on_solve_clicked)
        self.view.clear_button.clicked.connect(self.on_clear_clicked)
        
    def on_solve_clicked(self):
        expr1 = self.view.input1.text()
        expr2 = self.view.input2.text()

        try:
            #! Show loading
            self.view.loading_overlay.show_loading()
            #! Use QTimer to allow UI to update before computation
            QTimer.singleShot(100, lambda: self._solve(expr1, expr2))
            
        except Exception as e:
            self.view.loading_overlay.hide_loading()
            self.view.show_success("❌ " + str(e))

    def _solve(self, expr1, expr2):
        try:
            fx = FunctionModel(expr1)
            gx = FunctionModel(expr2)
            solutions = fx.solve_with(gx)
            self.plotter.plot(fx, gx, solutions)
            
            
            self.view.update_solutions(solutions)
            if solutions:
                self.toast.show_success(f"✓ Found {len(solutions)} intersection point(s)")
            else:
                self.toast.show_danger("No real solutions were found")
                
        except Exception as e:
            self.toast.show_danger("❌ " + str(e))
        finally:
            self.view.loading_overlay.hide_loading()
            
    def on_clear_clicked(self):
        self.plotter.clear_canvas()
        self.view.input1.clear()
        self.view.input2.clear()
        self.view.solutions_label.setText("")
        print("Hello from clear button!")