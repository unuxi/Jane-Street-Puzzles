# Geometric Probability Problem Solution

## Problem Statement
Given a unit square, two points (blue and red) are randomly and uniformly selected within it. Calculate the probability (to ten decimal places) that there exists a point on the edge of the square, closest to the blue point, that is equidistant to both the blue and red points.

## Solution Journey

### Initial Monte Carlo Approach
My first approach was to use a Monte Carlo simulation to approximate the solution. The strategy was straightforward: randomly generate millions of point pairs within the unit square and check for each pair if there exists a point on the square's edge (closest to the blue point) that is equidistant to both points. Initial results suggested the probability was approximately 0.491. However, achieving the required precision of ten decimal places would have required an impractical number of iterations and computational time.

### Key Geometric Insights
After reconsidering the problem, I made several important observations that led to a more elegant solution. First, the problem exhibits rotational symmetry. The unit square can be divided into three equal triangles by its diagonals, and due to symmetry, we only need to analyze one of these triangles. Second, when the blue point is placed in the lower triangle, the closest edge is always the bottom edge of the square, which significantly simplifies our analysis. Third, for any given blue point, the set of possible red points that satisfy our condition form a specific geometric pattern bounded by quarter circles centered at the square's corners.

These insights led to the development of two complementary programs: a visualization tool to build geometric intuition and an exact mathematical solution using integral calculus.

## Visualization Tool

### Purpose and Implementation
The visualization tool (`geometric_probability.py`) provides an interactive environment where users can explore the geometric properties of the problem. Users can place the blue point within the lower triangle of the unit square, observe a randomly generated red point, visualize the perpendicular bisector between the points, and see the quarter circles that define the boundary of valid red point positions.

### Mathematical Components
The tool implements several key geometric calculations:

```python
def is_inside_triangle(x, y, triangle_coords):
    """
    Determines if point (x,y) lies within the triangle using barycentric coordinates
    """
    x1, y1 = triangle_coords[0]
    x2, y2 = triangle_coords[1]
    x3, y3 = triangle_coords[2]
    denominator = ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
    a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / denominator
    b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / denominator
    c = 1 - a - b
    return (0 <= a <= 1) and (0 <= b <= 1) and (0 <= c <= 1)
```

For any blue point (x₀, y₀), two quarter circles are drawn from corners (0,0) and (1,0) with radii:
- r₁ = √(x₀² + y₀²)
- r₂ = √((1-x₀)² + y₀²)

### Key Observations
Through experimentation with the visualization tool, I discovered that for any blue point, the valid positions for the red point are bounded by two quarter circles. The intersection area of these quarter circles represents positions where no solution exists. This led to the realization that the total probability for a given blue point position is:

(Area of quarter circles - Intersection area) / Total square area

## Exact Mathematical Solution

### Mathematical Framework
The exact solution (`exact_solution.py`) calculates the probability through the following steps:

1. For any blue point (x, y) in the lower triangle, we calculate:
   ```
   f(x, y) = A₁ + A₂ - A_overlap
   where:
   A₁ = πr₁²/4 (area of first quarter circle)
   A₂ = πr₂²/4 (area of second quarter circle)
   r₁ = √(x² + y²)
   r₂ = √((1-x)² + y²)
   ```

2. The circle overlap area is calculated using:
   ```python
   def calculate_circles_overlap(radius1, radius2, distance):
       if distance >= radius1 + radius2:
           return 0
       elif distance <= abs(radius1 - radius2):
           return np.pi * min(radius1, radius2)**2
       
       angle1 = 2 * np.arccos((distance**2 + radius1**2 - radius2**2) / 
                             (2 * distance * radius1))
       angle2 = 2 * np.arccos((distance**2 + radius2**2 - radius1**2) / 
                             (2 * distance * radius2))
       
       area1 = 0.5 * radius1**2 * (angle1 - np.sin(angle1))
       area2 = 0.5 * radius2**2 * (angle2 - np.sin(angle2))
       
       return area1 + area2
   ```

   The mathematical formulation for the overlap area calculation is as follows:

   Let r₁, r₂ be the radii of the two circles and d be the distance between their centers.

   Case 1: No overlap (d ≥ r₁ + r₂)
   ```
   A_overlap = 0
   ```

   Case 2: One circle contains the other (d ≤ |r₁ - r₂|)
   ```
   A_overlap = πr_min²  where r_min = min(r₁, r₂)
   ```

   Case 3: Partial overlap
   ```
   θ₁ = 2 arccos((d² + r₁² - r₂²)/(2dr₁))
   θ₂ = 2 arccos((d² + r₂² - r₁²)/(2dr₂))

   A_overlap = ½r₁²(θ₁ - sin θ₁) + ½r₂²(θ₂ - sin θ₂)
   ```

   For our specific problem, given a blue point (x, y) in the lower triangle:
   ```
   r₁ = √(x² + y²)              [radius from (0,0)]
   r₂ = √((1-x)² + y²)          [radius from (1,0)]
   d = 1                        [distance between centers]

   A_quarter1 = πr₁²/4          [area of first quarter circle]
   A_quarter2 = πr₂²/4          [area of second quarter circle]

   Total valid area = A_quarter1 + A_quarter2 - A_overlap
   ```

3. The final probability is calculated by integrating over the lower triangle:
   ```
   P = (1/0.25) ∫∫_T f(x,y) dx dy
   where T is the triangle with vertices (0,0), (1,0), (0.5,0.5)
   ```

### Implementation Details
Due to the triangle's shape, the double integral is split into two parts:
```python
area1, _ = dblquad(integrand, 0, 0.5,
                   lambda x: 0,
                   lambda x: x)

area2, _ = dblquad(integrand, 0.5, 1,
                   lambda x: 0,
                   lambda x: 1 - x)

total_probability = (area1 + area2) / 0.25
```

## Usage

1. To run the visualization tool:
   ```bash
   python geometric_probability.py
   ```

2. To calculate the exact solution:
   ```bash
   python exact_solution.py
   ```

## Dependencies
- NumPy
- Matplotlib
- SciPy

## License
This project is licensed under the MIT License.

## Author's Note
This solution demonstrates the power of combining computational visualization with mathematical analysis. The visualization tool was crucial in building intuition about the problem's geometric properties, which then guided the development of the exact mathematical solution.

The journey from a brute-force Monte Carlo approach to an elegant analytical solution showcases how geometric insights and visual intuition can lead to more efficient and precise mathematical solutions.