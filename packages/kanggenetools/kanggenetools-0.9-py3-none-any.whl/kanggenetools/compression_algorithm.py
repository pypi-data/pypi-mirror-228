import numpy as np

def logistic_map(u_n, a):
    """
    Logistic Map function for chaotic dynamics.
    
    Parameters:
    - u_n: Current value
    - a: Constant parameter

    Returns:
    - Next value in the sequence
    """
    return a * u_n * (1 - u_n)


def u5D_to_v3D(points_5D):
    """
    Convert a 5D point to a 3D point using double compression.

    Parameters:
    - points_5D: 5D point

    Returns:
    - 3D point
    """
    first_compressed = u4D_to_v3D(points_5D[:-1])
    return np.array(u4D_to_v3D(np.hstack((first_compressed, [points_5D[-1]]))))


def u4D_to_v3D(points_4D):
    """
    Convert a 4D point to a 3D point.

    Parameters:
    - points_4D: 4D point

    Returns:
    - 3D point
    """
    r, alpha, beta = get_alpha_beta(*points_4D[:-1])
    return np.array(get_xyz(r, 0.5 * alpha, 0.5 * beta, points_4D[-1]))


def get_alpha_beta(x, y, z):
    """
    Calculate spherical coordinates for a 3D point.

    Parameters:
    - x, y, z: 3D point

    Returns:
    - r, alpha, beta: Spherical coordinates
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    beta = np.where(r != 0, np.arcsin(z/r), 0)
    return r, np.arctan2(y, x), beta


def get_xyz(r, alpha, beta, w=0):
    """
    Convert spherical coordinates to Cartesian coordinates.

    Parameters:
    - r, alpha, beta: Spherical coordinates

    Returns:
    - x, y, z: 3D Cartesian coordinates
    """
    z_temp = r * np.sin(beta)
    r1 = r * np.cos(beta)
    return r1 * np.cos(alpha), r1 * np.sin(alpha), z_temp + w
