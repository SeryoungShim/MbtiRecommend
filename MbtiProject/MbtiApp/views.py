from django.shortcuts import render

# Crawling
from .crawling import dramaCrawling as dc

# DB
from .models import DramaInfo, Character

# Create your views here.
def addDrama(request):
    context = {}

    if request.POST:
        #print(dc.getDrama("넝쿨째 굴러온 당신"))
        context["title"] = request.POST.get('search')
        # 1. POST search 값 변수에 저장 - context["title"] 에 저장
        # 2. db 드라마 제목에서 search 값이 있는지 확인
        # 2-1. 있다면 db = True / drama = db읽어오기
        if len(DramaInfo.objects.filter(title = context["title"])) != 0:
            title = DramaInfo.objects.get(title = context["title"])
            context['drama'] = title
            context["db"] = True
        # 2-2. 없다면 db = False
        else:
            context['db'] = False
        # 3. 아래 pass 지우기

    return render(request, "addDrama.html", context)

def crawlDrama(request, drama_name):
    context = {
<<<<<<< HEAD
        "title":drama_name,
    }

    # crawling 진행 - 세령
    
=======
        "title":drama_name,   
    }

    # crawling 진행 - 세령
    drama = dc.getDrama(drama_name)
    characters = dc.getCharacter(drama_name)
    context["db"] = True

    drama = DramaInfo.objects.create(
        title=drama["title"],
        image=drama["poster"],
        plot=drama["plot"],
        site=drama["main_home"]
    )
    context["drama"] = drama

    for character in characters:
        Character.objects.create(
            drama = drama,
            name = character["name"],
            poster = character["picture"],
            description = character["describe"],
            personal = "#훗",
            mbti = "INTJ"
        )
    context["character"] = Character.objects.filter(drama=drama)
>>>>>>> 44bfbcafcabcf0c28caf90ca381569e146efdf78

    return render(request, "addDrama.html", context)