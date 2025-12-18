import numpy as np
from scipy.linalg import lu, solve_triangular, null_space, lstsq

def find_integer_solution(A, b, search_radius=10):
    """
    Find an integer solution to Ax = b
    
    Strategy:
    1. Find any real-valued solution (using least squares for robustness)
    2. Find the null space of A
    3. Search for integer combinations near the real solution
    """
    
    # Step 1: Get a real-valued solution (works even if A is singular)
    x_real, residuals, rank, s = lstsq(A, b)
    
    print(f"Real solution: {x_real}")
    print(f"Matrix rank: {rank}/{min(A.shape)}")
    
    # Step 2: Get null space
    null_basis = null_space(A)
    n_null_dims = null_basis.shape[1]
    
    print(f"Null space dimensions: {n_null_dims}")
    
    # Step 3: Search for integer solutions
    # We'll search: x = x_real + linear combination of null space vectors
    
    if n_null_dims == 0:
        # Unique solution - just round and check
        x_int = np.round(x_real).astype(int)
        if np.allclose(A @ x_int, b):
            return x_int
        else:
            print("No integer solution found (unique solution is not integer)")
            return None
    
    # Search over null space combinations
    x_rounded = np.round(x_real)
    
    # Try different integer offsets in the null space
    from itertools import product
    
    best_solution = None
    best_error = float('inf')
    
    for offsets in product(range(-search_radius, search_radius+1), repeat=n_null_dims):
        # Construct candidate: x_rounded + combination of null vectors
        x_candidate = x_rounded.copy()
        for i, offset in enumerate(offsets):
            x_candidate += offset * null_basis[:, i]
        
        x_int = np.round(x_candidate).astype(int)
        
        # Check if this is a valid integer solution
        error = np.linalg.norm(A @ x_int - b)
        
        if error < 1e-10:  # Found exact solution
            return x_int
        
        if error < best_error:
            best_error = error
            best_solution = x_int
    
    if best_error < 1e-6:
        return best_solution
    
    print(f"No exact integer solution found. Best error: {best_error}")
    return best_solution

# Example usage
A = np.array([[0, 0, 0, 0, 1, 1],
              [0, 1, 0, 0, 0, 1],
              [0, 0, 1, 1, 1, 0],
              [1, 1, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]], dtype=float)
b = np.array([3, 5, 4, 7, 0, 0], dtype=float)

x_solution = find_integer_solution(A, b)
if x_solution is not None:
    print(f"\nInteger solution found: {x_solution}")
    print(f"Verification Ax = {A @ x_solution}")
    print(f"Target b = {b}")
    print(f"Match: {np.allclose(A @ x_solution, b)}")
