import math

def main():

    radius = input('Input the radius of a circle')

    radnum = float(radius)

    area = math.pi * (radnum ** 2)

    perimeter = math.pi * 2 * radnum 

    print(f'The circle with radius {radnum:.2f} has an area of {area:.2f} and a perimeter of {perimeter:.2f}.')

if __name__=="__main__":
    main()
    