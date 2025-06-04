import csv, requests
from bs4 import BeautifulSoup

def get_product_url():
    file = 'products.csv'
    with open(file, 'r') as f:
        reader = csv.reader(f)
        products_url = [row[0] for row in reader if row]
    return products_url

def fetch_product_info(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        content_area = soup.find('div', class_='tyJCtd mGzaTb Depvyb baZpAe')
        try:
            if not content_area:
                raise ValueError("Content area not found")
        except ValueError as ve:
            print(f"Error!: {ve}")
            return None

        html_blocks = []
        current_title = None

        for tag in content_area.descendants:
            if tag.name == 'h3':
                current_title = tag.get_text(strip=True)
                html_blocks.append(f"<h3>{current_title}</h3>")
            elif tag.name in ['p', 'ul'] and current_title:
                text = tag.get_text(separator='\n', strip=True)
                html_blocks.append(f"<p>{text}</p>")

        ds_block = "\n".join(html_blocks)
        return ds_block
    except Exception as e:
        print(f"Error: {e}")
        return None
    
# res = fetch_product_info("https://www.focusproducts.com.au/chemical-template/shock-n-clear")
# print(res)
# print(type(res))

BRAND = "Focus"
CATAGORY = "Chemical"

with open('products.csv', 'r') as f:
    reader = csv.reader(f)
    products_name = []
    products_url = []
    for row in reader:
        if row:
            products_name.append(row[0])
            products_url.append(row[1])

with open('wooCommerce_product.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['Name', 'Description', 'Category', 'Brand', 'Image'])
    writer.writeheader()
    for product, url in zip(products_name, products_url):
        description = fetch_product_info(url)
        if description:
            writer.writerow({
                "Name": product,
                "Description": description,
                "Category": CATAGORY,
                "Brand": BRAND,
                "Image": ""
            })
        else:
            print(f"Failed to fetch description for {product}")
