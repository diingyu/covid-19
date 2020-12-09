#########################################################################################
# some useful functions supplied here
# add_record() find the list dump file in list_data directory
# while the file name defined by the MACRO DATE on the top of this file
# add_record() will add the DATE record on the tail of every file in csv_all directory
#########################################################################################

import json
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from MACRO import DATE, sort_country, LAST_DATE
from spider import sum_by_country, save_data
import requests
from bs4 import BeautifulSoup
import pandas as pd
# import pymysql
# from functools import reduce


# this function can get save data from local raw data
def save_data_from_raw(the_date):
    f = open('raw/'+the_date+'.csv')
    list_data = f.readlines()
    list_data.pop(0)
    rawData = list()
    for item in list_data:
        str = item.replace(', ','  ')
        str = str.replace('\"','')
        temp = str.split(',')
        rawData.append([temp[3].replace('  ',', '), temp[4], temp[7], temp[8], temp[9]])
    data = sum_by_country(rawData)
    save_data(data, 'list_data/' + DATE + '.txt')


# save_data_from_raw(DATE)  #save list data from local raw data
# sys.exit(50)


PATH = 'csv_all/'
# DATE = '04-15-2020'
LIST_DATA = 'list_data/' + DATE + '.txt'
X = ['4.15', '4.16', '4.17', '4.18', '4.19', '4.20', '4.21']
# SORTED_COUNTRY = sort_country('list_data/' + DATE + '.txt')


def add_record():
    f = open(LIST_DATA)
    list_data = json.loads(f.read())
    for item in list_data:
        print(item)
        file_name = PATH + item[0] + '.csv'
        file_name = file_name.replace('*', '')
        try:
            f = open(file_name)
        except FileNotFoundError:
            f = open(file_name, 'w')
            f.write('date,confirmed,cured,dead\n'
                    + DATE + ',' + str(item[1]) + ',' + str(item[2]) + ',' + str(item[3]))
            f.close()
            continue
        content = f.read()
        if DATE in content:  # cannot add duplicated data
            print(DATE+" data has exited!")
            return False
        f.close()
        f = open(file_name, 'w')
        f.write(content + '\n' + DATE + ',' + str(item[1]) + ',' + str(item[2]) + ',' + str(item[3]))
        f.close()


def delete_last_record():
    f = open(LIST_DATA)
    list_data = json.loads(f.read())
    for item in list_data:
        file_name = PATH + item[0] + '.csv'
        file_name = file_name.replace('*', '')

        file_old = open(file_name, 'r')
        lines = [i for i in file_old]
        del lines[-1]  # delete the last line
        lines[-1] = lines[-1].replace('\n', '')  # delete the '\n'
        file_old.close()

        file_new = open(file_name, 'w', )
        file_new.write(''.join(lines))
        file_new.close()


def draw_all(file):
    data = json.loads(open(file).read())
    print(data)
    for k, v in data.items():
        print(k, v)
        plt.plot(X, v, color='red')
        plt.text(X[6], v[6], k)
    plt.title('all country confirmed')
    # plt.savefig(save_path + country[i] + '.png')
    plt.show()


# this function sum all confirmed, cured and dead of the world
# in according to all_result.txt
def get_sum(file):
    all_confirmed = 0
    all_cured = 0
    all_dead = 0
    data = json.loads(open(file).read())
    for item in data:
        all_confirmed += int(item[1])
        all_cured += int(item[2])
        all_dead += int(item[3])
    return [all_confirmed, all_cured, all_dead]


# given the last date, get a series of date with a period of span
def get_date_ser():
    date_list = list()
    for i in range(14):
        date_list.append((LAST_DATE + timedelta(days=i - 6)).strftime('%m-%d-%Y'))
    return date_list


############################################################################################################
# this function construct a json data
# the sort_data is a list, each item is a list too
# the item in the list includes country name, confirmed, cured and dead data
############################################################################################################
def make_json():
    sort_data = sort_country('list_data/' + DATE + '.txt')
    # total = get_sum('list_data/' + DATE + '.txt')
    data = dict()
    data["Period"] = get_date_ser()
    data["data"] = {}

    # day_data = json.loads(open('list_data/'+MACRO.DATE+'.txt').read())
    for item in sort_data:
        data["data"][item[0].replace('*', '')] = {
            "Confirmed": [],
            "PreConfirmed": [],
            "Cured": [],
            "Dead": []
        }

    for date in data["Period"]:
        file = 'list_data/' + date + '.txt'
        day_data = json.loads(open(file).read().replace('*', ''))
        for c in day_data:
            try:
                data["data"][c[0]]["Confirmed"].append(c[1])
                data["data"][c[0]]["Cured"].append(c[2])
                data["data"][c[0]]["Dead"].append(c[3])
            except:
                print(c)
                print(date)
                sys.exit(2)
        if date == DATE:  # the last file has been handled, need to break
            break
    return data


