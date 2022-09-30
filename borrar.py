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
'''
tupla = (("wong",2), ("xd",5), ("plaza_Vea",5))

[print(i.capitalize().replace("_"," ")) for i,j in tupla]'''
'''import numpy as np
x = [np.nan, np.nan, 1, 2, 3, 4,5, np.nan, np.nan, 8,9,np.nan, 10]
d = [np.nan, 9, np.nan, 2, 2 ,2]
a=[]

x = np.array(x)
d = np.array(d)

a.append(x)
a.append(d)
a = np.array(a)

print("Asi empieza: ")
print(a, "\n\n")

sin_Nan = []
for i in a:
    i = np.where(np.isnan(i)==False, i,0)
    i = i[i!=0]
    sin_Nan.append(i)

print(sin_Nan)
'''
'''
ANTES DE CAMBIAR 
def variacion(lista_prices):
    cnx = mysql.connector.connect(host='neurometricslab.mysql.pythonanywhere-services.com', user='neurometricslab', password='pricemap', database='neurometricslab$default')

    #1: WONG, 2: METRO, 3: PLAZA VEA, 4: TOTTUS Y 5: VIVANDA

    sin_Nan = []
    for i in lista_prices:
        i = np.where(np.isnan(i)==False, i,0)
        i = i[i!=0]
        sin_Nan.append(i)

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
            if np.isnan(variacion):
                lista_variaciones.append(None)
            else:
                lista_variaciones.append(variacion)

    return lista_variaciones
'''
##################################
#################
#################
#################
#################
#################
#Esto se podria pasar nomas a flask y lo lee con jinja
'''cuadro_1 = np.load("cuadro_1.npy")

for fila in cuadro_1:
    descripcion = fila[0]
    promedio = fila[1]
    maximo = fila[2]
    minimo = fila[3]
    sensibilidad = fila[4]
    rango = fila[5]
    print(descripcion,promedio, maximo, minimo, sensibilidad, rango,"\n")'''

'''cuadro_1_1 = np.load("cuadro_1_1.npy", allow_pickle=True)

for fila in cuadro_1_1:
    descripcion = fila[0]
    estadisticos_1_1 = fila[1]
    
    wong = estadisticos_1_1[0]
    metro = estadisticos_1_1[1]
    pv = estadisticos_1_1[2]
    vivanda = estadisticos_1_1[3]
    tottus = estadisticos_1_1[4]'''

'''cuadro2= np.load("cuadro2.npy", allow_pickle=True)

for fila in cuadro2:
    descripcion = fila[0]

    estadisticos2 = fila[1]
    dia_prom = estadisticos2[0][0]
    dia_desv = estadisticos2[0][1]

    tarde_prom = estadisticos2[1][0]
    tarde_desv = estadisticos2[1][1]

    noche_prom = estadisticos2[2][0]
    noche_desv = estadisticos2[2][1]

    ganador = fila[2]'''

#HACER NUMPY ROUND############################3
'''=cuadro2_chiquito np.load("cuadro2_chiquito.npy", allow_pickle=True)
dia = cuadro2_chiquito[0]
tarde = cuadro2_chiquito[1]
noche = cuadro2_chiquito[2]
'''

'''cuadro2_3 = np.load("cuadro2_3.npy", allow_pickle=True)

for fila in cuadro2_3:
    descripcion = fila[0]

    minimo = fila[1]
    minimo_dia = minimo[0]
    minimo_tarde = minimo[1]
    minimo_noche = minimo[2]

    maximo = fila[2]
    maximo_dia = maximo[0]
    maximo_tarde = maximo[1]
    maximo_noche = maximo[2]
'''
'''cuadro3 = np.load("cuadro3.npy", allow_pickle=True)

for fila in cuadro3:
    descripcion = fila[0]

    supermercados = fila[1]
    wong = supermercados[0]

    metro = supermercados[1]

    pv = supermercados[2]

    vivanda = supermercados[3]

    tottus = supermercados[4]
    print(tottus)

    ganador = fila[2]
'''

'''cuadro4 = np.load("cuadro4.npy", allow_pickle=True)

for fila in cuadro4:
    descripcion = fila[0]

    supermercados = fila[1]
    metro = supermercados[0]
    pv = supermercados[1]
    tottus = supermercados[2]
    vivanda = supermercados[3]
    wong = supermercados[4]

    ganador = fila[2]'''

'''cuadro5 = np.load("cuadro5.npy", allow_pickle=True)

for fila in cuadro5:
    descripcion = fila[0]

    supermercados = fila[1]
    metro = supermercados[0]
    pv = supermercados[1]
    tottus = supermercados[2]
    vivanda = supermercados[3]
    wong = supermercados[4]

    ganador = fila[2]'''
