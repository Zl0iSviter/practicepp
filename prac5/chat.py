import re

with open("raw.txt", "r", encoding="utf8") as file:
    text = file.read()

prices = re.findall(r"\d+,\d{2}", text)
print("All prices from the receipt:")
for price in prices:
    print(price)

products = re.findall(r"^[A-Za-z ].+", text, re.MULTILINE)
print("All products from the receipt:")
for product in products:
    print(product)