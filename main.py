import time
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

import pricemap

import plotly.graph_objects as go
import numpy as np
#import chart_studio
#import chart_studio.plotly as py

#from apscheduler.schedulers.blocking import BlockingScheduler

# sched = BlockingScheduler()
# @sched.scheduled_job('cron', minute='01', hour='8,16,23')
def update_prices():

    #Lee los archivos .csv
    price_evolution_data = pd.read_csv("/home/neurometricslab/flask_pricemap/price_evolution.csv")
    retail_data = pd.read_csv("/home/neurometricslab/flask_pricemap/retail_data_final.csv")

    #Se aplica get_price_retail de pricemap.py a los datos de retail_data (EL codigo demora)
    df = pd.DataFrame(columns=price_evolution_data.columns)
    df["sku"], df["price"],df["price_tienda"],df["price_tarjeta"], df["retail"], df["date"], df["time"]= zip(*retail_data.apply(lambda x: pricemap.get_price_retail(x["uri"], x["retail"], x["sku"]), axis=1))

    #Se guardan/actualizan en .csv los datos dentro de price_evolution_data
    price_evolution_data = pd.concat([price_evolution_data, df], axis=0, ignore_index=True)
    price_evolution_data.to_csv("/home/neurometricslab/flask_pricemap/price_evolution.csv", index=False)

    ##Guarda en variable solo los datos de la ultima semana (GRAFICO EN 1 SEMANA)
    seven_days_ago = pricemap.get_time(today=False)
    price_evolution_data = price_evolution_data.loc[price_evolution_data['date'] >= seven_days_ago[0]]

    #Se limpia los datos y se pasan al formato indicado
    price_evolution_data["price_float"] = price_evolution_data["price"].apply(lambda x: float(str(x).replace(',','')) if(x is not None) else "None")
    price_evolution_data["date_time"] = price_evolution_data[["date", "time"]].apply(lambda row: " ".join(row.values), axis=1)

#sched.start()
update_prices()
