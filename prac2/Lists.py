mylist = ["apple", "banana", "cherry"]
thislist = ["apple", "cherry", "banana", "cherry"]
print(thislist)
print(len(thislist))
list2 = [1, 5, 7, 9, 3]
list3 = [True, False, False]
list1 = ["abc", 34, True, 40, "male"]
print(type(mylist))
thislist = list(("apple", "banana", "cherry")) # note the double round-brackets
print(thislist)
print()
#Access List Items
print(thislist[1])
print(thislist[-1])
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5])
print(thislist[:4])
print(thislist[2:])
print(thislist[-4:-1])
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")
print()
#Change List Items
thislist[1] = "blackcurrant"
print(thislist)
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)
thislist = ["apple", "banana", "cherry"]
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist)
thislist[1:3] = ["watermelon"]
print(thislist)
thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)
print()
#Add List Items
thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)
thislist.insert(1, "orange")
print(thislist)
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)
thislist = ["apple", "banana", "cherry"]
thistuple = ("kiwi", "orange")
thislist.extend(thistuple)
print(thislist)
print()
#Remove List Items
thislist.remove("banana")
print(thislist)
thislist = ["apple", "banana", "cherry", "banana", "kiwi"]
thislist.remove("banana")
print(thislist)
thislist.pop(1)
print(thislist)
thislist.pop()
print(thislist)
del thislist[0]
print(thislist)
del thislist
thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist)
print()
#Loop Lists
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)
for i in range(len(thislist)):
  print(thislist[i])
i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1
[print(x) for x in thislist]
print()
#List Comprehension
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []

for x in fruits:
  if "a" in x:
    newlist.append(x)

print(newlist)
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

newlist = [x for x in fruits if "a" in x]

print(newlist)
print()
newlist = [x for x in fruits if x != "apple"]
print(newlist)
print()
newlist = [x for x in fruits]
print(newlist)
print()
newlist = [x for x in range(10)]
print(newlist)
print()
newlist = [x for x in range(10) if x < 5]
print(newlist)
print()
newlist = [x.upper() for x in fruits]
print(newlist)
print()
newlist = ['hello' for x in fruits]
print(newlist)
print()
newlist = [x if x != "banana" else "orange" for x in fruits]
print(newlist)
print()
#Sort Lists
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)
thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)
print(thislist)
thislist = [100, 50, 65, 82, 23]
thislist.sort(reverse = True)
print(thislist)
def myfunc(n):
  return abs(n - 50)

thislist = [100, 50, 65, 82, 23]
thislist.sort(key = myfunc)
print(thislist)
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort()
print(thislist)
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort(key = str.lower)
print(thislist)
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.reverse()
print(thislist)
print()
#Copy Lists
mylist = thislist.copy()
print(mylist)
mylist = list(thislist)
print(mylist)
mylist = thislist[:]
print(mylist)
#Join Lists
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list3 = list1 + list2
print(list3)
for x in list2:
  list1.append(x)

print(list1)
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]

list1.extend(list2)
print(list1)
#List Method
fruits = ['apple', 'banana', 'cherry']
fruits.append("orange")
print(fruits)
fruits = ['apple', 'banana', 'cherry', 'orange']

fruits.clear()
print(fruits)
fruits = ['apple', 'banana', 'cherry', 'orange']

x = fruits.copy()
print(x)
x = fruits.count("cherry")
print(x)
fruits = ['apple', 'banana', 'cherry']

cars = ['Ford', 'BMW', 'Volvo']

fruits.extend(cars)
print(fruits)
fruits = ['apple', 'banana', 'cherry']
x = fruits.index("cherry")
print(x)
fruits.insert(1, "orange")
print(fruits)
fruits.pop(1)
print(fruits)
fruits.remove("banana")
print(fruits)
fruits.reverse()
print(fruits)
cars.sort()
print(cars)