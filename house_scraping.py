from bs4 import BeautifulSoup
import requests
import csv

houses_data = []
num_page = 3

def generate_url(num_page):
    return f'https://www.mubawab.tn/en/sc/houses-for-sale:p:{num_page}'

for num in range(1, num_page + 1):
    url = generate_url(num)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    houses = soup.find_all('li', class_='listingBox w100')

    for house in houses:
        prix_span = house.find('span', class_='priceTag hardShadow float-right floatL yellowBg')
        pix2 = house.find('span', class_='priceTag hardShadow float-right floatL')
        title = house.find('h2', class_='listingTit').text.strip()
        place = house.find('h3', class_='listingH3').text.strip()
        w9t = house.find('span', class_='listingDetails iconPadR').text.strip()
        desc1 = house.find('p', class_='listingP descLi')
        desc2 = house.find('h4', class_='listingH4 floatR')

        if desc1:
            desc1 = desc1.text.strip().replace('\n', '')
        else:
            desc1 = "Description not found"

        if desc2:
            desc2 = desc2.text.strip()
        else:
            desc2 = house.find('p', class_='listingH4 floatR').text.strip()

        parts = desc2.split(',')

        rooms = "Rooms not found"
        area = "Area not found"

        for part in parts:
            part = part.strip()
            if 'bedroom' in part.lower():
                rooms = part
            elif 'm²' in part.lower():
                area = part

        if prix_span:
            prix = prix_span.text.strip()
        else:
            prix = pix2.text.strip()

        images = []
        image_tags = house.find_all('img', class_='w100 sliderImage firstPicture')
        for img_tag in image_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = img_url.strip()
                images.append(img_url)

        houses_data.append({
            'Title': title,
            'Place': ' '.join(place.split()),
            'W9t': w9t.replace('\n', ''),
            'Description': desc1,
            'Rooms': rooms,
            'Area': area,
            'Price': prix,
            'Images': '; '.join(images)  
        })



def convert_to_csv(data, filename='houses_data.csv'):
    headers = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)


        writer.writeheader()


        writer.writerows(data)

    print(f"Data has been written to {filename}")

convert_to_csv(houses_data)
