import numpy as np
from sympy import lambdify
from model.function_model import FunctionModel

def plot_functions(canvas, model1, model2, solutions):
    canvas.figure.clear()
    ax = canvas.figure.add_subplot(111)
    
    # Convert sympy expressions to numpy functions
    f1 = lambdify(model1.x, model1.expression, 'numpy')
    f2 = lambdify(model2.x, model2.expression, 'numpy')
    
    x_vals = np.linspace(-10, 10, 500)
    
    try:
        # Evaluate functions using numpy
        y1_vals = f1(x_vals)
        y2_vals = f2(x_vals)
        
        # Plot with proper labels
        ax.plot(x_vals, y1_vals, label=f'f(x) = {model1.expression}')
        ax.plot(x_vals, y2_vals, label=f'g(x) = {model2.expression}')

        # Add intersection points
        for sol in solutions:
            ax.scatter([sol], [f1(sol)], color='red')

        # Enable autoscaling
        ax.autoscale(True)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
    except Exception as e:
        print(f"Error plotting functions: {e}")
    
    canvas.draw()