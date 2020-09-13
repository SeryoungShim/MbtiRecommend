import requests
from bs4 import BeautifulSoup
import relationCrawling as rc

def getCharacter(title):
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query="+ title + " 등장인물"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    char_data = []

    if soup.select('#mflick'):
        link_info = soup.select('#mflick > div > div > ul > li > div > a')

    else:
        link_info = soup.select('div.sc._kgs_broadcast.cs_common_module > div.cm_content_wrap > div > div > ul > li > div.item > a')

    for a in link_info:
        character_link = a['href']
        
        response = requests.get("https://search.naver.com/search.naver"+character_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        character_info = soup.select_one('#main_pack > div.sc.cs_common_module._kgs_broadcast')

        try:
            # 역할 이름
            name = character_info.select_one('div.cm_top_wrap > div.top_answer_area > span.text > strong ').text
        except:
            continue

        # 인물 사진
        picture = character_info.select_one('div.rel_answer_wrap._accordion > div > div.area_thumb._thumb > div > img')['src']

        # 인물 설명
        describe = character_info.select_one('div.rel_answer_wrap._accordion > div > div.detail_info > div > span').get_text()

        cha = {'name': name,
        'picture': picture,
        'describe': describe}

        char_data.append(cha)

    return char_data


def getDrama(title):
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=" + title

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    drama_info = soup.select('div.sc._kgs_broadcast.cs_common_module') 

    for info in drama_info:
        # 제목
        title = info.select_one('div.cm_top_wrap._sticky > div.title_area._title_area > h2 > a > strong').text

        # 편성
        media = info.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > dl > div > dd > a').text

        # 줄거리
        plot = info.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > div.text_expand._ellipsis._img_ellipsis > span').text

        # 포스터
        poster = info.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > a > img')['src']

        # 공홈
        main_home = info.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > a')['href']

        try:
            rel_poster = None
            if media == "JTBC":
                rel_url = rc.getJtbc(title, main_home)
                rel_poster = rc.getJtbcRel(rel_url)
            if media == "tvN":
                rel_poster = rc.getTvn(main_home)
            if media == "MBC":
                rel_poster = rc.getMbc(main_home)

            if rel_poster:
                poster = rel_poster
        except:
            pass

        drama = {
            'title' : title,
            'media': media,
            'plot' : plot,
            'poster' : poster,
            'main_home' : main_home
        }

    return drama

print(getDrama(input(" >> ")))