import csv, requests, bs4

def get_product_list():
    file = 'products.csv'
    with open(file, 'r') as f:
        reader = csv.reader(f)
        products = [row[0] for row in reader if row]
    return products

