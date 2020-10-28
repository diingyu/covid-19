from datetime import datetime, timedelta
import json


LAST_DATE = datetime(2020, 10, 27)
DATE = LAST_DATE.strftime('%m-%d-%Y')


def get_date_ser(date):
    date_list = list()
    for i in range(14):
        date_list.append((date+timedelta(days=i-6)).strftime('%d'))
    return date_list


X1 = get_date_ser(LAST_DATE)


def sort_country(file):
    f = open(file)
    list_data = json.loads(f.read())
    return sorted(list_data, key=lambda i: i[1], reverse=True)


def get_top10(sorted_input):
    top10 = list()
    for i in range(10):
        top10.append(sorted_input[i][0])  # get the country name
    f = open('top10.txt', 'w')
    f.write(json.dumps(top10))
    f.close()
    return top10


def get_country(sorted_input):
    country = list()
    for item in sorted_input:
        country.append(item[0].replace('*', ''))
    return country
