import os
import csv
import random

# sprawdzamy w jakiej ścieżce jesteśmy
print(os.getcwd())

# tworzymy listę na podstawie nazw plików w danej ścieżce

# path = "C:\Users\fpiecyk.NATURAL\SDA\basketShopProject\upload\products"

shorts = ["Shorts " + str(no) for no in range(1,8)]
price = [random.randint(40, 55) for _ in range(1, 8)]
category = [2 for _ in range(1, 8)]
description = ["lorem"*50 for _ in range(1, 8)]
files = ['uploads/products/'+f for f in os.listdir() if os.path.isfile(f)]
rows = [shorts, price, category, description, files]
print(files)


with open('product_list.csv', 'w', encoding='1250', newline='') as file:
    writer = csv.writer(file)
    header =['name', 'price', 'category_id', 'description', 'image']
    # write the header
    writer.writerow(header)
    writer.writerows(rows)
    for row in files:
        writer.writerow(row)
    # write the data in multiple rows

