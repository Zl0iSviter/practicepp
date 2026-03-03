import re
import json
file = open("raw.txt", "r", encoding="utf8")

text = file.read()

pattern = r"x\s(.+,\d{2})"
prices = list(re.findall(pattern, text))
print("All prices from the receipt :")
for i in prices:
    print(i)

pattern = r"\.\n(.+)\n"
products = list(re.findall(pattern, text))
print("All products from the receipt :")
for i in products:
    print(i)
sum = 0
pattern = r"ь\n(.+)\n"
a = list(re.findall(pattern, text))
for i in a:
    i = i.replace(',' , '.').replace(" ", "")
    sum += float(i)
print()
print(f'Общая сумма : {sum}')
print()
print("Дата и время :")
pattern = r"Время:(.+)\n"
print(re.search(pattern, text).group(1))


pattern = r"(Банковская карта|Наличные)"
pay = re.search(pattern, text)
if pay.group(1) == None:
    print("Неизвестный метод оплаты")
else:
    print("Метод оплаты:", pay.group(1) )

data = {
    "prices": prices,
    "products": products,
    "total_sum": sum,
    "date_time": re.search(r"Время:(.+)\n", text).group(1),
    "payment_method": pay.group(1) if pay else "Неизвестный метод оплаты"
}

print(json.dumps(data, indent=4, ensure_ascii=False))