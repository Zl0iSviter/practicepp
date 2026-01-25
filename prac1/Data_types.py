x = 5
print(type(x) , x)
x = "Hello World"
print(type(x), x)
x = 20
print(type(x), x)
x = 20.5
print(type(x), x)
x = 1j
print(type(x), x)
x = ["apple", "banana", "cherry"]
print(type(x), x)
x = ("apple", "banana", "cherry")
print(type(x), x)
x = range(6)
print(type(x), x)
x = {"name" : "John", "age" : 36}
print(type(x), x)
x = {"apple", "banana", "cherry"}
print(type(x), x)
x = frozenset({"apple", "banana", "cherry"})
print(type(x), x)
x = True
print(type(x), x)
x = b"Hello"
print(type(x), x)
x = bytearray(5)
print(type(x), x)
x = memoryview(bytes(5))
print(type(x), x)
x = None
print(type(x), x)
#setting the specific data type :
x = str("Hello World")
x = int(20)
x = float(20.5)
x = complex(1j)
x = list(("apple", "banana", "cherry"))
x = tuple(("apple", "banana", "cherry"))
x = range(6)
x = dict(name="John", age=36)
x = set(("apple", "banana", "cherry"))
x = frozenset(("apple", "banana", "cherry"))
x = bool(5)
x = bytes(5)
x = bytearray(5)
x = memoryview(bytes(5))