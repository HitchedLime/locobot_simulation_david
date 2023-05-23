import numpy as np
import math
import sympy

def law_of_cosines(a, b, C):
    c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(C))
    return c

def angle_between_vectors(u, v):
    cos_theta = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    theta = np.arccos(cos_theta)
    
    return theta

def euclidean_distance(array):
    # calculates distance from robot assuming that robot is  at origin every step
    distance = 0
    for value in array:
        distance +=pow(value,2)
        
    return math.sqrt(distance)

def third_point(x1:float, y1:float, x2:float, y2:float,AC):
    # Calculate the length of each side
    
    AB = math.sqrt((x2-x1)**2+(y2-y1)**2)
    BC= math.sqrt(AB**2+AC**2)

    x, y = sympy.symbols("x y", real=True)

    eq1 = sympy.Eq((x1 - x)**2 +(y1-y)**2, AC**2)
    eq2 = sympy.Eq((x2 - x)**2 +(y2-y)**2, BC**2)
    

    # eq1 = sympy.Eq((x1 - x)**2 + (y1 - y)**2, 3)
    # eq2 = sympy.Eq((x2 - x)**2 + (y2 - y)**2, 100)


    result = sympy.solve([eq1, eq2])
    print(result)
    Cx,Cy= result[0][x],result[0][y]
    
    return round(Cx),round(Cy)


#third_point(1.0,1.0,2.0,2.0,1.0)