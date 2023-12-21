a11 = int(a11)
a12 = int(a12)
a21 = int(a21)
a22 = int(a22)
b1 = int(b1)
b2 = int(b2)

div = a11*a22-a12*a21
v1 = (a22*b1-a12*b2)/div
v2 = (-a21*b1+a11*b2)/div

v1 = int(v1)
v2 = int(v2)
result = {x1: v1, x2: v2}
