from flask import Flask, render_template ,request, session, redirect, url_for
import os
import pandas as pd
app = Flask(__name__)
app.secret_key = os.urandom(32)

def split_list(l, n):
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]

def my_round(val, digit=0):
    p = 10 ** digit
    return (val * p * 2 + 1) // 2 / p

df = pd.read_csv("data_csv_2.csv")
df_hatu = pd.read_csv("gen_0.csv")
# ラベル (時間)
data_list = list(df["time"])
# 日付一覧
day_list = list(df.columns)[2:]
day_list2 = [str(i) for i in range(len(list(df.columns)[2:]))]
# 日付:値
mean_dict = {}
max_dict = {}
min_dict = {}
all_dict = {}
value_dict = {}
hatu_dict = {}
for i in day_list:
    mean_dict[i] = my_round(sum(list(df[i])) / len(list(df[i])),1)
    max_dict[i] = max(list(df[i]))
    min_dict[i] = min(list(df[i]))
    all_dict[i] = sum(list(df[i]))
    value_dict[i] = list(df[i])
    hatu_dict[i] = list(df_hatu[i])

graph_dict = {}
for i in day_list:
    graph_dict[i] = [["時間","消費電力","発電量"]]
    count = 0
    for k in data_list:
        graph_dict[i].append([k,value_dict[i][count],hatu_dict[i][count]])
        count += 1

peak_dict = {}
day_grow_dict = {}
grow_list_dict = {}
time_txt_ = ["00:00~04:00","05:00~09:00","10:00~14:00","15:00~19:00","20:00~23:00",]
# for i in day_list:
#     upper_75 = int(df[i].describe()[6])
#     lower_25 = int(df[i].describe()[4])
#     count = 0
#     day_grow_dict[i] = {}
#     grow_list_dict[i] = []
#     for k in list(split_list(value_dict[i], 5)):
#         mean_ = sum(k) / len(k)
#         if mean_ <= lower_25:
#             day_grow_dict[i][time_txt_[count]] = "./static/images/tree1.png"
#             grow_list_dict[i].append("./static/images/tree3.png")
#         elif mean_ >= upper_75:
#             day_grow_dict[i][time_txt_[count]] = "./static/images/tree3.png"
#             grow_list_dict[i].append("./static/images/tree1.png")
#         else:
#             day_grow_dict[i][time_txt_[count]] = "./static/images/tree2.png"
#             grow_list_dict[i].append("./static/images/tree2.png")
#     peak_dict[i] = []
#     for k in graph_dict[i]:
#         if not type(k[1]) == int:
#             continue
#         else:
#             if k[1] >= upper_75:
#                 peak_dict[i].append(k[0])

grow_tree = {}
for i,j in zip(day_list, day_list2):
    upper_75 = int(df[i].describe()[6])
    lower_25 = int(df[i].describe()[4])
    count = 0
    day_grow_dict[i] = {}
    grow_list_dict[i] = []
    grow_tree[j] = {}
    for k in list(split_list(value_dict[i], 5)):
        mean_ = sum(k) / len(k)
        j = int(j)
        if mean_ <= lower_25:
            if (j == 0) and (count == 0):
                grow_tree[str(j)][time_txt_[count]] = 3
            elif count != 0:
                grow_tree[str(j)][time_txt_[count]] = grow_tree[str(j)][time_txt_[count - 1]] + 3
            elif count == 0:
                grow_tree[str(j)][time_txt_[count]] = grow_tree[str(j-1)][time_txt_[4]] + 3
        elif mean_ >= upper_75:
            if (j == 0) and (count == 0):
                grow_tree[str(j)][time_txt_[count]] = 1
            elif count != 0:
                grow_tree[str(j)][time_txt_[count]] = grow_tree[str(j)][time_txt_[count - 1]] + 1
            elif count == 0:
                grow_tree[str(j)][time_txt_[count]] = grow_tree[str(j-1)][time_txt_[4]] + 1
        else:
            if (j == 0) and (count == 0):
                grow_tree[str(j)][time_txt_[count]] = 2
            elif count != 0:
                grow_tree[str(j)][time_txt_[count]] = grow_tree[str(j)][time_txt_[count - 1]] + 2
            elif count == 0:
                grow_tree[str(j)][time_txt_[count]] = grow_tree[str(j-1)][time_txt_[4]] + 2
        j = str(j)
        if grow_tree[j][time_txt_[count]] % 10 <= 3:
            day_grow_dict[i][time_txt_[count]] = "./static/images/tree1.png"
            grow_list_dict[i].append("./static/images/tree1.png")
        elif grow_tree[j][time_txt_[count]] % 10 <= 7:
            day_grow_dict[i][time_txt_[count]] = "./static/images/tree2.png"
            grow_list_dict[i].append("./static/images/tree2.png")
        else:
            day_grow_dict[i][time_txt_[count]] = "./static/images/tree3.png"
            grow_list_dict[i].append("./static/images/tree3.png")
        count += 1
    peak_dict[i] = []
    for k in graph_dict[i]:
        if not type(k[1]) == int:
            continue
        else:
            if k[1] >= upper_75:
                peak_dict[i].append(k[0])

