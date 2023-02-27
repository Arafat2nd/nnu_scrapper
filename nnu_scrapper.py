from re import sub

from bs4 import BeautifulSoup
import requests


def snake_case(s):
    sub('[^A-Za-z0-9]+', '', s)
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def nnu_scrapper(link_en):
    soup = BeautifulSoup(requests.get(link_en).text, features="html.parser")
    for j in range(len(soup.find_all('table')) - (1 if free_less == False else 0)):
        if j == 0:
            continue
        tables = soup.find_all('table')[j]
        rows = []
        trs = tables.find_all('tr')
        for i, row in enumerate(trs):
            if i == 0:
                continue
            else:
                rows.append([el.text.strip() for el in row.find_all('td')])
        for row in rows:
            if len(row) > 1:
                values_en.update({snake_case(str(row[1])): row[1]})
    link_en = link_en.replace('en', 'ar', 1)
    with open(major + '_en.txt', 'w', encoding='utf-8') as convert_file:
        convert_file.write(str(values_en))
    nnu_scrapper_with_keys(link_en, list(values_en.keys()))


def nnu_scrapper_with_keys(link_ar, keys):
    soup = BeautifulSoup(requests.get(link_ar).text, features="html.parser")
    index_of_keys = 0
    for j in range(len(soup.find_all('table')) - (1 if free_less == False else 0)):
        if j == 0:
            continue
        tables = soup.find_all('table')[j]
        rows = []
        trs = tables.find_all('tr')
        for i, row in enumerate(trs):
            if i == 0:
                continue
            else:
                rows.append([el.text.strip() for el in row.find_all('td')])
        for row in rows:
            if len(row) > 1:
                values_ar.update({keys[index_of_keys]: row[1]})
                index_of_keys += 1
    with open(major + '_ar.txt', 'w', encoding="utf-8") as convert_file:
        convert_file.write(str(values_ar))


def has_free():
    free = title.find_all('h4', class_='text-bold')
    free_index = free[len(free) - 1].text
    if free_index.__eq__('Free Courses'):
        return True
    return False


values_en = {}
values_ar = {}
while True:
    values_en.clear()
    values_ar.clear()
    link = input('Enter the english link cunt:')
    title = BeautifulSoup(requests.get(link).text, features="html.parser")
    holder = title.find('div', class_='f24 dark-blue margin-btm-md').text
    major = holder.replace('\n', '')
    free_less = has_free()
    nnu_scrapper(link)

    print('Your files are ready lazy asshole\n')
