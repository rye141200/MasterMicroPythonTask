from model.function_model import FunctionModel
from utils.plotter import plot_functions

class MainController:
    def __init__(self, view):
        self.view = view
        self.setup_connections()

    def setup_connections(self):
        self.view.solve_button.clicked.connect(self.on_solve_clicked)

    def on_solve_clicked(self):
        expr1 = self.view.input1.text()
        expr2 = self.view.input2.text()

        try:
            model1 = FunctionModel(expr1)
            model2 = FunctionModel(expr2)
            solutions = model1.solve_with(model2)
            print(solutions)
            plot_functions(self.view.canvas, model1, model2, solutions)
        except Exception as e:
            self.view.show_error(str(e))