import numpy as np
from scipy.interpolate import splprep, splevfrom scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt

def fit_bspline(points, num_points_per_curve=100, max_error=1e-3):
    """
    Fit a set of points to one or more B-spline curves dynamically.
    
    Parameters:
        points (np.ndarray): Array of shape (n, 2) with points to fit.
        num_points_per_curve (int): Number of points to sample on each B-spline.
        max_error (float): Maximum allowed error for curve fitting.
    
    Returns:
        curves (list): A list of fitted curves, each containing sampled points.
    """
    curves = []
    n_points = len(points)
    current_start = 0
    
    while current_start < n_points:
        # Try fitting a curve to all remaining points
        remaining_points = points[current_start:]
        
        # Fit a B-spline to the remaining points
        tck, u = splprep(remaining_points.T, s=0)  # s=0 for interpolating the points
        fitted_points = np.array(splev(u, tck)).T
        
        # Calculate error
        error = np.linalg.norm(remaining_points - fitted_points, axis=1).mean()
        
        if error > max_error:
            # If error exceeds max_error, split the segment and refit
            split_index = len(remaining_points) // 2
            segment = remaining_points[:split_index]
            
            tck_segment, u_segment = splprep(segment.T, s=0)
            sampled_points = np.array(splev(np.linspace(0, 1, num_points_per_curve), tck_segment)).T
            curves.append(sampled_points)
            
            # Move the start point for next curve
            current_start += split_index
        else:
            # If error is acceptable, finalize the current curve
            sampled_points = np.array(splev(np.linspace(0, 1, num_points_per_curve), tck)).T
            curves.append(sampled_points)
            break

    return curves


# Example usage
if __name__ == "__main__":
    # Generate some synthetic points with noise
    t = np.linspace(0, 2 * np.pi, 100)
    x = np.cos(t) + 0.1 * np.random.normal(size=t.shape)
    y = np.sin(t) + 0.1 * np.random.normal(size=t.shape)
    points = np.vstack((x, y)).T

    # Fit the points to one or more B-splines
    fitted_curves = fit_bspline(points)

    # Plot the results
    plt.scatter(points[:, 0], points[:, 1], label="Original Points", s=10)
    for i, curve in enumerate(fitted_curves):
        plt.plot(curve[:, 0], curve[:, 1], label=f"Fitted Curve {i+1}")
    plt.legend()
    plt.show()

