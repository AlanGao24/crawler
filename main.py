import csv, requests
from bs4 import BeautifulSoup

def get_product_url():
    file = 'products.csv'
    with open(file, 'r') as f:
        reader = csv.reader(f)
        products_url = [row[0] for row in reader if row]
    return products_url

def get_soup(url):
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        return BeautifulSoup(res.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_product_info(soup):
    try:
        if not soup:
            print("Soup object is None")
            return None
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
 
        return "\n".join(html_blocks)
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_product_image(soup):
    try:
        image_element = soup.find('img', class_='CENy8b')
        if image_element and 'src' in image_element.attrs:
            return image_element['src']
        else:
            print("Image not found")
            return ""
    except Exception as e:
        print(f"Error fetching image: {e}")
        return ""

def main():
    BRAND = "testBrand"
    CATAGORY = "testChemical"

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
            soup = get_soup(url)
            description = fetch_product_info(soup)
            image = fetch_product_image(soup)
            if description:
                writer.writerow({
                    "Name": product,
                    "Description": description,
                    "Category": CATAGORY,
                    "Brand": BRAND,
                    "Image": image
                })
            else:
                print(f"Failed to fetch description for {product}")

if __name__ == "__main__":
    main()
