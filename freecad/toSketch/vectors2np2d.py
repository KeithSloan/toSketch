# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileNotice: Part of the ToSketch addon.

# Example list of FreeCAD Vectors
vectors = [App.Vector(1, 2, 3), App.Vector(4, 5, 6), App.Vector(7, 8, 9)]

# Convert to NumPy 2D array for the XY plane
array_xy = vectors_to_2d_array(vectors, plane="XY")
print("XY Plane:")
print(array_xy)
# Output:
# [[1. 2.]
#  [4. 5.]
#  [7. 8.]]

# Convert to NumPy 2D array for the XZ plane
array_xz = vectors_to_2d_array(vectors, plane="XZ")
print("XZ Plane:")
print(array_xz)
# Output:
# [[1. 3.]
#  [4. 6.]
#  [7. 9.]]

# Convert to NumPy 2D array for the YZ plane
array_yz = vectors_to_2d_array(vectors, plane="YZ")
print("YZ Plane:")
print(array_yz)
# Output:
# [[2. 3.]
#  [5. 6.]
#  [8. 9.]]

