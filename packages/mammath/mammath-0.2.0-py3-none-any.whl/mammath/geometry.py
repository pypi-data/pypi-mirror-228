from constants import pi
from operations import sqrt
import math

"""
GEOMETRY
"""

def deg_to_rad(degrees):
    """
    Converts degree to radians
    """
    return degrees * math.pi / 180

def rad_to_deg(radians):
    """
    Converts radians to degree
    """
    return radians * 180 / math.pi

def valid_triangle(s1, s2, s3):
    """
    If a triangle with three given sides is valid
    """
    if s1 + s2 >= s3 and s2 + s3 >= s1 and s1 + s3 >= s2:
        return True
    return False

def triangle_area(l, w):
    """
    Area of a triangle from base and vertical height
    """
    return (l*w)/2
def trapezium_area(a, b, h):
    """
    Area of a trapezium from two parallel sides and vertical height
    """
    return (a+b)/h
def para_area(b, h):
    """
    Area of a parallelogram from base and vertical height
    """
    return b*h
def circle_circumference(r):
    """
    Circumference of a circle from radius
    """
    return 2*pi*r
def circle_area(r):
    """
    Area of a circle from radius
    """
    return pi*(r**2)
def sphere_volume(r):
    """
    Volume of a sphere from radius
    """
    return 4/3*pi*(r**3)
def sphere_area(r):
    """
    Surface area of a sphere from radius
    """
    return 4*pi*(r**2)
def sphere_diametre(r):
    """
    Diameter of a sphere with radius
    """
    return 2*r
def surface_area(a, b, c):
    """
    Surface area of a cuboid with three side lengths
    """
    d = a*b
    e = a*c
    f = b*c
    return 2*(d+e+f)
def surf_area_prism(farea, *args):
    """
    Surface area of a prism with frontal area and length
    """
    total = 2*farea
    i = 0
    while i < len(args):
        total += args[i]
        i += 1
    return total
def volume(a, b, c):
    """
    Volume of a cuboid with three side lengths
    """
    return a*b*c
def cylinder_volume(r, h):
    """
    Volume of a cylinder with height and radius
    """
    return (pi*(r**2))*h
def cylinder_area(r, h):
    """
    Surface area of a cylinder with height and radius
    """
    return (2*pi*r*h)+(2*pi*(r**2))
def cylinder_diametre(v, h):
    """
    Diameter of a cylinder with volume and height
    """
    return 2*(sqrt(v/pi*h))
def cylinder_height(v, r):
    """
    Height of a cylinder with volume and radius
    """
    return v/(pi*(r**2))
def cylinder_radius(h, A):
    """
    radius of a cylinder from height and surface area
    """
    return round(0.5*sqrt(h**2 + 2*(A/pi))-h/2, 5)
def cone_area(r, h):
    """
    Surface area of a cone
    """
    area = pi*r*(r + sqrt(h**2 + r**2))
    return round(area, 5)
def cone_volume(r, h):
    """
    Volume of a cone from radius and height
    """
    vol = pi*r**2*(h/3)
    return round(vol, 5)
def cone_radius(h, vol):
    """
    Radius of cone from height and volume
    """
    rad = sqrt(3*(vol/(pi*h)))
    return round(rad, 5)
def cone_height(r, vol):
    """
    Height of a cone from radius and volume
    """
    height = 3*(vol/(pi*r**2))
    return round(height, 5)


def sin(theta, radians=True):
    """
    Computes the value of sin(theta)
    """
    return math.sin(deg_to_rad(theta)) if not radians else math.sin(theta)

def cos(theta, radians=True):
    """
    Computes the value of cos(theta)
    """
    return math.cos(deg_to_rad(theta)) if not radians else math.cos(theta)
    
def tan(theta, radians=True):
    """
    Computes the value of tan(theta)
    """
    return math.tan(deg_to_rad(theta)) if not radians else math.tan(theta)
    
def csc(theta, radians=True):
    """
    Computes the value of cosecant(theta)
    """
    return 1/math.sin(deg_to_rad(theta)) if not radians else 1/math.sin(theta)

def sec(theta, radians=True):
    """
    Computes the value of secant(theta)
    """
    return 1/math.cos(deg_to_rad(theta)) if not radians else 1/math.cos(theta)
    
def cot(theta, radians=True):
    """
    Computes the value of cotangent(theta)
    """
    return 1/math.tan(deg_to_rad(theta)) if not radians else 1/math.tan(theta)
    
def acsc(n, radians=True):
    """
    Computes the value of arccosecant(n)
    """
    return rad_to_deg(math.asin(1/n)) if not radians else math.asin(1/n)

def asec(n, radians=True):
    """
    Computes the value of arcsecant(n)
    """
    return rad_to_deg(math.acos(1/n)) if not radians else math.acos(1/n)
    
def acot(n, radians=True):
    """
    Computes the value of arccotangent(n)
    """
    return rad_to_deg(math.atan(1/n)) if not radians else math.atan(1/n)
    
def asin(n, radians=True):
    """
    Computes the value of arcsin(n)
    """
    return rad_to_deg(math.asin(n)) if not radians else math.asin(n)

def acos(n, radians=True):
    """
    Computes the value of arccos(n)
    """
    return rad_to_deg(math.acos(n)) if not radians else math.acos(n)
    
def atan(n, radians=True):
    """
    Computes the value of arctan(n)
    """
    return rad_to_deg(math.atan(n)) if not radians else math.atan(n)

def py_theorem_ab(a, b):
    """
    Returns the hypotenuse of a triangle given a and b sides
    """
    return sqrt(a**2+b**2)

def py_theorem_c(c, a):
    """
    Returns the missing side length given one leg and the hypotenuse
    """
    return sqrt(c**2-a**2)

def cos_rule(a, b, A_rad):
    """
    Finds the third side of a triangle given two sides and the angle between them
    """
    return a**2 + b**2 - 2*a*b*cos(A_rad)

def area_tan(n, s):
    """
    Finds the third side of a triangle given two sides and the angle between them
    """
    s1 = s**2
    up = n * s1
    intan = (180 / n)
    tanpart = math.tan(math.radians(intan))
    down = 4 * tanpart
    ans = up / down
    return ans

def polygon_area_nxn(n, s):
    """
    Computes the area of a regular n-sided polygon with lengths s
    """
    return round((n*s**2)/(4*tan(pi/n)), 6)

def pythagorean_triplets(n):
    """
    Prints pythagorean triplets until n
    """
    for b in range(n):
        for a in range(1, b):
            c = sqrt(a * a + b * b)
            if c % 1 == 0:
                print(a, b, int(c))
            
def pythagorean_triplets_check(a, b, c):
    """
    Checks if three numbers can be pythagorean triplets
    """
    return True if a**2 + b**2 == c**2 else False

def hex_area(a):
    """
    Finds the area of a regular hexagon given the side length
    """
    return 1.5 * sqrt(3) * a ** 2

def pent_area(a):
    """
    Finds the area of a regular pentagon given the side length
    """
    return a**2* sqrt(5*(5+2*sqrt(5)))/4

def herons_formula(a, b, c):
    """
    Finds the area of any triangle when given three valid sides
    """
    s = (a+b+c)/2
    return sqrt(s*(s-a)*(s-b)*(s-c))


"""
END OF OF GEOMETRY
"""
