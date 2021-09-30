from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests, os
# 설치 필요한 모듈 bs4, reqeusts


def url_pdflink_parser(url: str) -> list:  # url의 pdf 링크를 반환.
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    pdf_links = []
    for i in soup.find_all('a'):
        if i.text == 'pdf':
            pdf_links.append(i["href"])
    return pdf_links


def make_dir(dir_name, force=False):  # dir_name의
    if force:
        os.makedirs(dir_name, exist_ok=True)
    else:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        else:
            print(f"{dir_name} is already exist...")
            exit()


def pdflink_down(dir_name, links: list):
    for link in tqdm(links):
        name = link.split('/')[2]
        make_url = 'https://openaccess.thecvf.com/' + link

        response = requests.get(make_url)

        with open(f'{dir_name}/{name}', 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    file_name = input("폴더명을 입력하세요: ")
    make_dir(file_name, True)

    url = input("링크를 입력하세요: ")
    pdf_links = url_pdflink_parser(url)
    pdflink_down(file_name, pdf_links)



