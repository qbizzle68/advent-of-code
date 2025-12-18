import numpy as np
from scipy.linalg import lstsq, null_space

def project_gradient_to_nullspace(gradient, null_basis):
    """
    Project gradient onto the null space.
    
    This gives us the direction in null space that most decreases the objective.
    """
    if null_basis.shape[1] == 0:
        return np.zeros_like(gradient)
    
    # Project: P = N(N^T N)^{-1}N^T
    NTN = null_basis.T @ null_basis
    NTN_inv = np.linalg.inv(NTN)
    projection = null_basis @ NTN_inv @ null_basis.T @ gradient
    
    return projection


def gradient_descent_nullspace(A, b, learning_rate=0.1, max_iterations=1000000, 
                                tolerance=1e-8, verbose=True):
    """
    Use gradient descent in the null space to find minimum sum solution.
    
    Objective: minimize sum(x) subject to Ax = b and x > 0
    
    Returns the best positive integer solution found.
    """
    
    # Get initial solution and null space
    x_real, _, rank, _ = lstsq(A, b)
    null_basis = null_space(A)
    print(f'{null_basis=}')
    n_null_dims = null_basis.shape[1]
    
    if verbose:
        print(f"Starting real solution: {x_real}, sum={np.sum(x_real):.2f}")
        print(f"Null space dimensions: {n_null_dims}")
    
    if n_null_dims == 0:
        x_int = np.round(x_real).astype(int)
        if np.allclose(A @ x_int, b) and np.all(x_int > 0):
            return x_int
        return None
    
    # Start from real solution
    x_current = x_real.copy()
    
    # Gradient of sum(x) is just vector of ones
    gradient = np.ones(len(x_current))
    
    best_integer_solution = None
    best_sum = float('inf')
    
    for iteration in range(max_iterations):
        # Project gradient onto null space
        projected_grad = project_gradient_to_nullspace(gradient, null_basis)
        
        # Move in opposite direction (gradient descent)
        x_new = x_current - learning_rate * projected_grad
        
        # Check if we went too far (any element became negative)
        if np.any(x_new <= 0):
            # Reduce learning rate and try again
            learning_rate *= 0.5
            if learning_rate < 1e-10:
                if verbose:
                    print(f"Learning rate too small at iteration {iteration}")
                break
            continue
        
        x_current = x_new
        
        # Every so often, check if we have a good integer solution nearby
        if iteration % 100 == 0:
            x_int = np.round(x_current).astype(int)
            
            if np.all(x_int > 0) and np.allclose(A @ x_int, b, atol=1e-10):
                current_sum = np.sum(x_int)
                if current_sum < best_sum:
                    best_sum = current_sum
                    best_integer_solution = x_int.copy()
                    if verbose:
                        print(f"Iter {iteration}: Found integer solution sum={current_sum}: {x_int}")
        
        # Check convergence
        if np.linalg.norm(projected_grad) < tolerance:
            if verbose:
                print(f"Converged at iteration {iteration}")
            break
    
    # Final check
    x_int = np.round(x_current).astype(int)
    if np.all(x_int > 0) and np.allclose(A @ x_int, b, atol=1e-10):
        current_sum = np.sum(x_int)
        if current_sum < best_sum:
            best_sum = current_sum
            best_integer_solution = x_int.copy()
    
    if verbose and best_integer_solution is not None:
        print(f"\nFinal solution: {best_integer_solution}, sum={best_sum}")
    
    return best_integer_solution


