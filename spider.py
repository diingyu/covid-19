################################################################################################################
# in this file, we spider the data from a dada source at github.
# then we save the data in a file which is in the list_data directory.
# the data in file is json format
# you can use it by json.loads() function
# written at Apr 17th 2020
################################################################################################################

from bs4 import BeautifulSoup
# from selenium import webdriver
import json
import sys
from MACRO import DATE
import os

# DATE = '04-24-2020'
CSV_FILE = DATE + '.csv'
BASE_URL = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/'
URL = BASE_URL + CSV_FILE


def sum_by_country(raw_data):
    country = list()
    for item in raw_data:
        if item[0] not in country:
            country.append(item[0])

    sum_data = list()
    for c in country:
        confirmed = 0
        cured = 0
        dead = 0
        for item in raw_data:
            if item[0] == c:
                try:
                    confirmed += int(item[2])
                    cured += int(item[4])
                    dead += int(item[3])
                except ValueError:
                    save_data(item, 'error.txt')
                    print("error")
                    # sys.exit(2)
                    # print('data error:', item)
                    # continue
        sum_data.append([c, confirmed, cured, dead])
        print(c, confirmed, cured, dead)
    return sum_data


def save_data(list_data, file):
    f = open(file, 'w')
    f.write(json.dumps(list_data))
    f.close()


def get_raw_data_from_local_file(file):
    f = open(file)
    text = f.read()
    f.close()

    tbody = BeautifulSoup(text, 'html.parser')
    allTr = tbody.find_all('tr')
    rawData = ''

    for tr in allTr:
        allTd = tr.find_all('td')
        rawData += allTd[1].text.replace('\n', '') + '\n'

    f = open('raw/' + DATE + '.csv', 'w')
    f.write(rawData)
    f.close()


if __name__ == "__main__":
    # print(os.getcwd())
    # sys.exit(1)

    # from html to csv, saved as a csv file in csv directory
    get_raw_data_from_local_file('html/' + DATE + '.html')
    sys.exit(10)

    browser = webdriver.Chrome()
    browser.get(URL)
    text = browser.find_element_by_tag_name('tbody').get_attribute('innerHTML')
    tbody = BeautifulSoup(text, 'html.parser')
    allTr = tbody.find_all('tr')
    rawData = list()
    for tr in allTr:
        allTd = tr.find_all('td')
        rawData.append([allTd[4].text, allTd[5].text, allTd[8].text, allTd[9].text, allTd[10].text])
        # rawData.append([allTd[2].text, allTd[3].text, allTd[4].text, allTd[5].text, allTd[6].text])
    data = sum_by_country(rawData)
    save_data(data, 'list_data/' + DATE + '.txt')
    browser.close()
    browser.quit()
    sys.exit(0)
