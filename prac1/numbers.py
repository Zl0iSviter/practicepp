import random
x = 1    # int
y = 9.6  # float
z = 3j   # complex
print(type(x))
print(type(y))
print(type(z))
print()
x = -1
y = -9e6
z = -3j
print(type(x))
print(type(y))
print(type(z))
print()
a = float(x)
b = int(y)
c = complex(x)

print(a)
print(b)
print(c)
print()
print(type(a))
print(type(b))
print(type(c))
print()
print(random.randrange(1, 10))