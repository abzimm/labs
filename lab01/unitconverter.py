import math

def main():

    user_input = input("Input a distance or weight amount. There should be a space in between the number and unit, i.e '111.1 g'. You can use in, cm, yd, m, oz, g, kg, lb")

    val_string, unit_string = user_input.split()

    val = float(val_string)

    unit = unit_string.lower()

    if unit == "in":
        converted_val = val * 2.54
        converted_unit = "cm"
    elif unit == "cm":
        converted_val = val / 2.54
        converted_unit = "in"
    elif unit == "yd":
        converted_val = val * 0.9144
        converted_unit = "m"
    elif unit == "m":
        converted_val = val / 0.9144
        converted_unit = "yd"
    elif unit == "oz":
        converted_val = val * 28.349523125
        converted_unit = "g"
    elif unit == "g":
        converted_val = val / 28.349523125
        converted_unit = "oz"
    elif unit == "lb":
        converted_val = val * 0.45359237
        converted_unit = "kg"
    elif unit == "kg":
        converted_val = val / 0.45359237
        converted_unit = "lb"
    else:
        print("Input error")
        return

    print(f"{val}{unit} = {converted_val:.2f}{converted_unit}")

if __name__=="__main__":
    main()
    