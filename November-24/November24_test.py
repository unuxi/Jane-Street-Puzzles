#!/usr/bin/env python3
"""
Geometric Probability Visualization Tool

This script provides an interactive visualization for a geometric probability problem
where two random points are selected in a unit square, and we need to find the
probability that there exists a point on the square's edge (closest to the blue point)
that is equidistant to both points.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import quad

class GeometricProbabilityVisualizer:
    def __init__(self):
        """Initialize the visualization tool with default parameters."""
        # Square coordinates
        self.square_x = [0, 1, 1, 0, 0]
        self.square_y = [0, 0, 1, 1, 0]
        
        # Triangle coordinates (valid region for blue point)
        self.triangle_x = [0, 1, 0.5]
        self.triangle_y = [0, 0, 0.5]
        
        # Initialize plot elements
        self.current_point = None
        self.random_point = None
        self.intersection_point = None
        self.quarter_circle_patches = []
        self.lines = []
        
        self.setup_plot()
        
    def setup_plot(self):
        """Set up the matplotlib figure and axes with initial elements."""
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        
        # Draw square
        self.ax.plot(self.square_x, self.square_y, 'k-')
        
        # Draw and fill triangle
        self.ax.plot(self.triangle_x + [self.triangle_x[0]], 
                    self.triangle_y + [self.triangle_y[0]], 'b-')
        self.ax.fill(self.triangle_x, self.triangle_y, 'b', alpha=0.3)
        
        # Configure axes
        self.ax.set_xlim(-0.1, 1.1)
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('Click inside the Triangle to set a point')
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.grid(True)
        
        # Connect click event
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    @staticmethod
    def is_inside_triangle(x, y, triangle_coords):
        """
        Check if a point (x, y) lies inside the given triangle.
        
        Args:
            x (float): x-coordinate of the point
            y (float): y-coordinate of the point
            triangle_coords (list): List of (x, y) coordinates of triangle vertices
            
        Returns:
            bool: True if point is inside triangle, False otherwise
        """
        x1, y1 = triangle_coords[0]
        x2, y2 = triangle_coords[1]
        x3, y3 = triangle_coords[2]

        denominator = ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
        if denominator == 0:
            return False
            
        a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / denominator
        b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / denominator
        c = 1 - a - b

        return (0 <= a <= 1) and (0 <= b <= 1) and (0 <= c <= 1)

    @staticmethod
    def intersection_with_x_axis(p1, p2):
        """
        Calculate the intersection point of the perpendicular bisector with x-axis.
        
        Args:
            p1 (tuple): Coordinates of first point (x1, y1)
            p2 (tuple): Coordinates of second point (x2, y2)
            
        Returns:
            tuple: Coordinates of intersection point (x, 0)
        """
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
        
        if p1[0] == p2[0]:  # Vertical line case
            return p1[0], 0
            
        slope = -(p2[0] - p1[0]) / (p2[1] - p1[1])  # Perpendicular slope
        intercept = mid_y - slope * mid_x
        x_intercept = -intercept / slope
        return x_intercept, 0

    def clear_current_visualization(self):
        """Remove all current visualization elements."""
        if self.current_point is not None:
            self.current_point.remove()
            self.current_point = None
        if self.random_point is not None:
            self.random_point.remove()
            self.random_point = None
        if self.intersection_point is not None:
            self.intersection_point.remove()
            self.intersection_point = None
        
        for patch in self.quarter_circle_patches:
            patch.remove()
        self.quarter_circle_patches = []
        
        for line in self.lines:
            line.remove()
        self.lines = []

    def draw_quarter_circles(self, x_click, y_click):
        """
        Draw quarter circles from corner points through the clicked point.
        
        Args:
            x_click (float): x-coordinate of clicked point
            y_click (float): y-coordinate of clicked point
        """
        corner_coords = [(0, 0), (1, 0)]
        for corner in corner_coords:
            dx = x_click - corner[0]
            dy = y_click - corner[1]
            radius = np.sqrt(dx**2 + dy**2)
            start_angle = 0 if corner == (0, 0) else 90
            wedge = patches.Wedge(corner, radius, start_angle, 
                                start_angle + 90, facecolor='blue', alpha=0.3)
            self.ax.add_patch(wedge)
            self.quarter_circle_patches.append(wedge)

    def onclick(self, event):
        """Handle mouse click events within the plot."""
        if event.inaxes != self.ax:
            return
            
        x_click, y_click = event.xdata, event.ydata
        triangle_coords = [(self.triangle_x[i], self.triangle_y[i]) for i in range(3)]
        
        if not self.is_inside_triangle(x_click, y_click, triangle_coords):
            print("Click is outside the triangle.")
            return

        # Clear previous visualization
        self.clear_current_visualization()

        # Draw new blue point
        self.current_point, = self.ax.plot(x_click, y_click, 'bo')

        # Generate and draw random red point
        random_x, random_y = np.random.rand(2)
        self.random_point, = self.ax.plot(random_x, random_y, 'ro')

        # Draw quarter circles
        self.draw_quarter_circles(x_click, y_click)

        # Calculate and draw intersection point
        intersection_x, intersection_y = self.intersection_with_x_axis(
            (x_click, y_click), (random_x, random_y))

        # Only draw intersection point and lines if within square bounds
        if 0 <= intersection_x <= 1 and intersection_y == 0:
            self.intersection_point, = self.ax.plot(intersection_x, intersection_y, 'go')
            line1, = self.ax.plot([x_click, intersection_x], [y_click, intersection_y], 'b--')
            line2, = self.ax.plot([random_x, intersection_x], [random_y, intersection_y], 'r--')
            self.lines.extend([line1, line2])

        plt.draw()

def main():
    """Main function to run the visualization tool."""
    visualizer = GeometricProbabilityVisualizer()
    plt.show()

if __name__ == "__main__":
    main()