import html
import requests
from bs4 import BeautifulSoup
import csv

pcet = []
num_page=4
id_counter = 1
def generate_url(num_page):
    return f'https://www.tunisianet.com.tn/301-pc-portable-tunisie?page={num_page}&order=product.price.asc'

for num in range(1,num_page+1):
    url=generate_url(num)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    pcs = soup.find_all('div', class_='item-product')
    for pc in pcs:
        title = pc.find('h2', class_='h3 product-title').text.strip()
        price = pc.find('span', class_='price').text.strip()
        description = pc.find('div', class_='listds').text.strip()

        pcet.append({
            'ID': id_counter,
            'Title': title,
            'Price': price,
            'Description': description
        })
        
        id_counter += 1

for pc in pcet:
    print(pc)
def convert_to_csv(data, filename='pc_data.csv'):

    headers = data[0].keys()


    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        writer.writeheader()
        
        writer.writerows(data)

    print(f"Data has been written to {filename}")

# Appeler la fonction pour convertir le tableau en fichier CSV
convert_to_csv(pcet)