# ***********************************
# コミュニティ(関数化はあとでやる)
df_co = pd.read_csv("./data_box/data_comu.csv")
df_hatu_co = pd.read_csv("./data_box/data_gen_comu.csv")

data_list_co = list(df_co["time"])
# 日付一覧
day_list_co = list(df_co.columns)[2:]
day_list2_co = [str(i) for i in range(len(list(df_co.columns)[2:]))]
# 日付:値
mean_dict_co = {}
max_dict_co = {}
min_dict_co = {}
all_dict_co = {}
value_dict_co = {}
hatu_dict_co = {}
for i in day_list_co:
    mean_dict_co[i] = my_round(sum(list(df_co[i])) / len(list(df_co[i])),1)
    max_dict_co[i] = max(list(df_co[i]))
    min_dict_co[i] = min(list(df_co[i]))
    all_dict_co[i] = sum(list(df_co[i]))
    value_dict_co[i] = list(df_co[i])
    hatu_dict_co[i] = list(df_hatu_co[i])

graph_dict_co = {}
for i in day_list_co:
    graph_dict_co[i] = [["時間","消費電力","発電量"]]
    count = 0
    for k in data_list_co:
        graph_dict_co[i].append([k,value_dict_co[i][count],hatu_dict_co[i][count]])
        count += 1

peak_dict_co = {}
day_grow_dict_co = {}
grow_list_dict_co = {}
time_txt__co = ["00:00~04:00","05:00~09:00","10:00~14:00","15:00~19:00","20:00~23:00",]
grow_tree_co = {}
for i,j in zip(day_list_co, day_list2_co):
    upper_75 = int(df_co[i].describe()[6])
    lower_25 = int(df_co[i].describe()[4])
    count = 0
    day_grow_dict_co[i] = {}
    grow_list_dict_co[i] = []
    grow_tree_co[j] = {}
    for k in list(split_list(value_dict_co[i], 5)):
        mean_ = sum(k) / len(k)
        j = int(j)
        if mean_ <= lower_25:
            if (j == 0) and (count == 0):
                grow_tree_co[str(j)][time_txt__co[count]] = 3
            elif count != 0:
                grow_tree_co[str(j)][time_txt__co[count]] = grow_tree_co[str(j)][time_txt__co[count - 1]] + 3
            elif count == 0:
                grow_tree_co[str(j)][time_txt__co[count]] = grow_tree_co[str(j-1)][time_txt__co[4]] + 3
        elif mean_ >= upper_75:
            if (j == 0) and (count == 0):
                grow_tree_co[str(j)][time_txt__co[count]] = 1
            elif count != 0:
                grow_tree_co[str(j)][time_txt__co[count]] = grow_tree_co[str(j)][time_txt__co[count - 1]] + 1
            elif count == 0:
                grow_tree_co[str(j)][time_txt__co[count]] = grow_tree_co[str(j-1)][time_txt__co[4]] + 1
        else:
            if (j == 0) and (count == 0):
                grow_tree_co[str(j)][time_txt__co[count]] = 2
            elif count != 0:
                grow_tree_co[str(j)][time_txt__co[count]] = grow_tree_co[str(j)][time_txt__co[count - 1]] + 2
            elif count == 0:
                grow_tree_co[str(j)][time_txt__co[count]] = grow_tree_co[str(j-1)][time_txt__co[4]] + 2
        j = str(j)
        if grow_tree_co[j][time_txt__co[count]] % 10 <= 3:
            day_grow_dict_co[i][time_txt__co[count]] = "./static/images/tree1.png"
            grow_list_dict_co[i].append("./static/images/tree1.png")
        elif grow_tree_co[j][time_txt__co[count]] % 10 <= 7:
            day_grow_dict_co[i][time_txt__co[count]] = "./static/images/tree2.png"
            grow_list_dict_co[i].append("./static/images/tree2.png")
        else:
            day_grow_dict_co[i][time_txt__co[count]] = "./static/images/tree3.png"
            grow_list_dict_co[i].append("./static/images/tree3.png")
        count += 1
    peak_dict_co[i] = []
    for k in graph_dict_co[i]:
        if not type(k[1]) == int:
            continue
        else:
            if k[1] >= upper_75:
                peak_dict_co[i].append(k[0])

