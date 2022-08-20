a = 1
b = -6
c = 9

D = b**2 - 4*a*c
if D > 0:
    print((-b + D**(1/2))/(2*a))
    print((-b - D**(1/2))/(2*a))
elif D == 0:
    print(-b/(2*a))
else:
    print("No roots :)")