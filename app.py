from flask import Flask, render_template ,request, session, redirect, url_for
import os
import pandas as pd
app = Flask(__name__)

df = pd.read_csv("data_csv_2.csv")
# ラベル (時間)
data_list = list(df["time"])
# 日付一覧
day_list = list(df.columns)[2:]
# 日付:値
mean_dict = {}
max_dict = {}
min_dict = {}
all_dict = {}
value_dict = {}
for i in day_list:
    mean_dict[i] = sum(list(df[i])) / len(list(df[i]))
    max_dict[i] = max(list(df[i]))
    min_dict[i] = min(list(df[i]))
    all_dict[i] = sum(list(df[i]))
    value_dict[i] = list(df[i])

graph_dict = {}
for i in day_list:
    graph_dict[i] = [["時間","消費電力"]]
    count = 0
    for k in data_list:
        graph_dict[i].append([k,value_dict[i][count]])
        count += 1

peak_dict = {}
for i in day_list:
    upper_75 = int(df[i].describe()[6])
    peak_dict[i] = []
    for k in graph_dict[i]:
        if not type(k[1]) == int:
            continue
        else:
            if k[1] >= upper_75:
                peak_dict[i].append(k[0])


@app.route("/",methods=["POST","GET"])
def index():

    # 表示したい時間
    choose_day = request.form["choose_day"]
    # choose_day = "day_1"

    value_list = value_dict[choose_day]
    all_day = all_dict[choose_day]
    mean_value = mean_dict[choose_day]
    max_value = max_dict[choose_day]
    min_value = min_dict[choose_day]
    peak_time = peak_dict[choose_day]

    return render_template("index.html",data_list=data_list,\
                            peak_time=peak_time,value_list=value_list,\
                            all_day=all_day,mean_value=mean_value,\
                            max_value=max_value,min_value=min_value)