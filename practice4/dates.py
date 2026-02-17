import datetime

x = datetime.datetime.now()
print(x)

print(x.year)
print(x.strftime("%A"))

x = datetime.datetime(2020, 5, 17)

print(x)

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))

x = datetime.datetime.now()

print(x.strftime("%a"))

print(x.strftime("%A"))

print(x.strftime("%d"))

print(x.strftime("%b"))

print(x.strftime("%m"))

print(x.strftime("%y"))

print(x.strftime("%Y"))

print(x.strftime("%H"))

print(x.strftime("%I"))

print(x.strftime("%M"))

print(x.strftime("%S"))

print(x.strftime("%w"))

print(x.strftime("%W"))

print(x.strftime("%f"))

print(x.strftime("%z"))

print(x.strftime("%Z"))

print(x.strftime("%j"))

print(x.strftime("%U"))

print(x.strftime("%x"))

print(x.strftime("%X"))

print(x.strftime("%%"))

print(x.strftime("%G"))

print(x.strftime("%u"))

print(x.strftime("v"))