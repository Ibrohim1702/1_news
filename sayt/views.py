from django.shortcuts import render, HttpResponse

from sayt.helper import valyutalar, menu_ctgs
from sayt.models import Category, new, Contact, Comment


# Create your views here.


def index(requests):
    ctg = Category.objects.get(key='ozbekiston')
    jahon = Category.objects.get(key='jahon')
    jamiyat = Category.objects.get(key='jamiyat')
    siyosat = Category.objects.get(key='siyosat')
    sport = Category.objects.get(key='sport')
    uzb = Category.objects.get(key='ozbekiston')
    fan_tex = Category.objects.get(key='fan_texnika')

    ja_big_news = new.objects.filter(ctg=jahon).order_by("-pk")
    ja_news = new.objects.filter(ctg=jahon)
    si_news = new.objects.filter(ctg=siyosat)
    uzb_news = new.objects.filter(ctg=uzb)
    tex_news = new.objects.filter(ctg=fan_tex)


    sport_news = new.objects.filter(ctg=sport)
    sport_news2 = new.objects.filter(ctg=sport)
    sport_big_news = new.objects.filter(ctg=sport)

    jam_news = new.objects.filter(ctg=jamiyat).order_by("-pk")



    fresh = new.objects.all().order_by("-pk")
    news = new.objects.all().order_by('-pk')
    pop = new.objects.all().order_by('-views')
    eko = Category.objects.get(key='iqtisodiyot')
    iqtisodiyot = new.objects.filter(ctg=eko).order_by("-pk")

    print(jam_news)

    ctx = {
        "valyutalar": valyutalar(),
        "menu_ctgs": menu_ctgs(),
        "big": news[0],
        'news': news[1:],
        "fresh": fresh,
        "pop": pop,
        "ja_news": ja_news,
        "si_news": si_news[2:],
        "si_news2": si_news[2:5],
        "si_news3": si_news[5:8],
        "jam_news": jam_news[1:],
        "jam_big_news": jam_news[0],
        "ja_big_news": ja_big_news[0],
        "si_big_news": si_news[:2],
        "iqtisodiyot": iqtisodiyot,
        "eko": eko,
        "tex_news": tex_news[:4],
        "sport_news": sport_news[2:6],
        "sport_big_news": sport_big_news[:2],
        "sport_news2": sport_news2[6:10],
        "uzb_news": uzb_news[:3],


    }
    return render(requests, 'index.html', ctx)


def category(requests, key):
    ctg = Category.objects.get(key=key)
    ctgs_news = new.objects.filter(ctg=ctg).order_by("-pk")
    fresh = new.objects.all().order_by("-pk")
    ctx = {
        "valyutalar": valyutalar(),
        "menu_ctgs": menu_ctgs(),
        "ctg": ctg,
        "ctg_news": ctgs_news[1:],
        "big": ctgs_news[0],
        "fresh": fresh
    }
    try:
        ctx['big'] = ctgs_news[0]
    except:
        pass
    return render(requests, 'category.html', ctx)


def contact(requests):
    if requests.POST:
        post = requests.POST
        if "name" not in post or "phone" not in post or "msg" not in post:
            ctx = {
                "valyutalar": valyutalar(),
                "menu_ctgs": menu_ctgs(),
                "error": True
            }
            return render(requests, 'contact.html', ctx)
        else:
            cnt = Contact()
            cnt.name = requests.POST.get('name')
            cnt.phone = requests.POST.get('phone')
            cnt.msg = requests.POST.get('msg')
            cnt.save()
    ctx = {
        "valyutalar": valyutalar(),
        "menu_ctgs": menu_ctgs()
    }
    return render(requests, 'contact.html', ctx)


def search(requests):
    key = requests.GET.get('s')
    news = new.objects.raw(f"""
        select * from sayt_new
        where lower(titel) like lower('%{key}%')
    """)
    fresh = new.objects.all().order_by("-pk")



    ctx = {
        "valyutalar": valyutalar(),
        "menu_ctgs": menu_ctgs(),
        "key": key,
        "news": news,
        "fresh": fresh
    }

    try:
        ctx['len'] = len(news)
    except:
        ctx['len'] = 0
    return render(requests, 'search.html', ctx)


def view(requests, pk):
    news = new.objects.get(id=pk)
    news.views = news.views + 1
    news.save()
    fresh = new.objects.all().order_by("-pk")
    if requests.POST:
        ism = requests.POST.get('ism')
        comment = requests.POST.get('izoh')
        Comment.objects.create(
            author=ism, izoh=comment, new=news
        )

    comments = Comment.objects.filter(new=news)
    ctx = {
        "valyutalar": valyutalar(),
        "menu_ctgs": menu_ctgs(),
        "new": news,
        "fresh": fresh,
        "comments": comments,
        "cmt_cnt": len(comments)
    }

    return render(requests, 'view.html', ctx)
