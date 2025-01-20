import numpy as np
from sympy import lambdify
from model.function_model import FunctionModel

class Plotter:
    def __init__(self,canvas):
        self.canvas = canvas
        
    def clear_canvas(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)  # Re-add the subplot
        ax.grid(True, linestyle='--', alpha=0.7)  # Re-add the grid
        self.canvas.draw()  # Redraw the canvas
        
    def plot(self,fx,gx,solutions):
        self.canvas.figure.clear()
        
        ax = self.canvas.figure.add_subplot(111)
    
        # Convert sympy expressions to numpy functions
        f1 = lambdify(fx.x, fx.expression, 'numpy')
        f2 = lambdify(gx.x, gx.expression, 'numpy')

        x_vals = np.linspace(-10, 10, 500)

        try:
            # Evaluate functions using numpy
            y1_vals = f1(x_vals)
            y2_vals = f2(x_vals)

            # Plot with proper labels
            ax.plot(x_vals, y1_vals, label=f'f(x) = {fx.expression}')
            ax.plot(x_vals, y2_vals, label=f'g(x) = {gx.expression}')

            # Add intersection points
            for sol in solutions:
                ax.scatter([sol], [f1(sol)], color='red')

            # Enable autoscaling
            ax.autoscale(True)
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)

        except Exception as e:
            print(f"Error plotting functions: {e}")

        self.canvas.draw() 
   
def plot_functions(canvas, fx, gx, solutions):
    canvas.figure.clear()
    ax = canvas.figure.add_subplot(111)
    
    # Convert sympy expressions to numpy functions
    f1 = lambdify(fx.x, fx.expression, 'numpy')
    f2 = lambdify(gx.x, gx.expression, 'numpy')
    
    x_vals = np.linspace(-10, 10, 500)
    
    try:
        # Evaluate functions using numpy
        y1_vals = f1(x_vals)
        y2_vals = f2(x_vals)
        
        # Plot with proper labels
        ax.plot(x_vals, y1_vals, label=f'f(x) = {fx.expression}')
        ax.plot(x_vals, y2_vals, label=f'g(x) = {gx.expression}')

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