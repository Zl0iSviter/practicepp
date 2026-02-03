print(10 + 5)
x = 15
y = 4
#arithmetic operators
print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y)
print(x ** y)
print(x // y)
print()
#assignment operators
х = 5
х += 3
х = 3
х *= 3
х /= 3
х %= 3
х //= 3
х **= 3
x &= 3
print(x)
х = 3
х^= 3
х >>= 3
х <<= 3
print(x := 3)
print()
#the walrus operator:
numbers = [1, 2, 3, 4, 5]
count = len(numbers)
if count > 3:
    print(f"List has {count} elements")
numbers.append(6)
if (count := len(numbers)) > 3:
    print(f"List has {count} elements")
print()
#Comparison operators
x = 5
y = 3

print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)
print()
#chaining comparison operators
print(1 < x < 10)

print(1 < x and x < 10)
#Logical operators
print(x > 0 and x < 10)
print(x < 5 or x > 10)
print(not(x > 3 and x < 10))
print()
#identity operators
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)
# is - Checks if both variables point to the same object in memory
# == - Checks if the values of both variables are equal
x = ["apple", "banana"]
y = ["apple", "banana"]

print(x is not y)
print()
#Python Membership Operators
fruits = ["apple", "banana", "cherry"]

print("banana" in fruits)
print("pineapple" not in fruits)
text = "Hello World"

print("H" in text)
print("hello" in text)
print("z" not in text)
print()
#Bitwise Operators
print(6 & 3)
print(6 | 3)
print(6 ^ 3)
print(~5)
print(6 << 2)
print(6 >> 2)
print()
#Operator Precedence
print((6 + 3) - (6 + 3))
print(100 + 5 * 3)
print(5 + 4 - 7 + 3)
print(5 == 4 + 1)