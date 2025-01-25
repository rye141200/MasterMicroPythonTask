from sympy import lambdify, symbols, solve, sympify
from scipy.optimize import fsolve, newton, bisect
import numpy as np
class FunctionModel:
    def __init__(self, expression):
        self.x = symbols('x')
        expression = expression.replace('sqrt', 'sqrt')
        expression = expression.replace('log10', 'log')
        self.expression = sympify(expression)  # Converts string to symbolic math
        print(self.expression)

          
    
    def solve_with(self, other_model):
        try:
            # Try symbolic solution first
            symbolic_sols = [sol for sol in solve(self.expression - other_model.expression, self.x) if sol.is_real]
            if symbolic_sols:
                return symbolic_sols
        except:
            pass
        
        def equation(x):
            # Create lambdify functions once outside the loop
            f1 = lambdify(self.x, self.expression, modules=['numpy', {'log10': np.log10}])
            f2 = lambdify(self.x, other_model.expression, modules=['numpy', {'log10': np.log10}])
            def diff(x):
                return f1(x) - f2(x)
            return diff(x)
        
        solutions = set()
        
        # More focused sampling around potential solution areas
        x_ranges = []
        if 'log' in str(self.expression) or 'log' in str(other_model.expression):
            x_ranges.extend([
                np.linspace(0.0001, 0.1, 20),   # Very dense near zero
                np.linspace(0.1, 2, 50),        # Dense around 1
                np.linspace(2, 10, 30)          # Less dense for larger values
            ])
        else:
            x_ranges.extend([
                np.linspace(0, 2, 50),          # Dense around common solution areas
                np.linspace(2, 10, 30)          # Less dense for larger values
            ])
        
        x_range = np.concatenate(x_ranges)
        
        # Try numerical method with better tolerance
        for x0 in x_range:
            try:
                sol = fsolve(equation, x0, xtol=1e-8)[0]
                if abs(equation(sol)) < 1e-7 and not np.isnan(sol):
                    solutions.add(round(float(sol), 6))
            except:
                continue

        return sorted(list(solutions))