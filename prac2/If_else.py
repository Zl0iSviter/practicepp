a = 33
b = 200
if b > a:
  print("b is greater than a")
number = 15
if number > 0:
  print("The number is positive")
'''a = 33
b = 200
if b > a:
print("b is greater than a") 
you will get an error '''
age = 20
if age >= 18:
  print("You are an adult")
  print("You can vote")
  print("You have full legal rights")
is_logged_in = True
if is_logged_in:
  print("Welcome back!")
print()
#Elif Statement
a = 33
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
score = 75

if score >= 90:
  print("Grade: A")
elif score >= 80:
  print("Grade: B")
elif score >= 70:
  print("Grade: C")
elif score >= 60:
  print("Grade: D")
age = 25

if age < 13:
  print("You are a child")
elif age < 20:
  print("You are a teenager")
elif age < 65:
  print("You are an adult")
elif age >= 65:
  print("You are a senior")

day = 3

if day == 1:
  print("Monday")
elif day == 2:
  print("Tuesday")
elif day == 3:
  print("Wednesday")
elif day == 4:
  print("Thursday")
elif day == 5:
  print("Friday")
elif day == 6:
  print("Saturday")
elif day == 7:
  print("Sunday")
print()
#Else Statement
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")
a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")
number = 7

if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")
temperature = 22

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")
username = "Emil"

if len(username) > 0:
  print(f"Welcome, {username}!")
else:
  print("Error: Username cannot be empty")
print()
#Shorthand If
a = 5
b = 2
if a > b: print("a is greater than b")
a = 2
b = 330
print("A") if a > b else print("B")
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)
print()
#Logical Operators
a = 200
b = 33
c = 500
if a > b and c > a:
  print("Both conditions are True")
a = 200
b = 33
c = 500
if a > b or a > c:
  print("At least one of the conditions is True")
a = 33
b = 200
if not a > b:
  print("a is NOT greater than b")
age = 25
is_student = False
has_discount_code = True

if (age < 18 or age > 65) and not is_student or has_discount_code:
  print("Discount applies!")
temperature = 25
is_raining = False
is_weekend = True

if (temperature > 20 and not is_raining) or is_weekend:
  print("Great day for outdoor activities!")
username = "Tobias"
password = "secret123"
is_verified = True

if username and password and is_verified:
  print("Login successful")
else:
  print("Login failed")
score = 85

if score >= 0 and score <= 100:
  print("Valid score")
else:
  print("Invalid score")
print()
#Nested If
x = 41

if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  else:
    print("but not above 20.")
age = 25
has_license = True

if age >= 18:
  if has_license:
    print("You can drive")
  else:
    print("You need a license")
else:
  print("You are too young to drive")
score = 85
attendance = 90
submitted = True

if score >= 60:
  if attendance >= 80:
    if submitted:
      print("Pass with good standing")
    else:
      print("Pass but missing assignment")
  else:
    print("Pass but low attendance")
else:
  print("Fail")
temperature = 25
is_sunny = True

if temperature > 20:
  if is_sunny:
    print("Perfect beach weather!")
temperature = 25
is_sunny = True

if temperature > 20 and is_sunny:
  print("Perfect beach weather!")
username = "Emil"
password = "python123"
is_active = True

if username:
  if password:
    if is_active:
      print("Login successful")
    else:
      print("Account is not active")
  else:
    print("Password required")
else:
  print("Username required")
score = 92
extra_credit = 5

if score >= 90:
  if extra_credit > 0:
    print("A+ grade")
  else:
    print("A grade")
elif score >= 80:
  print("B grade")
else:
  print("C grade or below")
print()
#Pass Statement
a = 33
b = 200

if b > a:
  pass
age = 16

if age < 18:
  pass # TODO: Add underage logic later
else:
  print("Access granted")
score = 85

if score > 90:
  pass # This is excellent
print("Score processed")
value = 50

if value < 0:
  print("Negative value")
elif value == 0:
  pass # Zero case - no action needed
else:
  print("Positive value")
def calculate_discount(price):
  pass # TODO: Implement discount logic

# Function exists but doesn't do anything yet
