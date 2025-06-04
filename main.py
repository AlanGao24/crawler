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
        content_area = soup.find('div', {'id': 'h.3e74ddf81ceda5b4_70'})
        if not content_area:
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
    
res = fetch_product_info("https://www.focusproducts.com.au/chemical-template/shock-n-clear")
print(res)
print(type(res))