from model.function_model import FunctionModel
from utils.plotter import Plotter
from utils.toastr import Toast
from PySide2.QtCore import QTimer
import re

class MainController:
    def __init__(self, view):
        self.view = view
        self.setup_connections()
        
        self.plotter = Plotter(self.view.canvas,2)
        self.toast = Toast.get_instance(self.view)
        
    def setup_connections(self):
        self.view.solve_button.clicked.connect(self.on_solve_clicked)
        self.view.clear_button.clicked.connect(self.on_clear_clicked)
        
    def validate_expression(self, expr):
        """Validate function expression using regex"""
        #!1) Remove whitespace and handle minus signs
        expr = expr.replace(' ', '').replace('+-', '-').replace('-+', '-')
        
        #!2) Check for implicit multiplication (numbers directly before or after x)
        if re.search(r'\d[a-zA-Z]|[a-zA-Z]\d', expr):
            return False, "Use explicit multiplication (e.g., '3*x' or 'x*3' instead of '3x' or 'x3')"

        #!3) Check for invalid variables
        vars_used = set(re.findall(r'[a-zA-Z]+', expr)) - {'x', 'log', 'sqrt'}
        if vars_used:
            return False, f"Only variable 'x' is allowed. Found: {', '.join(vars_used)}"
        
        #!4) Check for balanced parentheses
        if expr.count('(') != expr.count(')'):
            return False, "Unbalanced parentheses"
            
        #!5) Check function names
        functions = re.findall(r'([a-zA-Z]+)\(', expr)
        invalid_funcs = [f for f in functions if f not in ['log', 'sqrt']]
        if invalid_funcs:
            return False, f"Only 'log' and 'sqrt' functions are allowed. Found: {', '.join(invalid_funcs)}"
        
        return True, ""

    def on_solve_clicked(self):
        expr1 = self.view.input1.text().strip()
        expr2 = self.view.input2.text().strip()

        #!1) Validate both expressions
        for expr, field_name in [(expr1, 'f(x)'), (expr2, 'g(x)')]:
            is_valid, error_msg = self.validate_expression(expr)
            if not is_valid:
                self.toast.show_danger(f"❌ Invalid {field_name}: {error_msg}")
                return

        try:
            #!2) Show loading
            self.view.loading_overlay.show_loading()
            
            #!3) Use QTimer to allow UI to update before computation
            QTimer.singleShot(100, lambda: self._solve(expr1, expr2))
            
        except Exception as e:
            self.view.loading_overlay.hide_loading()
            self.toast.show_danger("❌ " + str(e))

    def _solve(self, expr1, expr2):
        try:
            fx = FunctionModel(expr1)
            gx = FunctionModel(expr2)
            
            if fx.is_same_function(gx):
                #!1) Plot identical functions
                self.plotter.soft_reset()
                self.plotter.plot(fx, gx, [])  #* Empty solutions list since they're identical
                
                #!2) Update UI to show infinite solutions message
                self.view.solutions_label.setText("Infinite solutions were found, the two functions are the same")
                self.toast.show_success("✓ Functions are identical")
                return
            
            #!3) Normal case - find intersections
            solutions = fx.solve_with(gx)
            
            self.plotter.soft_reset()
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