from django.shortcuts import render, redirect

# Crawling
from .crawling import dramaCrawling as dc

# DB
from .models import DramaInfo, Character

# Create your views here.
def home(request):
    return render(request, "start.html")

def mbti_home(request):
    return render(request, "mbti_home.html")

def mbti(request, quiz):
    if "select" not in request.session.keys():
        request.session["select"] = []
    if request.POST:
        request.session["select"] = request.session["select"] + [request.POST["select"]]
    return render(request, "quiz" + str(quiz) + ".html")

def result(request):
    if request.POST:
        request.session["select"] = request.session["select"] + [request.POST["select"]]

    # 여기서 mbti 계산
    context = {
        "mbti" : request.session["select"]
    }
    return render(request, "result.html", context)


### admin page "/adddrama/"
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
        else:
            context['db'] = False

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
        # 크롤링 실패 --> 직접 입력
        return render(request, "form.html", context)
    context["db"] = True

    drama = DramaInfo.objects.create(
        title=drama["title"],
        image=drama["poster"],
        plot=drama["plot"],
        site=drama["main_home"]
    )

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
    context["drama_infos"] = [{"drama": drama, "characters": Character.objects.filter(drama=drama)}]

    return render(request, "addDrama.html", context)

def insertDrama(request):
    context = {}
    
    if request.method == "POST":

        drama = DramaInfo.objects.create(
            title = request.POST['title'],
            plot = request.POST['plot'],
            image = request.POST['image'],
            site = request.POST['site']
        )
        
        # context["drama_infos"] = {"drama":drama}
        names = request.POST.getlist('name[]')
        posters = request.POST.getlist('poster[]')
        desc = request.POST.getlist('desc[]')
        for i in range(len(names)):
            Character.objects.create(
                drama = drama,
                name = names[i],
                poster = posters[i],
                description = desc[i],
                personal = "#훗",
                mbti = "INTJ"
            )
        
        
    return render(request, "addDrama.html", context)
