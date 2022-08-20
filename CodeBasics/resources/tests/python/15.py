x = 0
y = 10
z = 20

while x > y > z:
    z -= x+y
    y -= x+z
    x -= z+y

print(x*y*z)