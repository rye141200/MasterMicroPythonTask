import numpy as np
from sympy import lambdify
from model.function_model import FunctionModel

class Plotter:
    def __init__(self,canvas):
        self.canvas = canvas
        
    def clear_canvas(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)  
        ax.grid(True, linestyle='--', alpha=0.7)  
        self.canvas.draw()  
        
    def plot(self, fx, gx, solutions):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
    
        f1 = lambdify(fx.x, fx.expression, modules=['numpy', {'log': np.log, 'sqrt': np.sqrt}])
        f2 = lambdify(gx.x, gx.expression, modules=['numpy', {'log': np.log, 'sqrt': np.sqrt}])
    
        combined_expr = str(fx.expression) + str(gx.expression)
        
        
        if 'log' in combined_expr or 'sqrt' in combined_expr:
            x_min = 0.0001
        else:
            x_min = -10
            
        x_max = max(10, max(solutions) + 2) if solutions else 10
        x_vals = np.linspace(x_min, x_max, 1000)
    
        try:
            y1_vals = f1(x_vals)
            y2_vals = f2(x_vals)
    
            # Plot with proper labels
            ax.plot(x_vals, y1_vals, label=f'f(x) = {fx.expression}')
            ax.plot(x_vals, y2_vals, label=f'g(x) = {gx.expression}')
    
            # Add intersection points without labels
            if solutions:
                for sol in solutions:
                    try:
                        y_val1 = float(f1(float(sol)))
                        y_val2 = float(f2(float(sol)))
                        y_val = (y_val1 + y_val2) / 2
                        ax.scatter([sol], [y_val], color='red', zorder=5, s=100)
                    except Exception as e:
                        print(f"Error plotting solution {sol}: {e}")
                        continue
                    
            # Calculate y range based on visible area
            y_vals = np.concatenate([y1_vals[~np.isnan(y1_vals)], y2_vals[~np.isnan(y2_vals)]])
            y_vals = y_vals[~np.isinf(y_vals)]  # Remove infinities
            if len(y_vals) > 0:
                y_min, y_max = np.min(y_vals), np.max(y_vals)
                margin = (y_max - y_min) * 0.1
                ax.set_ylim(y_min - margin, y_max + margin)
    
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