import requests
from bs4 import BeautifulSoup
import relationCrawling as rc

def getCharacter(title):
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query="+ title + " 등장인물"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    char_data = []

    link_info = soup.select('div.sc._kgs_broadcast.cs_common_module > div.cm_content_wrap > div > div > ul')

    for info in link_info:
        link = info.select('li > div.item > a')
        for a in link:
            character_link = a['href']

            response = requests.get("https://search.naver.com/search.naver"+character_link)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            character_info = soup.select('#main_pack > div.sc.cs_common_module._kgs_broadcast')
            for info in character_info :

                # 역할 이름
                nam = info.select_one(' div.cm_top_wrap > div > span.text > strong ')
                name = nam.get_text()
                
                # 인물 사진
                pic = info.select_one(' div.cm_content_wrap > div > div > div.rel_answer_wrap._accordion > div > div.area_thumb._thumb > div > img ')
                picture = pic['src']

                # 인물 설명
                des = info.select_one(' div.cm_content_wrap > div > div > div.rel_answer_wrap._accordion > div > div.detail_info > div > span' )
                describe = des.get_text()

                cha = {
                    'name': name,
                    'picture': picture,
                    'describe': describe
                }

                char_data.append(cha)
    return char_data


def getDrama(title):
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=" + title

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    drama_info = soup.select('div.sc._kgs_broadcast.cs_common_module') 

    for info in drama_info:
        # 제목
        tit = info.select_one('div.cm_top_wrap._sticky > div.title_area._title_area > h2 > a > strong')
        title = tit.get_text()

        # 편성
        media = info.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > dl > div > dd > a')
        media_name = media.get_text()

        # 줄거리
        plt = info.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > div.text_expand._ellipsis._img_ellipsis > span')
        plot = plt.get_text()

        # 포스터
        pos = info.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > a > img')
        poster = pos['src']

        # 공홈
        homepage = info.select_one('div.cm_content_wrap > div.cm_content_area._scroll_mover > div.cm_info_box > div.detail_info > a')
        main_home = homepage['href']

        rel_poster = None
        if media_name == "JTBC":
            rel_url = rc.getJtbc(title, main_home)
            rel_poster = rc.getJtbcRel(rel_url)
        if media_name == "tvN":
            rel_poster = rc.getTvn(main_home)
        if media_name == "MBC":
            rel_poster = rc.getMbc(main_home)

        if rel_poster:
            poster = rel_poster

        drama = {
            'title' : title,
            'media_name': media_name,
            'plot' : plot,
            'poster' : poster,
            'main_home' : main_home
        }

    return drama

print(getCharacter(input(" >> ")))