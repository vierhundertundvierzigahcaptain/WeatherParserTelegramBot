from bs4 import BeautifulSoup as BS
from html2image import Html2Image
import requests


def get_weather(city):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
    }

    link = f'https://www.google.com/search?q=weather+in+{city}'
    response = requests.get(link, headers=headers)
    soup = BS(response.text, 'lxml')

    datetime = soup.select("#wob_dts")[0].getText()
    temperature = soup.select("#wob_tm")[0].getText()
    status = soup.select("#wob_dc")[0].getText()
    humidity = soup.select("#wob_hm")[0].getText()
    wind = soup.select("#wob_ws")[0].getText()

    return datetime, status, temperature, humidity, wind


def values_to_image(datetime, city, temperature, status, humidity, wind):
    with open(r'for_img//index.html', 'r', encoding='UTF-8') as f:
        file = f.read()
    soup = BS(file, 'lxml')

    time = ''
    date = ''
    temp = datetime
    for i in temp:
        if i != ' ':
            temp = temp.replace(i, '')
        else:
            break
    time = temp.replace(' ', '')
    date = datetime.strip(time).replace(' ', '')

    soup.find(class_="time").string = time
    soup.find(class_="date").string = date
    soup.find(class_="city").string = city
    soup.find(class_="temperature").string = temperature + "°C"
    soup.find(class_="status").string = status
    soup.find(class_="humidity_value").string = humidity
    soup.find(class_="wind_value").string = wind

    with open("for_img//index.html", "w", encoding='utf-8') as file:
        file.write(str(soup))


def get_image():
    hti = Html2Image(size=(502, 502))

    hti.screenshot(
        html_file='for_img//index.html', css_file='for_img//styles.css',
        save_as='index.jpg'
    )
