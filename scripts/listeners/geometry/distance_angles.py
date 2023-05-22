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

def third_point(x1:float, y1:float, x2:float, y2:float)-> tuple(float,float):
    # Calculate the length of each side
    AB = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    AC = AB / (2 ** 0.5)
    BC = AC

    # Calculate the angle between AB and AC
    angle = math.atan2(y2 - y1, x2 - x1)

    # Calculate the coordinates of C
    Cx = x2 - BC * math.cos(angle + math.pi / 4)
    Cy = y2 - BC * math.sin(angle + math.pi / 4)

    return Cx, Cy