def progress_bar(p, t):
    print('>' * p + '\n' + '*' * (t - p))


def make_map_data(end=250):
    file = 'list_data/' + DATE + '.txt'
    day_data = json.loads(open(file).read().replace('*', ''))
    data = ''
    length = len(day_data)
    i = 0
    for c in day_data:
        if i == end - 1 or i == length - 1:
            data += '{' + 'name:' + "\'" + c[0].replace("\'", "\\\'") + "\'" + ', value: [' + str(
                c[2]) + "," + str(c[3]) + "," + str(c[1]) + "], label: {normal: {show: true,formatter: function (" \
                                                            "params) {return params.name}}}}" + "\n "
            break
        data += '{' + 'name:' + "\'" + c[0].replace("\'", "\\\'") + "\'" + ', value: [' + str(
            c[2]) + "," + str(c[3]) + "," + str(c[1]) + "], label: {normal: {show: true,formatter: function (" \
                                                        "params) {return params.name}}}}," + "\n "
        i += 1
    data = "window.map_data=[" + "\n" + data + "]"
    f = open('data/map.js', 'w')
    f.write(data)
    f.close()
    print("map_data file has been saved to data directory!")


def make_top10_data():
    # ####    get the DATE data
    file = 'list_data/' + DATE + '.txt'
    day_data = json.loads(open(file).read().replace('*', ''))

    # ####    get the day before DATE data
    before = (LAST_DATE + timedelta(days=-1)).strftime('%m-%d-%Y')
    list_before = json.loads(open('list_data/' + before + '.txt').read().replace('*', ''))

    # ####    spider the newest data from worldometers  #######################
    cdc = data_of_cdc()

    # ####    construct the top10 dict
    top10 = dict()
    top10["Date"] = cdc["updated"]
    top10["TotalConfirmed"] = cdc["Coronavirus Cases:"]
    top10["TotalCured"] = cdc["Recovered:"]
    top10["TotalDead"] = cdc["Deaths:"]

    top10["confirmed"] = dict()
    top10["confirmed"]["country"] = list()
    top10["confirmed"]["data"] = list()
    top10["increase"] = dict()
    top10["increase"]["country"] = list()
    top10["increase"]["data"] = list()

    # ####    get health index of a country which is the ratio of recovered/confirmed
    hope = health_index(day_data)  # top10 hope index country
    sort_list = sorted(day_data, key=lambda i: i[1], reverse=True)[:10]
    top10["hope"] = dict()
    top10["hope"]["country"] = hope["country"]
    top10["hope"]["data"] = hope["data"]

    # ####  make top10 confirmed country  ######################################
    for item in sort_list:
        top10["confirmed"]["country"].append(item[0])
        top10["confirmed"]["data"].append(item[1])

    # ####  make top10 death country  #################
    top10["deaths"] = dict()
    top10["deaths"]["country"] = list()
    top10["deaths"]["data"] = list()
    death_list = sorted(day_data, key=lambda i: i[3], reverse=True)[:10]
    for item in death_list:
        top10["deaths"]["country"].append(item[0])
        top10["deaths"]["data"].append(item[3])

    # ####  make top10 increase confirmed country  ####
    increase = list()
    for item in day_data:
        for c in list_before:
            if item[0] == c[0]:
                increase.append([item[0], item[1] - c[1]])
    top10_increase = sorted(increase, key=lambda i: i[1], reverse=True)[:10]
    for item in top10_increase:
        top10["increase"]["country"].append(item[0])
        top10["increase"]["data"].append(item[1])

    # ####    make top10 hope index per day, which is the ratio of new recovered/new cases
    top10["hope_day"] = dict()
    top10["hope_day"]["country"] = list()
    top10["hope_day"]["data"] = list()
    hope_day = hope_index_today(day_data, list_before)
    for item in hope_day:
        top10["hope_day"]["country"].append(item[0])
        top10["hope_day"]["data"].append(item[1])

    # ####    make new cases    #######################################
    today_cases = 0
    for item in day_data:
        today_cases += item[1]

    yesterday_cases = 0
    for item in list_before:
        yesterday_cases += item[1]
    new_cases = today_cases - yesterday_cases
    top10["new_cases"] = new_cases
    # #################################################################

    # ####    make new cured    #######################################
    today_recovered = 0
    for item in day_data:
        today_recovered += item[2]

    yesterday_recovered = 0
    for item in list_before:
        yesterday_recovered += item[2]
    new_recovered = today_recovered - yesterday_recovered
    top10["new_recovered"] = new_recovered
    # #################################################################

    # ####    make new deaths    ######################################
    today_deaths = 0
    for item in day_data:
        today_deaths += item[3]

    yesterday_deaths = 0
    for item in list_before:
        yesterday_deaths += item[3]
    new_deaths = today_deaths - yesterday_deaths
    top10["new_deaths"] = new_deaths
    # ##################################################################

    # ####    calculate the world health index    ######################
    top10["health_index"] = round(100*today_recovered/today_cases)

    # ####    calculate the world hope index    ########################
    top10["hope_index"] = round(new_recovered/new_cases, 1)

    # ####    calculate top10 death rate    ############################
    top10["death_rate"] = dict()
    top10["death_rate"]["country"] = list()
    top10["death_rate"]["data"] = list()
    for item in death_rate(day_data):
        top10["death_rate"]["country"].append(item[0])
        top10["death_rate"]["data"].append(item[1])

    # ####    calculate the infection rate top 10    #################
    top10["infection_rate"] = dict()
    top10["infection_rate"]["country"] = list()
    top10["infection_rate"]["data"] = list()
    for item in infection_rate(day_data):
        top10["infection_rate"]["country"].append(item[0])
        top10["infection_rate"]["data"].append(item[1])

    # ####    calculate the death trend for top30 country    ##########
    # top10["death_trend"] = dict()
    # death_trend = trend_per_day(3)  # 3 means death data
    # top10["death_trend"]["period"] = death_trend["period"]
    # top10["death_trend"]["country"] = death_trend["country"]
    # top10["death_trend"]["data"] = death_trend["data"]

    # ####    calculate the world trend for new cases, new recovered and new deaths
    top10["world_trend"] = world_day_trend()

    # ###############save the top10 js file here ######################
    f = open('data/top10.js', 'w')
    f.write('window.top10=' + json.dumps(top10))
    f.close()
    print("top10_data file has been saved to data directory!")
    # #################################################################


