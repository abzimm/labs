import math

def main():

    num1 = input('Type a number')
    num2 = input('Type another number')

    a = float(num1)
    b = float(num2)

    c = math.sqrt(a**2 + b**2)

    print(f'The hypotenuse is {c:.2f}')

if __name__=="__main__":
    main()