from django.shortcuts import render, redirect

# Crawling
from .crawling import dramaCrawling as dc

# DB
from .models import DramaInfo, Character

alpha_mbti = {
    "EFNP":"ENFP", "EFJN":"ENFJ", "ENPT":"ENTP", "EJNT":"ENTJ",
    "EFPS":"ESFP", "EFJS":"ESFJ", "EPST":"ESTP", "EJST":"ESTJ",
    "FINP":"INFP", "FIJN":"INFJ", "INPT":"INTP", "IJNT":"INTJ",
    "FIPS":"ISFP", "FIJS":"ISFJ", "IPST":"ISTP", "IJST":"ISTJ"
}

# Create your views here.
def home(request):
    request.session["mbti"] = [""]*12
    return render(request, "start.html")

def mbti_home(request):
    return render(request, "mbti_home.html")

def mbti(request, quiz):
    # if "select" not in request.session.keys():
    #     redirect(home)
    if request.POST:
        if type(request.session["mbti"]) == list:
            mbtis = request.session["mbti"]
            mbtis[quiz-2] = request.POST["select"]
            request.session["mbti"] = mbtis
    print(request.session["mbti"])
    return render(request, "quiz" + str(quiz) + ".html")

def result(request):
    if request.POST:
        if type(request.session["mbti"]) == list:
            mbtis = request.session["mbti"]
            if "select" in request.POST:
                mbtis[-1] = request.POST["select"]
            request.session["mbti"] = mbtis
            print(request.session["mbti"])
            # 여기서 mbti 계산
            lst = list(set(request.session["mbti"]))
            for i in lst:
                if request.session["mbti"].count(i) < 2:
                    request.session["mbti"].remove(i)
            
            mbti = alpha_mbti["".join(sorted(set(request.session["mbti"])))]
            request.session["mbti"] = mbti
        else:
            if "mbti_input" in request.POST:
                mbti = request.POST["mbti_input"].upper()
                request.session["mbti"] = mbti

    print(request.session["mbti"])
    # random 숫자 5개 뽑기
    characters = Character.objects.filter(mbti=request.session["mbti"])[:10]
    context = {
        "same" : "반대",
        "same_url" : "reverse",
        "mbti" : request.session["mbti"],
        "characters" : characters
    }
    return render(request, "result.html", context)

def reverse(request):
    # mbti 반대로
    mbti = request.session["mbti"]
    mbti_reverse=[]
    for i in mbti:
        if "E" == i:
            mbti_reverse.append("I")
        elif "I" == i:
            mbti_reverse.append("E")
        elif 'N' == i:
            mbti_reverse.append("S")
        elif 'S' == i: 
            mbti_reverse.append("N")
        elif "F" == i:
            mbti_reverse.append("T")
        elif "T" == i:
            mbti_reverse.append("F")
        elif "J" == i:
            mbti_reverse.append("P")
        elif "P" == i:
            mbti_reverse.append("J")
    
    characters = Character.objects.filter(mbti="".join(mbti_reverse))[:10]
    # random 5개
    context = {
        "same" : "같은",
        "same_url" : "result",
        "mbti" : request.session["mbti"],
        "characters" : characters
    }
    print("".join(mbti_reverse))

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
