import requests as re

from sayt.models import Category


def valyutalar():
    url = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"
    requests = re.get(url)
    return requests.json()



def menu_ctgs():
    return Category.objects.filter(is_menu = True)