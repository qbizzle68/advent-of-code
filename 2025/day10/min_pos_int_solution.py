import numpy as np
from scipy.linalg import lstsq, null_space
from itertools import product

def find_min_positive_integer_solution(A, b, search_radius=50):
    """
    Find the positive integer solution to Ax = b with minimum sum of elements.
    
    Parameters:
    -----------
    A : array_like
        Coefficient matrix
    b : array_like
        Right-hand side vector
    search_radius : int
        How far to search in null space directions
        
    Returns:
    --------
    x_min : ndarray or None
        Positive integer solution with minimum sum, or None if not found
    """
    
    # Step 1: Get a real-valued solution
#    print(f'{A=}')
#    print(f'{b=}')
    x_real, residuals, rank, s = lstsq(A, b)
    
    print(f"Real solution: {x_real}")
    print(f"Matrix rank: {rank}/{min(A.shape)}")
    
    # Step 2: Get null space
    null_basis = null_space(A)
    n_null_dims = null_basis.shape[1]
    
    print(f"Null space dimensions: {n_null_dims}")
    
    # Step 3: Search for positive integer solutions with minimum sum
    
    if n_null_dims == 0:
        # Unique solution - just round and check
        x_int = np.round(x_real).astype(int)
        if np.allclose(A @ x_int, b) and np.all(x_int > 0):
            print(f"Unique solution (sum={np.sum(x_int)}): {x_int}")
            return x_int
        else:
            print("No positive integer solution found (unique solution is invalid)")
            return None
    
    # Start search from rounded real solution
    x_base = np.round(x_real)
    
    min_sum = float('inf')
    best_solution = None
    
    # Search over combinations of null space vectors
    total_searched = 0
    
    for offsets in product(range(-search_radius, search_radius+1), repeat=n_null_dims):
        # Construct candidate
        x_candidate = x_base.copy()
        for i, offset in enumerate(offsets):
            x_candidate += offset * null_basis[:, i]
        
        x_int = np.round(x_candidate).astype(int)
        
        # Check if valid: positive, integer, and satisfies Ax=b
        if np.all(x_int > 0):
            error = np.linalg.norm(A @ x_int - b)
            
            if error < 1e-10:  # Valid solution
                current_sum = np.sum(x_int)
                if current_sum < min_sum:
                    min_sum = current_sum
                    best_solution = x_int.copy()
                    print(f"Found solution with sum={current_sum}: {x_int}")
        
        total_searched += 1
        
        # Progress indicator for large searches
        if total_searched % 100000 == 0:
            print(f"Searched {total_searched} combinations...")
    
    if best_solution is not None:
        print(f"\nBest solution found with sum={min_sum}: {best_solution}")
        return best_solution
    else:
        print(f"\nNo positive integer solution found in search radius {search_radius}")
        print("Try increasing search_radius")
        return None


def find_min_positive_smart(A, b, max_attempts=50000):
    """
    Smarter search using gradient descent in null space to minimize sum
    while maintaining positive integer constraints.
    """
    
    # Get real solution and null space
    x_real, _, rank, _ = lstsq(A, b)
    null_basis = null_space(A)
    n_null_dims = null_basis.shape[1]
    
    print(f"Real solution: {x_real}")
    print(f"Null space dimensions: {n_null_dims}")
    
    if n_null_dims == 0:
        x_int = np.round(x_real).astype(int)
        if np.allclose(A @ x_int, b) and np.all(x_int > 0):
            return x_int
        return None
    
    # Strategy: move in null space directions that decrease the sum
    # while keeping all elements positive
    
    best_solution = None
    min_sum = float('inf')
    
    # Try multiple starting points
    rng = np.random.RandomState(42)
    
    for attempt in range(max_attempts):
        # Random starting point in null space
        if attempt == 0:
            # Start from rounded real solution
            coeffs = np.zeros(n_null_dims)
        else:
            # Random starting point
            coeffs = rng.randint(-20, 21, size=n_null_dims)
        
        x_candidate = np.round(x_real).copy()
        for i, c in enumerate(coeffs):
            x_candidate += c * null_basis[:, i]
        
        x_int = np.round(x_candidate).astype(int)
        
        # Check validity
        if np.all(x_int > 0) and np.allclose(A @ x_int, b, atol=1e-10):
            current_sum = np.sum(x_int)
            if current_sum < min_sum:
                min_sum = current_sum
                best_solution = x_int.copy()
                print(f"Found solution with sum={current_sum}: {x_int}")
        
        if attempt % 10000 == 0 and attempt > 0:
            print(f"Attempted {attempt} random walks...")
    
    return best_solution


# Example usage
if __name__ == "__main__":
    # Example: singular system with multiple solutions
    A = np.array([[0, 0, 0, 0, 1, 1],
                  [0, 1, 0, 0, 0, 1],
                  [0, 0, 1, 1, 1, 0],
                  [1, 1, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]], dtype=float)
    b = np.array([3, 5, 4, 7, 0, 0], dtype=float)
    
    print("="*60)
    print("Method 1: Exhaustive search")
    print("="*60)
    x_solution = find_min_positive_integer_solution(A, b, search_radius=20)
    
    if x_solution is not None:
        print(f"\n{'='*60}")
        print("FINAL RESULT")
        print(f"{'='*60}")
        print(f"Minimum positive integer solution: {x_solution}")
        print(f"Sum of elements: {np.sum(x_solution)}")
        print(f"Verification Ax = {A @ x_solution}")
        print(f"Target b = {b}")
        print(f"Valid: {np.allclose(A @ x_solution, b)}")
        print(f"All positive: {np.all(x_solution > 0)}")
    
    print("\n" + "="*60)
    print("Method 2: Random search (for larger problems)")
    print("="*60)
    x_solution2 = find_min_positive_smart(A, b, max_attempts=10000)
    
    if x_solution2 is not None:
        print(f"\nSolution: {x_solution2}, sum={np.sum(x_solution2)}")

    tmp = np.array([1, 3, 0, 3, 1, 2])
    print(A @ tmp)
