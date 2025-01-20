from model.function_model import FunctionModel
from utils.plotter import plot_functions,Plotter

class MainController:
    def __init__(self, view):
        self.view = view
        self.setup_connections()
        #! No dependency injection sadly
        self.plotter = Plotter(self.view.canvas)
        
    def setup_connections(self):
        self.view.solve_button.clicked.connect(self.on_solve_clicked)
        self.view.clear_button.clicked.connect(self.on_clear_clicked)
        
    def on_solve_clicked(self):
        expr1 = self.view.input1.text()
        expr2 = self.view.input2.text()

        try:
            fx = FunctionModel(expr1)
            gx = FunctionModel(expr2)
            solutions = fx.solve_with(gx)
            print(solutions)
            self.plotter.plot(fx, gx, solutions)
        except Exception as e:
            self.view.show_error(str(e))
            
    def on_clear_clicked(self):
        self.plotter.clear_canvas()
        # Clear the input fields
        self.view.input1.clear()
        self.view.input2.clear()
        print("Hello from clear button!")