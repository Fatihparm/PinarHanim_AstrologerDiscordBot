import requests
from bs4 import BeautifulSoup
from data_models import ZodiacSign, TarotCard , Model

horoscope_signs = [
    "balik", "kova", "oglak", "yay", "akrep", "terazi",
    "basak", "aslan", "yengec", "ikizler", "boga", "koc"
] # Turkish names of zodiac signs

model = Model()

def get_sign_link_set():
    url = "https://onedio.com/gunluk-burc-yorumlari-haberleri"
    base_url = "https://onedio.com"
    response = requests.get(url)
    page = BeautifulSoup(response.content, "html.parser")
    link_list = []
    link_set = set()
    deadline = ""
    link_day = ""
    content = page.find_all("a")
    links = [link["href"] for link in content if "-burcu-gunluk-burc-" in link["href"]] # filter out unnecessary links
    for link in links:
        link_day = link.split('/')[2].split('-')[0]
        if deadline == "": 
            deadline = link_day # deadline is the day of the first link in the list
        if link_day == deadline: 
            link_list.append(base_url + link)
    link_set = list(set(link_list)) # set() removes duplicates
    return link_set

def sign_content_push():
    link_list = get_sign_link_set()
    for link in link_list:
        response = requests.get(link)
        page = BeautifulSoup(response.content, "html.parser")
        caption = page.find("figcaption")
        content = caption.find_all("p")
        text = content[0].text + content[1].text
        name = link.split('-')[2] 
        date = link.split('/')[4].split('-')[0]
        sign = ZodiacSign(name, text, date)
        model.insert_zodiac_sign(sign)

def get_tarot_link():
    url = "https://onedio.com/yasam/astroloji/tarot-fali"
    base_url = "https://onedio.com"
    response = requests.get(url)
    page = BeautifulSoup(response.content, "html.parser")
    content = page.find("div", class_="flex flex-col my-auto px-8 py-0")
    link = content.find("a")["href"]
    return base_url + link

def tarot_content_push():
    link = get_tarot_link()
    
    response = requests.get(link)
    page = BeautifulSoup(response.content, "html.parser")
    
    content = page.find("article", class_="article px-4 sm:px-0 sm:pt-7.5 relative quiz")
    sections = content.find_all("section", class_="entry entry--image image content-visibility-entry")
    
    for section in sections:
        name = section.find("h2").text
        description = section.find("p").text
        image = section.find("img")["src"]
        tarot= TarotCard(name, description, image)
        model.insert_tarot_card(tarot)

