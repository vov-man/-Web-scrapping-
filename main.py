import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
import re



url = "https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=python"
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

reg = requests.get(url, headers = headers)
src = reg.text


soup = BeautifulSoup(src, "lxml")
link_main = soup.find_all("div", class_="vacancy-serp-item-body__main-info")
all_vaccansy = []

count=0

for link_vaccancy in link_main: 
    name_vaccancy = link_vaccancy.find("a", class_="serp-item__title").text
    link = link_vaccancy.find("a", class_="serp-item__title").get("href")
    city = link_vaccancy.find("div", attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
    name_company = link_vaccancy.find("a", attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
    #salary = link_vaccancy.find("span", attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
    page_vaccancy = requests.get(link, headers=headers).text
    soup_page_vaccancy = BeautifulSoup(page_vaccancy, "lxml")
    #salary = soup_page_vaccancy.find("span", attrs={'data-qa': 'vacancy-salary-compensation-type-gross'})
    salary = soup_page_vaccancy.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite").text
    page_text = soup_page_vaccancy.find("div", class_="g-user-content")
    
    django_find = re.findall('Django', str(page_text))
    Flask_find = re.findall('Flask', str(page_text))
    if django_find or Flask_find == None:
        all_vaccansy.append(
        {
            "name_vaccancy": name_vaccancy,
            "ссылка": link,
            "вилка зп": str(salary),
            "город": city,
            "название компании": name_company
        }
    )
    else:
        pass

with open("vaccancy_dict.json", "w", encoding="utf-8") as file:
   json.dump(list(all_vaccansy), file, indent=4, ensure_ascii=False)






    
    




