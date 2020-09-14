from django.shortcuts import render

# Crawling
from .crawling import dramaCrawling as dc

# Create your views here.
def addDrama(request):
    context = {}
    if request.POST:
        # print(dc.getDrama("넝쿨째 굴러온 당신"))

        # 1. POST search 값 변수에 저장 - context["title"] 에 저장
        # 2. db 드라마 제목에서 search 값이 있는지 확인
        # 2-1. 있다면 db = True / drama = db읽어오기
        # 2-2. 없다면 db = False
        # 3. 아래 pass 지우기
        pass

    return render(request, "addDrama.html", context)

def crawlDrama(request, drama_name):
    context = {
        "title":drama_name,
        "db" : True,    
    }

    # crawling 진행 - 세령

    return render(request, "addDrama.html", context)