import time

from requests_html import HTMLSession
import datetime
import requests

url = "https://www.njoftimefalas.com/name.php"
params = {
    'name': 'ads_advertise',
    'ads_advertise': 'njoftime',
    'njoftime': 'ads_list',
    'idk': 4,
    'page': 1
}
session = HTMLSession()
announcements = []
latest_title = "Jepet Me Qera Shtepia Shtepia 2+1"


def convert_to_date(string_date):
    date_year = string_date.split(" ")[0].split("/")[2]
    date_month = string_date.split(" ")[0].split("/")[1]
    if date_month[0] == '0':
        date_month = date_month[1]
    date_day = string_date.split(" ")[0].split("/")[0]
    if date_day[0] == '0':
        date_day = date_day[1]
    date_hour = string_date.split(" ")[1].split(":")[0]
    date_minute = string_date.split(" ")[1].split(":")[1]
    return datetime.datetime(int(date_year), int(date_month), int(date_day), int(date_hour), int(date_minute))


def find_latest_article(latest_title):
    r = session.get(url, params=params)
    r.html.render(timeout=10)
    category_list = r.html.find('.category-list', first=True)
    announcement_list = category_list.find('.item-list')
    for item in announcement_list:
        if len(item.find('.cornerRibbons')) != 1:
            title_object = item.find('.add-title', first=True)
            title = title_object.find('a', first=True).text
            price = title_object.find('strong', first=True).text.split(" ")[0].split("\n")
            location = item.find('.item-location', first=True).find('a', first=True).text
            date = item.find('.info-row')[1].text.split("...")
            date_value = date[len(date) - 2].strip()
            if date_value[0] == ".":
                date_value = date_value.lstrip(".").strip()
            announcement = {
                'title': title,
                'price': price[0],
                'unit': price[1],
                'location': location,
                'date': date_value
            }
            announcements.append(announcement)
            if latest_title == announcement['title']:
                break
    return announcements[0]['title']


def retrieve_data(latest_title, announcements):
    while True:
        r = session.get(url, params=params)
        r.html.render(timeout=10)
        category_list = r.html.find('.category-list', first=True)
        announcement_list = category_list.find('.item-list')
        for item in announcement_list:
            if len(item.find('.cornerRibbons')) != 1:
                title_object = item.find('.add-title', first=True)
                title = title_object.find('a', first=True).text
                price = title_object.find('strong', first=True).text.split(" ")[0].split("\n")
                location = item.find('.item-location', first=True).find('a', first=True).text
                date = item.find('.info-row')[1].text.split("...")
                date_value = date[len(date) - 2].strip()
                if date_value[0] == ".":
                    date_value = date_value.lstrip(".").strip()
                announcement = {
                    'title': title,
                    'price': price[0],
                    'unit': price[1],
                    'location': location,
                    'date': date_value
                }
                if latest_title == announcement['title']:
                    break
                else:
                    print(announcement)
                    announcements.append(announcement)
        if len(announcements) != 0:
            latest_title = announcements[0]['title']
            announcements = []
        print("------------------------------------------------------------------------------------------")
        time.sleep(2)


#
#
# latest_title = find_latest_article(latest_title)
# print(latest_title)
# retrieve_data(latest_title, announcements)
