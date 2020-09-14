import requests
from bs4 import BeautifulSoup
import re
import json

# tvn
def getTvn(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    text = soup.select("script")[-1]
    regex = re.compile(r"bCode: \"\d+\"")
    bcode = regex.findall(str(text))[0].split('"')[1]
    regex = re.compile(r"pCode: \"\d+\"")
    pcode = regex.findall(str(text))[0].split('"')[1]

    headers = {
        'Referer': url,
    }

    params = (
        ('udate', '2020091117'),
        ('callback', 'cMenuList'),
        ('bCode', bcode),
        ('pCode', pcode),
        ('lCode', '0'),
    )

    response = requests.get(f'http://img.lifestyler.co.kr/uploads/program/menu/1/menu.{pcode}.Release.js', headers=headers, params=params, verify=False)
    if(response.status_code == 404):
        response = requests.get(f'http://img.lifestyler.co.kr/uploads/program/menu/2/menu.{pcode}.Release.js', headers=headers, params=params, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    menu_dict = json.loads(str(soup).split("cMenuList(")[1][:-1])

    for i in menu_dict["MenuList"]:
        if(i["MenuName"]["ko_KR"].replace(" ", "") == "인물관계도"):
            rel_url = i["MenuUrl"]
            break
        if "MenuDepth2" in i:
            for depth in i["MenuDepth2"]:
                if(depth["D2Name"]["ko_KR"].replace(" ", "") == "인물관계도"):
                    rel_url = depth["D2MUrl"]
    response = requests.get(rel_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        img = soup.select_one("div.majorImg > img")
        return img["src"]
    except:
        img = soup.select_one("div.module-innerbox > style")
        regex = re.compile(r"url(.+\.jpg)")
        img = regex.findall(str(img))[0][1:]
        return img

# JTBC
def getJtbc(title, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    dls = soup.select("div.pro_gnb > div > dl")
    for dl in dls:
        if (dl.select_one("dt").text.strip() == title) :
            li = dl.select("dd > ul > li")[-1]
            return li.select_one("a")["href"]

def getJtbcRel(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    if len(soup.select("div.actor_select_list")) > 1:
        return soup.select("div.actor_select_list")[1].select_one("img")["src"]
    return

def getMbc(url):
    response = requests.get(url+"cast/")
    if(response.status_code != 200):
        response = requests.get(url + "relation/")
    soup = BeautifulSoup(response.text, "html.parser")
    for img in soup.select("img"):
        if "jpg" in img["src"]:
            return img["src"]
    return