# spider the cdc newest data
def data_of_cdc():
    url = "https://www.worldometers.info/coronavirus/"
    for i in range(3):
        print("get the url for %d time..." % (i+1))
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            total = dict()
            all_div = soup.find_all("div")
            for div in all_div:
                if "Last updated" in div.text:
                    total["updated"] = div.text[14:]

            div_list = soup.find_all('div', {"id": "maincounter-wrap"})
            for div in div_list:
                total[div.find("h1").text] = div.find("span").text
            # print(total)
            return total
    print("can not get the url:", url)
    sys.exit(101)



# ####    calculate the health index    ##############################
# ####    this function return a dict which key:value are
# ####    "country": ["China", "Singapore", ... ]
# ####    "data": [93, 90, ... ]
# ####    which means (total recovered/total confirmed) ratio
def health_index(data):
    hope = list()
    for item in data:
        if item[1] < 1000:
            continue
        hope.append([item[0], round(item[2] / item[1], 2)])
    sorted_hope = sorted(hope, key=lambda i: i[1], reverse=True)[:10]
    hope_dict = dict()
    hope_dict["country"] = list()
    hope_dict["data"] = list()
    for item in sorted_hope:
        hope_dict["country"].append(item[0])
        hope_dict["data"].append((item[1]))
    return hope_dict


# ####    this function to show (new recovered/new cases) ratio
# ####    the parameter "today" is a list like [["US", 930000, 30000, 56000], ["Spain", 220000, 50000,20000], ...]
# ####    which means country, confirmed, recovered and death
# ####    the parameter "yesterday" is list also, just like "today", but it's the data of day before "today"
def hope_index_today(today, yesterday):
    # get new cases
    day_new = list()
    for t in today:
        for y in yesterday:
            if t[0] == y[0] and t[1] > 1000:  # same country
                day_new.append([t[0], t[1] - y[1], t[2] - y[2], t[3] - y[3]])
    r_2_c = list()
    for item in day_new:
        if item[1] > 0:
            r_2_c.append([item[0], round(item[2] / item[1], 1)])

    return sorted(r_2_c, key=lambda d: d[1], reverse=True)[:10]


def death_rate(today):
    data = filter(lambda x: x[1] > 1000, today)
    d_rate = map(lambda x: (x[0], round(x[3]/x[1], 3)), data)
    d_rate = sorted(d_rate, key=lambda d: d[1], reverse=True)[:10]
    return d_rate


# ####    calculate the infection rate    ###################################
# ####    the parameter 'today' is a list like [[country_name, confirmed, recovered, death], ...]
# ####    return a list of top10 infection rate, whose range is 0 - 1000
def infection_rate(today):
    # ####    get the population data
    file = 'population/population.csv'
    data = pd.read_csv(file, index_col=0)
    population = data.values.tolist()  # population list including [country_name, population, continent] ...
    infection = list()
    for item in today:
        for p in population:
            if item[0] == p[0] and item[1] > 1000:
                infection.append([item[0], round(1000*item[1]/p[1], 1)])
    return sorted(infection, key=lambda d: d[1], reverse=True)[:10]


