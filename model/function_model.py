from sympy import symbols, solve, sympify

class FunctionModel:
    def __init__(self, expression):
        self.x = symbols('x')
        expression = expression.replace('sqrt', 'sqrt')
        expression = expression.replace('log10', 'log')
        self.expression = sympify(expression)  # Converts string to symbolic math
        print(self.expression)

    def solve_with(self, other_model):
        return [
        solution 
        for solution in solve(self.expression - other_model.expression, self.x)
        if solution.is_real]