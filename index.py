from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
import json
import plotly
import plotly.io as pio
import chart_studio.plotly as py
import numpy as np
from pytz import timezone
import datetime

app = Flask(__name__)

#https://stackoverflow.com/questions/4828406/import-a-python-module-into-a-jinja-template
#https://plotly.com/python/creating-and-updating-figures/
#https://plotly.com/python/renderers/

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

@app.route("/")
def pagina_principal():
    return render_template('index.html')

@app.route("/prueba", methods=["GET", "POST"])
def pag_prueba():

    try:
        dias = request.form['days']
    except:
        dias = "7"
    
    retailers = ["wong", "metro", "plaza_vea", "tottus", "vivanda"]
    skus = ["59539001", "59539001", "497497", "10174358", "497497"]
    title = 'INKA COLA 500ML'
    fig, price = create_fig(retailers, skus, title, price_evolution_data, dias)
    fig.write_html("static/img/fig2.html") #NO HACE OVERWRITE, BUSCAR FORMA PARA HACERLO

    mins, maxs, variacion, media = estadisticos(price)
    retailers = ["WONG", "METRO", "PLAZA VEA", "TOTTUS", "VIVANDA"]

    print("GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print("Minimo: ", type(mins), "\n")
    print("Maximo: ", type(maxs), "\n")
    print("Variacion: ", type(variacion), "\n")
    print("Media: ", type(media), "\n")

    checked = "checked"

    return render_template('borrar.html',mins = mins, maxs = maxs, variacion=variacion,retailers=retailers, media=media, dias = dias, checked=checked)

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

if __name__ == '__main__':
    import pandas as pd
    price_evolution_data = pd.read_csv("price_evolution.csv")
    app.run(debug=True)