# ####    calculate the day data, which is like [[country_name, new cases, new recovered, new deaths], ...]
# ####    the_date is datetime type    ####################################################################
def day_data(the_date):
    today = json.loads(open('list_data/' + the_date.strftime('%m-%d-%Y') + '.txt').read().replace('*', ''))
    the_before_day = the_date + timedelta(days=-1)
    yesterday = json.loads(open('list_data/' + the_before_day.strftime('%m-%d-%Y') + '.txt').read().replace('*', ''))
    day_data = list()
    for t in today:
        for y in yesterday:
            if t[0] == y[0]:  # the same country
                day_data.append([t[0], t[1]-y[1], t[2]-y[2], t[3]-y[3]])
    return day_data


# ####    calculate every country's day data    ######################################
# ####    return a list, which is a dict   ###########################################
# ####    the parameter type could be 1, 2 or 3, means confirmed, recovered or deaths
def trend_per_day():
    period = 21
    data = dict()
    data["period"] = list()
    data["country"] = list()
    data["new_cases"] = list()
    data["new_recovered"] = list()
    data["new_death"] = list()
    the_date = LAST_DATE

    for i in range(period):
        cases = list()
        recovered = list()
        deaths = list()
        today = day_data(the_date)
        if i == 0:
            data["period"].append(the_date.strftime('%m-%d-%Y'))
            for item in today:
                data["country"].append(item[0])
                cases.append(item[1])
                recovered.append(item[2])
                deaths.append(item[3])
            data["new_cases"].append(cases)
            data["new_recovered"].append(recovered)
            data["new_death"].append(deaths)
        else:
            data["period"].insert(0, the_date.strftime('%m-%d-%Y'))
            for j in range(len(data["country"])):
                for item in today:
                    if data["country"][j] == item[0]:
                        data["new_cases"][j].insert(0, item[1])
                        recovered.insert(0, item[2])
                        deaths.insert(0, item[3])

        the_date = the_date + timedelta(days=-1)
    return data


# ####    calculate world new cases, recovered and deaths    ###############
# ####    the_date is a datetime type parameter    #########################
def world_day(the_date):
    data = day_data(the_date)
    cases = 0
    recovered = 0
    deaths = 0
    for item in data:
        cases += item[1]
        recovered += item[2]
        deaths += item[3]
    return [cases, recovered, deaths]


def world_day_trend():
    period = 21
    world = dict()
    world["period"] = list()
    world["cases"] = list()
    world["recovered"] = list()
    world["deaths"] = list()

    for i in range(period):
        the_date = LAST_DATE + timedelta(days=-period + 1+i)
        data = world_day(the_date)
        # if data[0] < 0 or data[1] < 0 or data[2] < 0:  # wrong data, dropped
        #     print(data)
            # continue
        world["period"].append(the_date.strftime('%m.%d'))
        world["cases"].append(data[0])
        world["recovered"].append(data[1])
        world["deaths"].append(data[2])

    return world


#  the_date is like 03-15-2020
def update_record(the_date):
    f = open('list_data/' + the_date + '.txt')
    # f = open(LIST_DATA)
    list_data = json.loads(f.read())
    for item in list_data:
        print(item)
        file_name = PATH + item[0] + '.csv'
        file_name = file_name.replace('*', '')
        try:
            f = open(file_name)
        except FileNotFoundError:
            f = open(file_name, 'w')
            f.write('date,confirmed,cured,dead\n'
                    + DATE + ',' + str(item[1]) + ',' + str(item[2]) + ',' + str(item[3]))
            f.close()
            continue
        content = f.read().split('\n')
        f.close()
        f = open(file_name, 'w')
        new_content = ''
        for day_data in content:
            if day_data.split(',')[0] == the_date:
                new_content += '\n' + the_date+ ',' + str(item[1]) + ',' + str(item[2]) + ',' + str(item[3])
            else:
                new_content += '\n' + day_data
        f.write(new_content)
        f.close()


if __name__ == "__main__":
    # world_day_trend()
    # sys.exit(11)
    # delete_last_record()
    # sys.exit(100)
    # update_record('08-03-2020')
    # sys.exit(111)

    # step 1
    print("step1...")
    save_data_from_raw(DATE)  #save list data from local raw data, saved as a list file
    # sys.exit(101)

    # step 2
    print("step2...")
    add_record()  # add the DATE data to the csv files end
    # sys.exit(102)

    # step 3
    print("step3...")
    make_map_data()  # make the map data

    # step 4
    print("step4...")
    # get realtime data from "https://www.worldometers.info/coronavirus/"
    make_top10_data()  # make the top10 js data in data directory

    sys.exit(0)
