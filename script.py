import io
import requests
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
place = "Населено място: "
adress = "Адрес: "
phone = "Телефон: "
email = "E-mail: "
not_needed_1 = "ЗДРАВЕН ФОРУМ ПО ТЕМАТА"
not_needed_2 = "АНКЕТА"
not_needed_3 = "НАЙ-НОВОТО ВЪВ ФОРУМА"

open('result.txt', 'w').close()

def get_HTML(url):
    result = requests.get(url)
    result.encoding = 'windows-1251'
    html = result.text
    return html

def get_info_for_page(url):
    parsed_html = BeautifulSoup(url)
    result = ""
    for element in parsed_html.find_all("div", {"id": "info"}):
        for child in element.children:
            if place in child.text or adress in child.text or phone in child.text or email in child.text:  
                text = child.text.replace(place, '').replace(adress, '').replace(phone, '').replace(email, '')
                result += text
                result += "|"
                result = result.replace('\n','')
    with io.open('result.txt', 'a', encoding='utf-8') as f:
        f.write(result)
        f.write("\n")
    #print (result)
    

def get_pharmacies_for_region(url):
    page_num=1
    ht = get_HTML(url+'?vars=24,'+str(page_num)+',0,0')
    page = BeautifulSoup(ht)
    count = 1
    pages_menu = page.find("div", class_="ui pagination menu")
    for page_n in pages_menu.children:
        if count == len(pages_menu.contents)-1:
            pageCount = int(page_n.text)
        count=count+1
    for page_num in range(1,pageCount+1):
        page = get_HTML(url+'?vars=24,'+str(page_num)+',0,0')
        parsed_html = BeautifulSoup(page)
        for element in parsed_html.find_all("h2", class_="header"): 
            atag = element.find_all("a", href=True)
            for el in atag:
                txt = el.text.replace(not_needed_1, '').replace(not_needed_2, '').replace(not_needed_3, '')
                txt.strip()
                if txt != "" and txt != '\n': 
                    with io.open('result.txt', 'a', encoding='utf-8') as f:
                        f.write(txt)
                        f.write("|")
                    #print(txt,"|", end = ''),
                    link = el['href']
                    newHTML = get_HTML(link)
                    get_info_for_page(newHTML)

mainPage = get_HTML("https://spravochnik.framar.bg/%D0%B0%D0%BF%D1%82%D0%B5%D0%BA%D0%B8")
main_parsed_html = BeautifulSoup(mainPage)
elem = main_parsed_html.find("ul", class_="ui list tree")
atag = elem.find_all("a", href=True)
for el in atag:
    link = el['href']
    get_pharmacies_for_region(link)
