import os
import csv

# sprawdzamy w jakiej ścieżce jesteśmy
print(os.getcwd())

# tworzymy listę na podstawie nazw plików w danej ścieżce

# path = "C:\Users\fpiecyk.NATURAL\SDA\basketShopProject\upload\products"
files = [['Full cap', 30, 1, 'lorem', 'uploads/products/'+f] for f in os.listdir() if os.path.isfile(f)]
print(files)


with open('product_list.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    header =['name', 'price', 'category_id', 'description', 'image']
    # write the header
    writer.writerow(header)

    # for row in files:
    #     writer.writerow(row)
    # write the data in multiple rows
    writer.writerows(files)
