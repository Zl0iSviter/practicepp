import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
#The findall() func:
x = re.findall("ai", txt)
print(x)
x = re.findall("Portugal", txt)
print(x)
#The search() func:
x = re.search("\s", txt)

print("The first white-space character is located in position:", x.start())
x = re.search("Portugal", txt)
print(x)
# the split() func:
x = re.split("\s", txt)
print(x)
#Split the string only at the first occurrence:
x = re.split("\s", txt, 1)
print(x)
# the sub() func:
x = re.sub("\s", "9", txt)
print(x)
x = re.sub("\s", "9", txt, 2)
print(x)
# Match object
x = re.search("ai", txt)
print(x) #this will print an object
x = re.search(r"\bS\w+", txt)
print(x.span())
x = re.search(r"\bS\w+", txt)
print(x.string)
x = re.search(r"\bS\w+", txt)
print(x.group())
#Metacharacters :
txt = "hello planet"
#Find all lower case characters alphabetically between "a" and "m":
x = re.findall("[a-m]", txt)
print(x)

#Find all digit characters:

x = re.findall("\d", txt)
print(x)

#Search for a sequence that starts with "he", followed by two (any) characters, and an "o":

x = re.findall("he..o", txt)
print(x)

#Check if the string starts with 'hello':

x = re.findall("^hello", txt)
if x:
  print("Yes, the string starts with 'hello'")
else:
  print("No match")

#Check if the string ends with 'planet':

x = re.findall("planet$", txt)
if x:
  print("Yes, the string ends with 'planet'")
else:
  print("No match")

#Search for a sequence that starts with "he", followed by 0 or more  (any) characters, and an "o":

x = re.findall("he.*o", txt)

print(x)

#Search for a sequence that starts with "he", followed by 1 or more  (any) characters, and an "o":

x = re.findall("he.+o", txt)

print(x)

#Search for a sequence that starts with "he", followed by 0 or 1  (any) character, and an "o":

x = re.findall("he.?o", txt)

print(x)

#This time we got no match, because there were not zero, not one, but two characters between "he" and the "o"

#Search for a sequence that starts with "he", followed excactly 2 (any) characters, and an "o":

x = re.findall("he.{2}o", txt)

print(x)

txt = "The rain in Spain falls mainly in the plain!"

#Check if the string contains either "falls" or "stays":

x = re.findall("falls|stays", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Flags:

txt = "Åland"

#Find all ASCII matches:
print(re.findall("\w", txt, re.ASCII))

#Without the flag, the example would return all character:
print(re.findall("\w", txt))


#Same result using the shorthand re.A flag:
print(re.findall("\w", txt, re.A))

txt = "The rain in Spain"

#Use a case-insensitive search when finding a match for Spain in the text:

print(re.findall("spain", txt, re.DEBUG))

txt = """Hi
my
name
is
Sally"""

#Search for a sequence that starts with "me", followed by one character, even a newline character, and continues with "is":
print(re.findall("me.is", txt, re.DOTALL))

#This example would return no match without the re.DOTALL flag:
print(re.findall("me.is", txt))


#Same result with the shorthand re.S flag:
print(re.findall("me.is", txt, re.S))

txt = "The rain in Spain"

#Use a case-insensitive search when finding a match for Spain in the text:
print(re.findall("spain", txt, re.IGNORECASE))


#Same result using the shorthand re.I flag:
print(re.findall("spain", txt, re.I))

txt = """There
aint much
rain in 
Spain"""

#Search for the sequence "ain", at the beginning of a line:
print(re.findall("^ain", txt, re.MULTILINE))

#This example would return no matches without the re.MULTILINE flag, because the ^ character without re.MULTILINE only get a match at the very beginning of the text:
print(re.findall("^ain", txt))


#Same result with the shorthand re.M flag:
print(re.findall("^ain", txt, re.M))

txt = "Åland"

#Find all UNICODE matches:
print(re.findall("\w", txt, re.UNICODE))


#Same result using the shorthand re.U flag:
print(re.findall("\w", txt, re.U))

text = "The rain in Spain falls mainly on the plain"

#Find and return words that contains the phrase "ain":

pattern = """
[A-Za-z]* #starts with any letter
ain+      #contains 'ain'
[a-z]*    #followed by any small letter
"""

print(re.findall(pattern, text, re.VERBOSE))

#The example would return nothing without the re.VERBOSE flag
print(re.findall(pattern, text))


#Same result with the shorthand re.X flag:
print(re.findall(pattern, text, re.X))

#Special Sequences

txt = "The rain in Spain"

#Check if the string starts with "The":

x = re.findall("\AThe", txt)

print(x)

if x:
  print("Yes, there is a match!")
else:
  print("No match")

#Check if "ain" is present at the beginning of a WORD:

x = re.findall(r"\bain", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if "ain" is present at the end of a WORD:

x = re.findall(r"ain\b", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if "ain" is present, but NOT at the beginning of a word:

x = re.findall(r"\Bain", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if "ain" is present, but NOT at the end of a word:

x = re.findall(r"ain\B", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if the string contains any digits (numbers from 0-9):

x = re.findall("\d", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Return a match at every no-digit character:

x = re.findall("\D", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Return a match at every white-space character:

x = re.findall("\s", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Return a match at every NON white-space character:

x = re.findall("\S", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Return a match at every word character (characters from a to Z, digits from 0-9, and the underscore _ character):

x = re.findall("\w", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Return a match at every NON word character (characters NOT between a and Z. Like "!", "?" white-space etc.):

x = re.findall("\W", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if the string ends with "Spain":

x = re.findall("Spain\Z", txt)

print(x)

if x:
  print("Yes, there is a match!")
else:
  print("No match")

#sets

#Check if the string has any a, r, or n characters:

x = re.findall("[arn]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if the string has any characters between a and n:

x = re.findall("[a-n]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if the string has other characters than a, r, or n:

x = re.findall("[^arn]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if the string has any 0, 1, 2, or 3 digits:

x = re.findall("[0123]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

txt = "8 times before 11:45 AM"

#Check if the string has any digits:

x = re.findall("[0-9]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if the string has any two-digit numbers, from 00 to 59:

x = re.findall("[0-5][0-9]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if the string has any characters from a to z lower case, and A to Z upper case:

x = re.findall("[a-zA-Z]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#Check if the string has any + characters:

x = re.findall("[+]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")