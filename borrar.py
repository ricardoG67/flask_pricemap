'''import numpy as np

def comparador_min(lista_prices):
    #1: WONG, 2: METRO, 3: PLAZA VEA, 4: TOTTUS Y 5: VIVANDA
    minimo = np.min(lista_prices)
    if lista_prices[0] == minimo:
        return "wong", minimo
    if lista_prices[1] == minimo:
        return "metro", minimo
    if lista_prices[2] == minimo:
        return "plaza_vea", minimo
    if lista_prices[3] == minimo:
        return "tottus", minimo
    if lista_prices[4] == minimo:
        return "vivanda", minimo

def comparador_max(lista_prices):
    #1: WONG, 2: METRO, 3: PLAZA VEA, 4: TOTTUS Y 5: VIVANDA
    maximo = np.max(lista_prices)
    if lista_prices[0] == maximo:
        return "wong", maximo
    if lista_prices[1] == maximo:
        return "metro", maximo
    if lista_prices[2] == maximo:
        return "plaza_vea", maximo
    if lista_prices[3] == maximo:
        return "tottus", maximo
    if lista_prices[4] == maximo:
        return "vivanda", maximo

def variacion(lista_prices):
    #1: WONG, 2: METRO, 3: PLAZA VEA, 4: TOTTUS Y 5: VIVANDA
    lista_variaciones = []
    for i in lista_prices:
        if len(i) == 0:
            variacion = None
            lista_variaciones.append(variacion)
        else:
            fin = i[-1]
            inicio = i[0]
            variacion = ((fin-inicio)/inicio)*100
            variacion = np.round(np.mean(variacion),1)
            lista_variaciones.append(variacion)

    return lista_variaciones

price = np.array([[2.6, 2.6], [1.3, 1.5], [4, 5], ['nan','nan'], [9,8]])

mins=[]
maxs=[]

for i in price:
    if len(i)!=0:
        mins.append(np.min(i))
        maxs.append(np.max(i))
    else:
        mins.append(99999)
        maxs.append(0)

print(variacion(price))
'''
'''
import pandas as pd
import numpy as np
retail_data = pd.read_csv("retail_data_final.csv")

description = retail_data['description'].to_numpy()
inca = []
for i in description:
    if ("inca kola" in i) and "500ml" in i:
        inca.append(i)

print((inca))'''
'''
from flask import Flask, render_template
import plotly.graph_objects as go
import json
import plotly
import plotly.io as pio
import chart_studio.plotly as py
import numpy as np
import datetime
from pytz import timezone

def create_fig(retailers, skus, title, price_evolution_data, time):   
    ## create traces
    fig = go.Figure()

    #NUEVO
    est = timezone('EST')
    now = datetime.datetime.now(est) - datetime.timedelta(days=int(time))
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    current_date = '{}-{}-{}'.format(year, month, day)
    #####

    #Save prices
    prices = []
    ## navigate for each retail and sku
    for retail, sku in zip(retailers, skus):
        ## select the sku and retail
        query = price_evolution_data.loc[(price_evolution_data['sku'] == sku) & (price_evolution_data['retail'] == retail)]
        query = query.loc[query["date"]>=current_date]

        price = query["price"] ## get the price
        date = query["date"] ## get the date
        
        fig.add_trace(go.Scatter(x=date.values,
                                 y=price.values,                                
                                 name=retail))

        prices.append(price.values)
        #[prices.append(i) for i in price.values]

    fig.update_traces(mode='lines+markers')
    fig.update_layout(title={
                            'text': title,
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    
    return fig, prices'''

'''retailers = ["wong", "metro", "plaza_vea", "tottus", "vivanda"]
skus = ["59539001", "59539001", "497497", "10174358", "497497"]
title = 'INKA COLA 500ML'
import pandas as pd
price_evolution_data = pd.read_csv("price_evolution.csv")
time = "7"
fig, price = create_fig(retailers, skus, title, price_evolution_data, time)
fig.show(renderer="iframe")'''


'''est = timezone('EST')
now = datetime.datetime.now(est) - datetime.timedelta(days=7)
year = '{:02d}'.format(now.year)
month = '{:02d}'.format(now.month)
day = '{:02d}'.format(now.day)
current_date = '{}-{}-{}'.format(year, month, day)
print(current_date)
seven_days = price_evolution_data.loc[price_evolution_data["date"]>=current_date]
print(seven_days)'''

'''import numpy as np

price = np.array([[2.6, 2.6], [1.3, 1.5], [4, 5], [3,2], [9,8]])

print(np.mean(price))

media = []
for i in price:
    media.append(np.average(i))

print(np.average(media))
import datetime
from pytz import timezone
import pandas as pd
import plotly.graph_objects as go

price_evolution_data = pd.read_csv("retail_data_final.csv")

if "INCA KOLA" in price_evolution_data["description"]:
    print(price_evolution_data["description"])
    print("gaaaa")

def create_fig(retailers, skus, title, price_evolution_data, time):   
    ## create traces
    fig = go.Figure()

    #NUEVO
    est = timezone('EST')
    now = datetime.datetime.now(est) - datetime.timedelta(days=int(time))
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    current_date = '{}-{}-{}'.format(year, month, day)
    #####

    #Save prices
    prices = []
    ## navigate for each retail and sku
    for retail, sku in zip(retailers, skus):
        ## select the sku and retail
        query = price_evolution_data.loc[(price_evolution_data['sku'] == sku) & (price_evolution_data['retail'] == retail)]
        query = query.loc[query["date"]>=current_date]

        price = query["price"] ## get the price
        date = query["date"] ## get the date
        
        fig.add_trace(go.Scatter(x=date.values,
                                 y=price.values,                                
                                 name=retail))

        prices.append(price.values)
        #[prices.append(i) for i in price.values]

    fig.update_traces(mode='lines+markers')
    fig.update_layout(title={
                            'text': title,
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    
    return fig, prices

'''

tupla = (("wong",2), ("xd",5), ("plaza_Vea",5))

[print(i.capitalize().replace("_"," ")) for i,j in tupla]