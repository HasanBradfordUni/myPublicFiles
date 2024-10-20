#PAT 1

import math

def circleCalcs(radius):
    area = math.pi * radius**2
    circumference = math.pi * radius * 2
    return area, circumference

if __name__ == "__main__":
    radius = int(input("Enter a radius for a circle (integer): "))
    area, circumference = circleCalcs(radius)
    print("The circumference of this circle is: %5.2f" % (circumference))
    print("The area of this circle is: %6.2f" % (area))
