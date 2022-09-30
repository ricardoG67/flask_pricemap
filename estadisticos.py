import numpy as np
from pytz import timezone
import datetime
import plotly.graph_objects as go
import pandas as pd
import mysql.connector

cnx = mysql.connector.connect(host='localhost', user='root', password='', database='pricemap')

def estadisticos(price):
    maxs = []
    mins = []
    media = []
    #1: WONG, 2: METRO, 3: PLAZA VEA, 4: TOTTUS Y 5: VIVANDA
    for i in price:
        if len(i)!=0:
            mins.append(np.nanmin(i))
            maxs.append(np.nanmax(i))
            media.append(np.average(i))
        else:
            mins.append(99999)
            maxs.append(0)

    mins = comparador_min(mins)
    maxs = comparador_max(maxs)
    var = variacion(price)
    media = np.round(np.nanmean(media),1)
    return mins, maxs, var, media


def comparador_min(lista_prices):
    #1: WONG, 2: METRO, 3: PLAZA VEA, 4: TOTTUS Y 5: VIVANDA
    minimo = np.nanmin(lista_prices)
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
    maximo = np.nanmax(lista_prices)
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
            if np.isnan(variacion):
                lista_variaciones.append(None)
            else:
                lista_variaciones.append(variacion)

    return lista_variaciones

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
        
        fig.add_trace(go.Scatter(x=date.values, y=price.values, name=retail))

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

def productos():
    price_evolution_data = pd.read_csv("price_evolution.csv")
    retailers = ["wong", "metro", "plaza_vea", "tottus", "vivanda"]

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM productos')
    data = cursor.fetchall()

    for i in data:
        title = i[1]
        sku = []
        sku.append(i[2])
        sku.append(i[3])
        sku.append(i[4])
        sku.append(i[5])
        sku.append(i[6])

        sku = list(map(str, sku))

        dias = [7,14,30]

        if None not in sku:
            for dia in dias:

                fig, price = create_fig(retailers, sku, title, price_evolution_data, dia)
                # figura = py.plot(fig, auto_open=False) #Figura te da el url del embed
                name = title.replace(" ","") + "_" + str(dia)
                url = "/home/neurometricslab/flask_pricemap/static/img/figuras/" + name +".html"
                if dia == 7:
                    fig.write_html(url) 
                    mins, maxs, variacion, media = estadisticos(price)

                    cursor = cnx.cursor()
                    update = ("UPDATE productos SET minimo_7=%s, maximo_7=%s, variacion_7=%s, media_7=%s where descripcion=%s")
                    cursor.execute(update, (str(mins), str(maxs), str(variacion), str(media), title))
                    cnx.commit()

                elif dia == 14:
                    fig.write_html(url) 
                    mins, maxs, variacion, media = estadisticos(price)

                    cursor = cnx.cursor()
                    update = ("UPDATE productos SET minimo_14=%s, maximo_14=%s, variacion_14=%s, media_14=%s where descripcion=%s")
                    cursor.execute(update, (str(mins), str(maxs), str(variacion), str(media), title))
                    cnx.commit()
                elif dia == 30:
                    fig.write_html(url) 
                    mins, maxs, variacion, media = estadisticos(price)

                    cursor = cnx.cursor()
                    update = ("UPDATE productos SET minimo_30=%s, maximo_30=%s, variacion_30=%s, media_30=%s where descripcion=%s")
                    cursor.execute(update, (str(mins), str(maxs), str(variacion), str(media), title))
                    cnx.commit()

productos()
#SE VA A CORRER 3 VECES AL DIA, IGUAL QUE EL MAIN
