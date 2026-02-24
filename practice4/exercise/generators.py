# the first task:
def square(n):
    for i in range(n + 1):
        yield i * i

n = int(input())
for value in square(n):
    print(value)

#the second :
def even(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input())
print(",".join(str(num) for num in even(n)))

# the third:
def div(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
for num in div(n):
    print(num)
# the fourth:
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

a = int(input())
b = int(input())
for value in squares(a, b):
    print(value)
# the fifth:
def cd(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input())
for num in cd(n):
    print(num)