import numpy as np
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt

def fit_bspline(points, num_points_per_curve=100, max_error=1e-3):
    """
    Fit a set of points to one or more B-spline curves dynamically.
    
    Parameters:
        points (np.ndarray): Array of shape (n, 3) with points to fit.
        num_points_per_curve (int): Number of points to sample on each B-spline.
        max_error (float): Maximum allowed error for curve fitting.
    
    Returns:
        curves (list): A list of B-spline curves as arrays of sampled points.
    """
    curves = []
    n_points = len(points)
    current_start = 0
    
    while current_start < n_points:
        # Extract remaining points
        remaining_points = points[current_start:]

        # Transpose the input points to shape (3, n_points)
        transposed_points = remaining_points.T

        # Fit a B-spline curve using splprep
        tck, u = splprep(transposed_points, s=0)  # s=0 for interpolation

        # Evaluate the spline at the fitted parameter values
        fitted_points = np.array(splev(u, tck)).T

        # Calculate error
        error = np.linalg.norm(remaining_points - fitted_points, axis=1).mean()

        if error > max_error:
            # If error exceeds max_error, split the segment and refit
            split_index = len(remaining_points) // 2
            segment = remaining_points[:split_index]
            
            # Fit to the segment
            tck_segment, u_segment = splprep(segment.T, s=0)
            sampled_points = np.array(splev(np.linspace(0, 1, num_points_per_curve), tck_segment)).T
            curves.append(sampled_points)
            
            # Move the start point for the next curve
            current_start += split_index
        else:
            # Acceptable fit, finalize this curve
            sampled_points = np.array(splev(np.linspace(0, 1, num_points_per_curve), tck)).T
            curves.append(sampled_points)
            break

    return curves

# Example Usage
if __name__ == "__main__":
    # Generate synthetic points (e.g., a noisy helix in 3D)
    t = np.linspace(0, 4 * np.pi, 100)
    x = np.sin(t)
    y = np.cos(t)
    z = t / (2 * np.pi)
    points = np.vstack((x, y, z)).T

    # Fit the points to one or more B-splines
    fitted_curves = fit_bspline(points)

    # Plot the original points and fitted curves
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], label="Original Points", s=10)
    for i, curve in enumerate(fitted_curves):
        ax.plot(curve[:, 0], curve[:, 1], curve[:, 2], label=f"Fitted Curve {i+1}")
    ax.legend()
    plt.show()

