################################################################################################
# after we prepared every data, every day, we can try to train them now.
# we design a global deep learning model and train it by all data.
# I reshape 7 day data in one array, and use it to predict the 8'th data.
# only last 30 day's data is used, because we believe that the recent data is more important.
# when tomorrow data is predicted, then we can predict the 9'th data, and so on.
# in this way, we can get 7 day's data in future.
# in fact, we can predict every day in future. but we don't think it's necessary.
################################################################################################

import pandas as pd
import torch
from torch import nn
import torch.nn.functional as F
import sys
import numpy as np
import matplotlib.pyplot as plt
import json
from MACRO import X1, DATE, sort_country, get_top10, get_country
from util import make_json, progress_bar

DIRECTORY = 'csv_files/'
SCALE = 1000000
SORTED_COUNTRY = sort_country('list_data/'+DATE+'.txt')
TOP10 = get_top10(SORTED_COUNTRY)
COUNTRY = get_country(SORTED_COUNTRY)


def get_train_data(data):
    local_train_x = np.zeros((23, 21), dtype=np.float32)
    local_train_y = np.zeros((23, 3), dtype=np.float32)
    for i in range(23):
        for j in range(7):
            local_train_x[i][j * 3] = data[i + j][0]
            local_train_x[i][j * 3 + 1] = data[i + j][1]
            local_train_x[i][j * 3 + 2] = data[i + j][2]
        local_train_y[i][0] = data[i + 7][0]
        local_train_y[i][1] = data[i + 7][1]
        local_train_y[i][2] = data[i + 7][2]
    return local_train_x, local_train_y


loss_func = F.mse_loss


class CoLogistic(nn.Module):
    def __init__(self):
        super().__init__()
        self.lin1 = nn.Linear(21, 128)
        self.lin2 = nn.Linear(128, 2048)
        self.lin3 = nn.Linear(2048, 4096)
        self.lin4 = nn.Linear(4096, 1024)
        self.lin5 = nn.Linear(1024, 3)

    def forward(self, xb):
        xb = self.lin1(xb)
        xb = self.lin2(xb)
        xb = self.lin3(xb)
        xb = self.lin4(xb)
        return self.lin5(xb)


n = 23
bs = 4
lr = 0.01  # learning rate
epochs = 50  # how many epochs to train for
# model = CoLogistic()


def fit(train_x, train_y):
    model = CoLogistic()

    for epoch in range(epochs):
        pred = loss = 0
        for i in range((n - 1) // bs + 1):
            start_i = i * bs
            end_i = start_i + bs
            xb = train_x[start_i:end_i]
            yb = train_y[start_i:end_i]
            pred = model(xb)
            loss = loss_func(pred, yb)
            # if i == 22:
            #     print(epoch, pred * SCALE, loss)
            loss.backward()
            with torch.no_grad():
                for p in model.parameters():
                    p -= p.grad * lr
                model.zero_grad()
        print(epoch, pred * SCALE, loss)
    return model


def update_xb(x, pred):
    t = x.clone()
    x[0:17] = t[3:20]
    x[18:20] = pred[0:2]
    return x


# predict 14 day with the past 7 days
def pre_week(country):
    global SCALE
    # get data from csv file
    data = pd.read_csv(country, index_col=0)
    my_list = data.values.tolist()[-30:]
    SCALE = my_list[-1][0]
    while len(my_list) < 30:
        my_list.insert(0, [0, 0, 0])
    train_x, train_y = get_train_data(my_list)
    train_x, train_y = map(
        torch.tensor, (train_x, train_y)
    )
    train_x /= SCALE
    train_y /= SCALE

    # train
    model = fit(train_x, train_y)

    # predict 2 weeks with past 7 days
    pre_confirmed = np.zeros(14)
    pre_cured = np.zeros(14)
    pre_dead = np.zeros(14)
    xb = train_x[15]
    for i in range(14):
        p = model(xb)
        pre_confirmed[i] = p.detach().numpy()[0] * SCALE
        pre_cured[i] = p.detach().numpy()[1] * SCALE
        pre_dead[i] = p.detach().numpy()[2] * SCALE
        xb = update_xb(xb, p)

    return pre_confirmed, pre_cured, pre_dead


# draw the last 7 days figure
def last_7_day(country):
    # file = csv_path + item + '.csv'
    data = pd.read_csv('csv_all/'+country+'.csv', index_col=0)
    my_list = data.values.tolist()[-7:]
    confirmed = list()
    for i in range(7):
        confirmed.append(my_list[i][0])
    return confirmed


def run_new(country, csv_path, save_path, save_result):
    # ############ get country list and save as js file###############
    f = open('data/country.js', 'w')
    f.write('window.country='+json.dumps(country))
    f.close()
    # ################################################################

    js_data = make_json()
    preConfirmed = list()
    global SCALE
    step = 0
    distance = len(country)
    # get predict data
    for item in country:
        file = csv_path + item + '.csv'
        preConfirmed.append(pre_week(file)[0].astype(int))
        js_data["data"][item]["PreConfirmed"] = preConfirmed[-1].tolist()
        progress_bar(step, distance)
        step += 1

    # ####### save the js_data as a js file#######
    f = open('data/data.js', 'w')
    f.write('window.data='+json.dumps(js_data))
    f.close()
    # ############################################

    result = {}
    for a, b in zip(country, preConfirmed):
        result[a] = b.tolist()
        print(a, b)

    # ########  here to save the prediction data  ##########
    f = open(save_result, 'w')
    f.write(json.dumps(result))
    f.close()
    # ######################################################

    # ####  here to draw the figure  ##########################################
    # country_num = len(country)
    # for i in range(country_num):
    #     confirmed = last_7_day(country[i])
    #     plt.plot(X1[:7], confirmed, color='green')
    #     for a, b in zip(X1, confirmed):
    #         plt.text(a, b, '%d' % b, ha='center', va='bottom', fontsize=10)
    #     plt.plot(X1, preConfirmed[i], color='red')
    #     for a, b in zip(X1, preConfirmed[i]):
    #         plt.text(a, b, '%d' % b, ha='center', va='bottom', fontsize=10)
    #     plt.title(country[i])
    #     plt.savefig(save_path + country[i] + '.png')
    #     plt.show()  # show figure one by one
    # ##########################################################################


if __name__ == "__main__":
    # train just one country
    # run_new(['US'], 'csv_all/', 'top10/', 'one_country.txt')

    # get top10 country prediction, for now, it's 8.
    # run_new(TOP10, 'csv_all/', 'top10/', 'top10_result.txt')

    # save model
    # model = CoLogistic()
    # torch.save(model, 'model.pth')
    # print(list(model.modules())[0])
    # sys.exit(101)

    # get all country prediction
    run_new(COUNTRY, 'csv_all/', 'figures/', 'all_result.txt')

    # torch.save(model, 'model/model.pth')
    print(TOP10)

    sys.exit(0)
