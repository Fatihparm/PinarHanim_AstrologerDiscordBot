import requests
from bs4 import BeautifulSoup
from data_models import ZodiacSign, TarotCard


horoscope_signs = [
    "balik", "kova", "oglak", "yay", "akrep", "terazi",
    "basak", "aslan", "yengec", "ikizler", "boga", "koc"
]

def get_link_list():
    url = "https://onedio.com/gunluk-burc-yorumlari-haberleri"
    base_url = "https://onedio.com"
    response = requests.get(url)
    page = BeautifulSoup(response.content, "html.parser")
    link_list = []

    deadline = ""
    link_day = ""

    for link in page.find_all("a"):
        if "-burcu-gunluk-burc-" in link["href"]:
            url_link = link["href"]
            link_day = url_link.split('/')[2].split('-')[0]
            
            if not deadline:
                deadline = link_day
            
            if link_day == deadline: 
                link_list.append(base_url + url_link)
    return link_list


def get_content():
    link_list = get_link_list()
    sign_dictionary = {}
    for i in link_list:
        response = requests.get(i)
        page = BeautifulSoup(response.content, "html.parser")
        section = page.find("section", class_="entry entry--image image")
        content = section.find("p").text
        name = i.split('-')[2]
        date = i.split('/')[4].split('-')[0]
        sign_dictionary[name] = ZodiacSign(name, content, date)
    return sign_dictionary


def get_tarot_link():
    url = "https://onedio.com/yasam/astroloji/tarot-fali"
    base_url = "https://onedio.com"
    
    response = requests.get(url)
    page = BeautifulSoup(response.content, "html.parser")
    
    content = page.find("div", class_="flex flex-col my-auto px-8 py-0")
    link = content.find("a")["href"]
    
    return base_url + link


def get_tarot_content():
    link = get_tarot_link()
    response = requests.get(link)
    page = BeautifulSoup(response.content, "html.parser")
    content = page.find("article", class_="article px-4 sm:px-0 sm:pt-7.5 relative quiz")
    sections = content.find_all("section", class_="entry entry--image image")
    
    tarot_cards = []
    id = 0
    for section in sections:
        name = section.find("h2").text
        id += 1
        description = section.find("p").text
        image = section.find("img")["src"]
        tarot_cards.append(TarotCard(name, id, description, image))
    return tarot_cards
