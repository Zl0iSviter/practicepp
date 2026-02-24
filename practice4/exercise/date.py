from datetime import datetime , timedelta
#1
x = datetime.now()
print(x - timedelta(days = 5))
#2

print("Yesterday:", x - timedelta(days=1))
print("Today:", x)
print("Tomorrow:", x+timedelta(days=1))
# 3
nomicrosec = x.replace(microsecond=0)
print(nomicrosec)
#4
date1 = datetime(2026, 2, 20, 12, 0, 0)
date2 = datetime(2026, 2, 24, 15, 30, 0)

difference = date2 - date1

print(difference.total_seconds())