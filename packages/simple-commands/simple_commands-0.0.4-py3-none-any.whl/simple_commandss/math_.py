import math

# คำนวณพื้นที่สามเหลี่ยม
def calculate_triangle_area(base, height):
    return 0.5 * base * height

# คำนวณพื้นที่สี่เหลี่ยมผืนผ้า
def calculate_rectangle_area(length, width):
    return length * width

# คำนวณพื้นที่สี่เหลี่ยมจตุรัส
def calculate_square_area(side):
    return side * side

# คำนวณพื้นที่วงกลม
def calculate_circle_area(radius):
    return math.pi * (radius ** 2)

# คำนวณความยาวเส้นรอบรูปสามเหลี่ยม
def calculate_triangle_perimeter(side1, side2, side3):
    return side1 + side2 + side3

# คำนวณความยาวเส้นรอบรูปสี่เหลี่ยมผืนผ้า
def calculate_rectangle_perimeter(length, width):
    return 2 * (length + width)

# คำนวณความยาวเส้นรอบรูปสี่เหลี่ยมจตุรัส
def calculate_square_perimeter(side):
    return 4 * side

# คำนวณความยาวเส้นรอบรูปวงกลม
def calculate_circle_circumference(radius):
    return 2 * math.pi * radius

# คำนวณปริมาตรของทรงกรวย
def calculate_cone_volume(radius, height):
    return (1/3) * math.pi * (radius ** 2) * height

# คำนวณปริมาตรของทรงกระบอก
def calculate_cylinder_volume(radius, height):
    return math.pi * (radius ** 2) * height

# คำนวณปริมาตรของทรงกระบอกออกซิเดียน
def calculate_oxygen_cylinder_volume(diameter, height):
    radius = diameter / 2
    return math.pi * (radius ** 2) * height


def tempFtoC(F):
    return (F - 32) * 5/9

def tempCtoF(C):
    return (C * 9/5) + 32
