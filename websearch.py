import requests, socket
from bs4  import BeautifulSoup
from urllib.parse import urlparse


'''
    Inputs:
        None
    Returns:
        ip_address - adres ip domeny danej strony
        
    Funkcja anazlizuje dana strone pod katem linkow i maili, zapisuje je do dwoch plikow txt
'''
def websearch():
    # Pobieramy adres strony od uzytkownika i sprawdzamy jego poprawnosc
    url = input("Podaj adres strony: ")
    if not 'https://' in url: 
        url = 'https://' + url
    try:
        web_html = requests.get(url).text
    except Exception as e:
        print(f'Wystapil blad przy probie otwarcia strony: {e}')
        return None
    
    # Tu pobieramy adres ip domeny
    try:
        parsed_url = urlparse(url)                  # Tworzymy obiekt z danymi o domenie
        domain = parsed_url.netloc                  # Zapisujemy domene do oddzielnej zmiennej
        ip_address = socket.gethostbyname(domain)   # Pobieramy adres ip i go wyswietlamy
        print(f'Adres ip domeny: {ip_address}')
    except Exception as e:
        print(f'Blad przy pobieraniu adresu ip: {e}')
        return None
    
    # Tu rozpoczyna sie analiza strony pod katem adresow mail oraz linkow + zapis tych danych do plikow
    print('Rozpoczynam analize strony...')
    
    # Znajdujemy kazdy znacznik <a></a>
    links = BeautifulSoup(web_html, 'html.parser').find_all('a')
    
    # Dodajemy naglowki do plikow - ip domeny oraz link danej strony
    divider = '='*50
    with open('links.txt', 'a') as file:
        file.write(f'{divider}\nAdres ip: {ip_address}\nLinks in: ' + url + '\n\n')
    with open('mails.txt', 'a') as file:
        file.write(f'{divider}\nAdres ip: {ip_address}\nMails in: ' + url + '\n\n')
        
    # Ze znalezionych znacznikow wybieramy tylko dane z atrybutow href
    for link in links:
        data = link.get('href')
        if data.startswith('http'):                 # Strony w zaczynaja sie od http, wiec zapisujemy je do pliku links.txt
            with open('links.txt', 'a') as file:
                file.write(data + '\n')
        elif data.startswith('mailto'):             # Maile zaczynaja sie od mailto, wiec zapisujemy je do pliku mails.txt
            with open('mails.txt', 'a') as file:
                data = data.lstrip('mailto:')
                file.write(data + '\n')
    print("Dane o mailach i linkach zapisane do plikow 'mails.txt' oraz 'links.txt'")
    
    return ip_address

websearch()