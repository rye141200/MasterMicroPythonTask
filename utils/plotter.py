import numpy as np
from sympy import lambdify
from model.function_model import FunctionModel
import traceback
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class Plotter:
    def __init__(self, canvas, precision=2):
        self.canvas = canvas
        self.precision = precision
        self.current_zoom_level = None  # Initialize to None to detect first plot
        self.zoom_ranges = [
            (-10, 10),     # Default view
            (-25, 25),     # First zoom out
            (-50, 50),     # Second zoom out
            (-100, 100),   # Third zoom out
            (-200, 200)    # Maximum zoom out
        ]
        # Enable mouse wheel zooming
        self.canvas.figure.canvas.mpl_connect('scroll_event', self.on_scroll)
        
    def on_scroll(self, event):
        # Check if we have functions to plot
        if not hasattr(self, 'current_fx') or not hasattr(self, 'current_gx'):
            return
                
        # Update zoom level based on scroll direction
        if event.button == 'up':  # Zoom in
            self.current_zoom_level = max(0, self.current_zoom_level - 1)
        elif event.button == 'down':  # Zoom out
            self.current_zoom_level = min(len(self.zoom_ranges) - 1, self.current_zoom_level + 1)
        
        # Get new range and replot
        x_min, x_max = self.zoom_ranges[self.current_zoom_level]
        self.plot(self.current_fx, self.current_gx, self.current_solutions, x_min, x_max)
        
    def clear_canvas(self):
        self.canvas.figure.clear()
        
        for ax in self.canvas.figure.axes[:]:
            self.canvas.figure.delaxes(ax)

        self.canvas.draw_idle()  
        
    def plot(self, fx, gx, solutions, x_min=None, x_max=None):
        # Store current functions and solutions for redrawing
        self.current_fx = fx
        self.current_gx = gx
        self.current_solutions = solutions
        
        # If no range specified, calculate from solutions
        if x_min is None or x_max is None:
            x_min = min(solutions) - self.precision if solutions else -10
            x_max = max(solutions) + self.precision if solutions else 10
            
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
                       
        modules = ['numpy']
        
        f1 = lambdify(fx.x, fx.expression, modules=modules)
        f2 = lambdify(gx.x, gx.expression, modules=modules)
    
        combined_expr = str(fx.expression) + str(gx.expression)
        
        x_vals = np.linspace(float(x_min), float(x_max), 1000)

        try:
            y1_vals = f1(x_vals)
            y2_vals = f2(x_vals)
    
            # Plot functions
            ax.plot(x_vals, y1_vals, label=f'f(x) = {fx.expression}')
            ax.plot(x_vals, y2_vals, label=f'g(x) = {gx.expression}')
    
            # Add intersection points
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
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)
    
        except Exception as e:
            print(f"Error plotting functions: {e} ")
            traceback.print_exc()
    
        self.canvas.draw()