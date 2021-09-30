from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests, os
# 설치 필요한 모듈 bs4, reqeusts, tqdm


def url_pdflink_parser(url: str) -> (list, list):  # url의 pdf 링크를 반환.
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    pdf_links, name_list = [], []
    for i in soup.find_all('a'):
        if i.text == 'pdf':
            pdf_links.append(link := i["href"])
            name_list.append(link.split('/')[2])
    return pdf_links, name_list


def make_dir(dir_name, name_list, force=False):  # dir_name의
    pass_file = {}

    if force:
        os.makedirs(dir_name, exist_ok=True)
    else:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        else:
            print(f"{dir_name} is already exist...")
            exist_file = set(os.listdir(dir_name))
            down_file = set(name_list)
            # 파일명의 교집합이 존재하면, 차집합 다운
            # 파일명의 교집합이 없으면, 다운할 것인지 요청
            if (already_down := exist_file & down_file):
                print('Your download history has been verified, Keep downloading..')
                pass_file = {i : 1 for i in already_down}
            else:
                judge = input('Do you want to download?[Y / N]')
                if judge == 'N' or judge == 'n':
                    exit()

        return pass_file


def pdflink_down(dir_name, links: list):
    for i in tqdm(range(len(links))):
        if pass_file.get(name := name_list[i]):
            continue
        make_url = 'https://openaccess.thecvf.com/' + links[i]

        response = requests.get(make_url)

        with open(f'{dir_name}/{name}', 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    file_name = input("폴더명을 입력하세요: ")
    url = input("링크를 입력하세요: ")

    pdf_links, name_list = url_pdflink_parser(url)  # 다운받을 링크, 파싱한 이름
    pass_file = make_dir(file_name, name_list)  # 다운 필요없는 이름
    pdflink_down(file_name, pdf_links)  # passfile 비교해서 다운로드