def multi_start_gradient_descent(A, b, n_starts=10, verbose=True):
    """
    Run gradient descent from multiple starting points to avoid local minima.
    """
    
    x_real, _, _, _ = lstsq(A, b)
    null_basis = null_space(A)
    
    if null_basis.shape[1] == 0:
        x_int = np.round(x_real).astype(int)
        if np.allclose(A @ x_int, b) and np.all(x_int > 0):
            return x_int
        return None
    
    best_solution = None
    best_sum = float('inf')
    
    rng = np.random.RandomState(42)
    
    for start_idx in range(n_starts):
        if verbose:
            print(f"\n{'='*60}")
            print(f"Starting point {start_idx + 1}/{n_starts}")
            print(f"{'='*60}")
        
        # Create starting point by moving in null space
        if start_idx == 0:
            # Start from the least squares solution
            x_start = x_real.copy()
        else:
            # Random starting point in null space
            coeffs = rng.randn(null_basis.shape[1]) * 10
            x_start = x_real.copy()
            for i, c in enumerate(coeffs):
                x_start += c * null_basis[:, i]
            
            # Ensure positive
            if np.any(x_start <= 0):
                x_start = np.abs(x_start) + 1
        
        # Run gradient descent
        solution = gradient_descent_nullspace(
            A, b, 
            learning_rate=0.5 / (start_idx + 1),  # Decrease learning rate for later starts
            max_iterations=5000,
            verbose=verbose
        )
        
        if solution is not None:
            current_sum = np.sum(solution)
            if current_sum < best_sum:
                best_sum = current_sum
                best_solution = solution.copy()
                if verbose:
                    print(f"New best from this start: sum={best_sum}")
    
    return best_solution


def hybrid_approach(A, b, verbose=True):
    """
    Combine gradient descent with local search around the result.
    """
    
    # First, use gradient descent to get close
    if verbose:
        print("Phase 1: Gradient descent to find good region")
        print("="*60)
    
    gd_solution = gradient_descent_nullspace(A, b, verbose=verbose)
    
    if gd_solution is None:
        return None
    
    # Then do local search around this solution
    if verbose:
        print(f"\nPhase 2: Local search around gradient descent result")
        print("="*60)
    
    null_basis = null_space(A)
    best_solution = gd_solution.copy()
    best_sum = np.sum(gd_solution)
    
    # Search in a small radius around the GD solution
    search_radius = 5
    n_null = null_basis.shape[1]
    
    if n_null > 0:
        from itertools import product
        
        for offsets in product(range(-search_radius, search_radius+1), repeat=n_null):
            x_candidate = gd_solution.astype(float)
            for i, offset in enumerate(offsets):
                x_candidate += offset * null_basis[:, i]
            
            x_int = np.round(x_candidate).astype(int)
            
            if np.all(x_int > 0) and np.allclose(A @ x_int, b, atol=1e-10):
                current_sum = np.sum(x_int)
                if current_sum < best_sum:
                    best_sum = current_sum
                    best_solution = x_int.copy()
                    if verbose:
                        print(f"Found better solution: sum={best_sum}: {x_int}")
    
    return best_solution


# Example usage
if __name__ == "__main__":
    # Example system
    '''A = np.array([[1, 2, 3],
                  [2, 4, 6],
                  [1, 1, 2]], dtype=float)
    b = np.array([7, 14, 8], dtype=float)'''
    A = np.array([[0, 0, 0, 0, 1, 1],
                  [0, 1, 0, 0, 0, 1],
                  [0, 0, 1, 1, 1, 0],
                  [1, 1, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]], dtype=int)
    b = np.array([3, 5, 4, 7, 0, 0], dtype=int)
    
    print("Method 1: Single gradient descent")
    print("="*60)
    solution1 = gradient_descent_nullspace(A, b)
    if solution1 is not None:
        print(f"\nResult: {solution1}, sum={np.sum(solution1)}")
        print(f"Valid: {np.allclose(A @ solution1, b)}")
    
    print("\n\nMethod 2: Multi-start gradient descent")
    print("="*60)
    solution2 = multi_start_gradient_descent(A, b, n_starts=5)
    if solution2 is not None:
        print(f"\nBest result: {solution2}, sum={np.sum(solution2)}")
        print(f"Valid: {np.allclose(A @ solution2, b)}")
    
    print("\n\nMethod 3: Hybrid (gradient descent + local search)")
    print("="*60)
    solution3 = hybrid_approach(A, b)
    if solution3 is not None:
        print(f"\nFinal result: {solution3}, sum={np.sum(solution3)}")
        print(f"Valid: {np.allclose(A @ solution3, b)}")
