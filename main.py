from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests, os, re
# 설치 필요한 모듈 bs4, reqeusts

url = 'https://openaccess.thecvf.com/CVPR2016'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

pattern = re.compile(".*[.]pdf")

pdf_links = []
for i in soup.find_all('a'):
    if i.text == 'pdf':
        pdf_links.append(i["href"])


os.makedirs('ThesisPdf')

for link in pdf_links:
    print(link)
    name = link.split('/')[-1]
    make_url = 'https://openaccess.thecvf.com/' + link

    response = requests.get(make_url)

    with open(f'ThesisPdf/{name}', 'wb') as f:
        f.write(response.content)