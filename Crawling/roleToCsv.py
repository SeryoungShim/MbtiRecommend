import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_roles(tvTitle):
    URL = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=' + tvTitle + " 등장인물"

    role_urls = {}
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    names = soup.select("div.list_image_info > ul > li > div > div > strong")
    for name in names:
        role_name = name.text.split()[0]
        role_urls[role_name] = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=' + tvTitle + " " + role_name
    return role_urls

def get_role_desc(urls):
    description = {}
    for name in urls.keys():
        response = requests.get(urls[name])
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            description[name] = soup.select_one("div.detail_info > div > span.desc._text").text
        except:
            pass
    return description

def main():
    dramas = pd.read_csv("Drama_mbti.csv")
    titles = dramas.iloc[:,0]
    for title in titles:
        drama_title = re.sub("[:\-\,!\"]", " ", title)
        urls = get_roles(drama_title)
        description = get_role_desc(urls)
        current_title = [title] * len(description)
        current_name = list(description.keys())
        current_desc = list(description.values())
        df = pd.DataFrame({"title":current_title, "name":current_name, "desc":current_desc})
        print(df)
        df.to_csv('roles.csv', mode='a', header=False, index=False)

main()