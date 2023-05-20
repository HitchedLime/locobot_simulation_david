import numpy as np
import math
def law_of_cosines(a, b, C):
    c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(C))
    return c

def angle_between_vectors(u, v):
    cos_theta = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    theta = np.arccos(cos_theta)
    print(f"The angle between the two vectors is {np.degrees(theta)} degrees")
    return theta

def euclidean_distance(array):
    # calculates distance from robot assuming that robot is  at origin every step
    distance = 0
    for value in array:
        distance +=pow(value,2)
        
    return math.sqrt(distance)