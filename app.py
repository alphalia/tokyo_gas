from flask import Flask, render_template ,request, session, redirect, url_for
import os
import pandas as pd
app = Flask(__name__)

def split_list(l, n):
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]

def my_round(val, digit=0):
    p = 10 ** digit
    return (val * p * 2 + 1) // 2 / p

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
    mean_dict[i] = my_round(sum(list(df[i])) / len(list(df[i])),1)
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
day_grow_dict = {}
grow_list_dict = {}
time_txt_ = ["00:00~04:00","05:00~09:00","10:00~14:00","15:00~19:00","20:00~23:00",]
for i in day_list:
    upper_75 = int(df[i].describe()[6])
    lower_25 = int(df[i].describe()[4])
    count = 0
    day_grow_dict[i] = {}
    grow_list_dict[i] = []
    for k in list(split_list(value_dict[i], 5)):
        mean_ = sum(k) / len(k)
        if mean_ <= lower_25:
            day_grow_dict[i][time_txt_[count]] = "./static/images/tree1.png"
            grow_list_dict[i].append("./static/images/tree3.png")
        elif mean_ >= upper_75:
            day_grow_dict[i][time_txt_[count]] = "./static/images/tree3.png"
            grow_list_dict[i].append("./static/images/tree1.png")
        else:
            day_grow_dict[i][time_txt_[count]] = "./static/images/tree2.png"
            grow_list_dict[i].append("./static/images/tree2.png")
    peak_dict[i] = []
    for k in graph_dict[i]:
        if not type(k[1]) == int:
            continue
        else:
            if k[1] >= upper_75:
                peak_dict[i].append(k[0])

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route("/",methods=["POST","GET"])
def index():

    if("choose_day" in request.form):
        # 表示したい時間
        choose_day = request.form["choose_day"]
    else:
        choose_day = "day_1"

    value_list = value_dict[choose_day]
    all_day = all_dict[choose_day]
    mean_value = mean_dict[choose_day]
    max_value = max_dict[choose_day]
    min_value = min_dict[choose_day]
    peak_time = peak_dict[choose_day]
    data_list = day_list
    graph_list = graph_dict[choose_day]
    grow_dict  = day_grow_dict[choose_day]
    grow_list = grow_list_dict[choose_day]

    return render_template("index.html",data_list=data_list,\
                            peak_time=peak_time,value_list=value_list,\
                            all_day=all_day,mean_value=mean_value,\
                            max_value=max_value,min_value=min_value,\
                            graph_list=graph_list,choose_day=choose_day,grow_dict=grow_dict,\
                            time_txt_=time_txt_,grow_list=grow_list)