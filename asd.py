import requests
from bs4 import BeautifulSoup

def get_link_set():
    url = "https://onedio.com/gunluk-burc-yorumlari-haberleri"
    base_url = "https://onedio.com"
    response = requests.get(url)
    page = BeautifulSoup(response.content, "html.parser")
    link_list = []
    link_set = set()

    deadline = ""
    link_day = ""

    content = page.find_all("a")
    links = [link["href"] for link in content if "-burcu-gunluk-burc-" in link["href"]]

    for link in links:
        link_day = link.split('/')[2].split('-')[0]
        
        if not deadline:
            deadline = link_day
            
        if link_day == deadline: 
            link_list.append(base_url + link)

    link_set = list(set(link_list))
    return link_set

a = get_link_set()
print(len(a))
for i in a:
    print(i)