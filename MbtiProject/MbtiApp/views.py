from django.shortcuts import render

# Crawling
from .crawling import dramaCrawling as dc

# DB
from .models import DramaInfo, Character

# Create your views here.
def addDrama(request):
    context = {}

    if request.POST:

        context["title"] = request.POST.get('search')

        context["drama_infos"] = []
        if len(DramaInfo.objects.filter(title__icontains = context["title"])) != 0:
            context['dramas'] = DramaInfo.objects.filter(title__icontains = context["title"])
            for drama in context["dramas"]:
                context["drama_infos"].append({"drama":drama, "characters":Character.objects.filter(drama=drama)})
            context["db"] = True
        # 2-2. 없다면 db = False
        else:
            context['db'] = False
        # 3. 아래 pass 지우기

    return render(request, "addDrama.html", context)

def crawlDrama(request, drama_name):
    context = {
        "title":drama_name,   
    }

    # crawling 진행
    try:
        drama = dc.getDrama(drama_name)
        characters = dc.getCharacter(drama_name)
    except:
        # html 변경 예정
        return render(request, "adddrama.html", context)
    context["db"] = True

    drama = DramaInfo.objects.create(
        title=drama["title"],
        image=drama["poster"],
        plot=drama["plot"],
        site=drama["main_home"]
    )
    context["dramas"] = [drama]

    for character in characters:
        Character.objects.create(
            drama = drama,
            name = character["name"],
            poster = character["picture"],
            description = character["describe"],
            # 키워드 뽑아내기
            personal = "#훗",
            # mbti model 결과
            mbti = "INTJ"
        )
    context["character"] = Character.objects.filter(drama=drama)

    return render(request, "addDrama.html", context)