tree_count = 0
tree_count_co = 0
for i in grow_list_dict:
    tree_count_ = grow_list_dict[i].count("./static/images/tree3.png")
    tree_count += tree_count_
for i in grow_list_dict_co:
    tree_count_ = grow_list_dict_co[i].count("./static/images/tree3.png")
    tree_count_co += tree_count_
# ******************************************

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

    if("which" in request.form):
        which = int(request.form["which"])
        session["which"] = which
    else:
        if "which" not in session:
            which = 0
        else:
            which = session["which"]

    if("choose_day" in request.form):
        # 表示したい時間
        choose_day = request.form["choose_day"]
    else:
        choose_day = "day_1"

    if which == 0:
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
        tree_count_is = tree_count

    else:
        value_list = value_dict_co[choose_day]
        all_day = all_dict_co[choose_day]
        mean_value = mean_dict_co[choose_day]
        max_value = max_dict_co[choose_day]
        min_value = min_dict_co[choose_day]
        peak_time = peak_dict_co[choose_day]
        data_list = day_list_co
        graph_list = graph_dict_co[choose_day]
        grow_dict  = day_grow_dict_co[choose_day]
        grow_list = grow_list_dict_co[choose_day]
        tree_count_is = tree_count_co
    img_dict = {
            1:["./static/images/ama_asa_good.png","./static/images/ama_asa_normal.png","./static/images/ama_asa_bad.png"],
            2:["./static/images/ama_hiru_good.png","./static/images/ama_hiru_normal.png","./static/images/ama_hiru_bad.png"],
            3:["./static/images/ama_yuu_good.png","./static/images/ama_yuu_normal.png","./static/images/ama_yuu_bad.png"],
            4:["./static/images/ama_yoru_good.png","./static/images/ama_yoru_normal.png","./static/images/ama_yoru_bad.png"],
            0:["./static/images/ama_shin_good.png","./static/images/ama_shin_normal.png","./static/images/ama_shin_bad.png"],
            }
    img_dict_kara = {
            1:["./static/images/kara_asa_good.png","./static/images/kara_asa_normal.png","./static/images/kara_asa_bad.png"],
            2:["./static/images/kara_hiru_good.png","./static/images/kara_hiru_normal.png","./static/images/kara_hiru_bad.png"],
            3:["./static/images/kara_yuu_good.png","./static/images/kara_yuu_normal.png","./static/images/kara_yuu_bad.png"],
            4:["./static/images/kara_yoru_good.png","./static/images/kara_yoru_normal.png","./static/images/kara_yoru_bad.png"],
            0:["./static/images/kara_shin_good.png","./static/images/kara_shin_normal.png","./static/images/kara_shin_bad.png"],
            }

    
    if("amakara" in request.form):
        amakara = int(request.form["amakara"])
        session["amakara"] = amakara
    else:
        if "amakara" not in session:
            amakara = 0
        else:
            amakara = session["amakara"]
    if amakara == 0:
        comment_list = []
        count = 0
        for i in grow_list:
            if i == "./static/images/tree1.png":
                # 良い
                comment_list.append(img_dict[count][0])
            elif i == "./static/images/tree2.png":
                # 真ん中
                comment_list.append(img_dict[count][1])
            else:
                # 悪い
                comment_list.append(img_dict[count][2])
            count += 1
    else:
        comment_list = []
        count = 0
        for i in grow_list:
            if i == "./static/images/tree1.png":
                # 良い
                comment_list.append(img_dict_kara[count][0])
            elif i == "./static/images/tree2.png":
                # 真ん中
                comment_list.append(img_dict_kara[count][1])
            else:
                # 悪い
                comment_list.append(img_dict_kara[count][2])
            count += 1

    nokori = 30 - tree_count_is
    return render_template("index.html",data_list=data_list,\
                            peak_time=peak_time,value_list=value_list,\
                            all_day=all_day,mean_value=mean_value,\
                            max_value=max_value,min_value=min_value,\
                            graph_list=graph_list,choose_day=choose_day,grow_dict=grow_dict,\
                            time_txt_=time_txt_,grow_list=grow_list,comment_list=comment_list,\
                            tree_count_is=tree_count_is,nokori=nokori)