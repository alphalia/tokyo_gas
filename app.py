from flask import Flask, render_template ,request, session, redirect, url_for
import os
import pandas as pd
app = Flask(__name__)

@app.route("/")
def index():
    peak_time = ["2000/03/10","2000/03/11","2000/03/12","2000/03/13","2000/03/14"]
    value_list = [1,2,3,4,5]
    all_day = sum(value_list)
    mean_value = sum(value_list)/len(value_list)
    max_value = max(value_list)
    min_value = min(value_list)
    peak_time = ["2000/03/13","2000/03/14"]
    return render_template("index.html",peak_time=peak_time,value_list=value_list,all_day=all_day,mean_value=mean_value,max_value=max_value,min_value=min_value)