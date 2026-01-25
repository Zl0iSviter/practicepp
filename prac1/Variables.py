x , y = 5 ,"Adema"
print(x)
print(y)
x = "Anya"
print(x)
print()
print(type(x))
print(type(y))
a = int(4)
A = "Sally"
print(a," ", A)
_var_="Smth"
#2var is illegal
#Camel case :
myVarName = "Jonny"
#Pascal Case
MyVarName = "Sara"
#Snake Case
my_variable_name= "Asan"
a = b = "Orange"
print(a)
print(b)
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)
print()
print(myVarName, MyVarName , my_variable_name)
print(myVarName + MyVarName + my_variable_name)
b = 6
a = 5
# print(b + A) will give an error
print(b , A)
print(a + b) # + is also a mathematical operator
print()
c = "T_T"
print("Global variable c :" , c)

def myFunc():
    global c
    c = "Hiiii"
    print("Global variable used in func : " + MyVarName )

myFunc()
print("Changed global variable c in a func :", c)

def myFunc2():
    MyVarName = "Jonny"
    print("Local variable MyVarName:" , MyVarName)

myFunc2()
print("Global variable MyVarName:" ,MyVarName)
