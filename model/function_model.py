from sympy import Interval, lambdify, symbols, solve, sympify,solve_univariate_inequality, S, oo
from scipy.optimize import fsolve
from sympy.calculus.util import continuous_domain
import numpy as np
import sympy as sp
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

class FunctionModel:
    def __init__(self, expression):
        self.x = symbols('x')
        expression = expression.replace('sqrt', 'sqrt')
        expression = expression.replace('log10', 'log')
        self.expression = sympify(expression)  # Converts string to symbolic math
        print(self.expression)
    
    def is_same_function(self,other_model):
        return self.expression == other_model.expression
    
    def solve_with(self, other_model):
        try:
            symbolic_sols = [sol for sol in solve(self.expression - other_model.expression, self.x) if sol.is_real]
            if symbolic_sols:
                return symbolic_sols
        except:
            pass
        
        #! Numeric solutions
        def equation(x):
            f1 = lambdify(self.x, self.expression, modules=['numpy', {'log10': np.log10}])
            f2 = lambdify(self.x, other_model.expression, modules=['numpy', {'log10': np.log10}])
            def diff(x):
                return f1(x) - f2(x)
            return diff(x)
        
        solutions = set()
        
        # **1. Adaptive range expansion**
        initial_range = np.linspace(0.1, 10, 100) 
        expanded_ranges = [initial_range]
        
        for scale in [10, 100, 1000]:
            expanded_ranges.append(np.linspace(scale, scale * 10, 50))
        
        x_samples = np.concatenate(expanded_ranges)
        
        # **2. Find sign changes for potential intersections**
        y_diff = equation(x_samples)
        sign_changes = np.where(np.diff(np.sign(y_diff)))[0]
        
        if len(sign_changes) > 0:
            x_range = np.concatenate([
                np.linspace(x_samples[idx], x_samples[idx + 1], 50)
                for idx in sign_changes
            ])
        else:
            x_range = np.linspace(0.1, 1000, 500) 

        
        #! Use this in case of messed up code
        """ # More focused sampling around potential solution areas
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
        
        x_range = np.concatenate(x_ranges) """
        
        for x0 in x_range:
            try:
                sol = fsolve(equation, x0, xtol=1e-8)[0]
                if abs(equation(sol)) < 1e-7 and not np.isnan(sol):
                    solutions.add(round(float(sol), 6))
            except:
                continue

        return sorted(list(solutions))