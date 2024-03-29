import os
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_cat_breeds"

names = []
locations = []
pics = []

os.makedirs('cat_imgs', exist_ok=True)

# Mask as a browser
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

response = requests.get(url, headers=headers)

# Check if response was successful
if response.status_code == 200:
	# Parse HTML
	soup = BeautifulSoup(response.text, 'html.parser')

	# Extract a table
	table = soup.find('table', {'class': 'wikitable sortable'})

	# Extracting all breeds
	for row in table.find_all('tr')[1:]:
		# Get breed info
		columns = row.find_all(['td', 'th'])
		name = columns[0].find('a').text.strip()
		location = columns[1].text.strip()

		# Get breed image
		img_tag = columns[6].find('img')
		pic = img_tag['src'] if img_tag else ''

		if pic and not pic.startswith('http'):
			pic = 'https:' + pic

		if pic:
			response = requests.get(pic)
			img_filename = os.path.join('cat_imgs', f'{name}.jpg')
			with open(img_filename, 'wb') as img_file:
				img_file.write(response.content)

		names.append(name)
		locations.append(location)
		pics.append(pic)

print(names)
print(locations)