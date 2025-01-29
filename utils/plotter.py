import numpy as np
from sympy import lambdify
from model.function_model import FunctionModel
import traceback
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from PySide2.QtWidgets import QToolButton

class Plotter:
    def __init__(self, canvas, zoom=2, zoom_offset=5, max_zoom_level=5, min_zoom_level=0):
        self.canvas = canvas
        self.zoom = zoom
        self.zoom_offset = zoom_offset
        self.current_zoom_level = 0
        self.max_zoom_level = max_zoom_level
        self.min_zoom_level = min_zoom_level
        
        # Create toolbar but hide it initially
        self.toolbar = NavigationToolbar2QT(self.canvas, self.canvas.parent())
        self.toolbar.setVisible(False)  # Hide entire toolbar initially
        
        # Hide all buttons except Save
        for action in self.toolbar.actions():
            if action.text() != 'Save':
                action.setVisible(False)
            else:
                self.save_action = action  # Store reference to save action
                self.save_action.setVisible(False)  # Hide save button initially
        
        # Connect scroll event
        self.canvas.figure.canvas.mpl_connect('scroll_event', self.on_scroll)
    
    def soft_reset(self):
        self.current_zoom_level = 0

    def on_scroll(self, event):
        if not hasattr(self, 'current_fx') or not hasattr(self, 'current_gx'):
            return
                
        # Update zoom level based on scroll direction
        if event.button == 'up':  # Zoom in
            self.current_zoom_level = max(self.min_zoom_level, self.current_zoom_level - 1)
        elif event.button == 'down':  # Zoom out
            self.current_zoom_level = min(self.max_zoom_level, self.current_zoom_level + 1)
            
        self.plot(self.current_fx, self.current_gx, self.current_solutions)
        
    def clear_canvas(self):
        # Hide save button when clearing
        self.toolbar.setVisible(False)
        self.save_action.setVisible(False)
        
        self.canvas.figure.clear()
        
        for ax in self.canvas.figure.axes[:]:
            self.canvas.figure.delaxes(ax)

        self.canvas.draw_idle()  
        
    def plot(self, fx, gx, solutions):
        try:
            # Store current functions and solutions for redrawing
            self.current_fx = fx
            self.current_gx = gx
            self.current_solutions = solutions
            
            if solutions:
                self.default_range = (
                    min(solutions) - self.zoom,
                    max(solutions) + self.zoom
                )
            else:
                self.default_range = (-10, 10)

            x_min = self.default_range[0] - self.zoom_offset ** self.current_zoom_level
            x_max = self.default_range[1] + self.zoom_offset ** self.current_zoom_level
                
            self.clear_canvas()
            ax = self.canvas.figure.add_subplot(111)
                           
            modules = ['numpy']
            
            f1 = lambdify(fx.x, fx.expression, modules=modules)
            f2 = lambdify(gx.x, gx.expression, modules=modules)
            
            x_vals = np.linspace(float(x_min), float(x_max), 1000)

            y1_vals = f1(x_vals)
            y2_vals = f2(x_vals)

            # Plot functions
            ax.plot(x_vals, y1_vals, label=f'f(x) = {fx.expression}')
            ax.plot(x_vals, y2_vals, label=f'g(x) = {gx.expression}')
            ax.set_xlabel("x")
            
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
            self.canvas.draw()
            
            # Show toolbar and save button only after successful plot
            self.toolbar.setVisible(True)
            self.save_action.setVisible(True)
            
        except Exception as e:
            print(f"Error plotting functions: {e}")
            traceback.print_exc()
            # Hide toolbar and save button if plot fails
            self.toolbar.setVisible(False)
            self.save_action.setVisible(False)