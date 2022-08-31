from flask import Flask, render_template
import plotly.graph_objects as go
import json
import plotly
import plotly.io as pio
import chart_studio.plotly as py
import numpy as np

app = Flask(__name__)


#https://stackoverflow.com/questions/4828406/import-a-python-module-into-a-jinja-template
#https://plotly.com/python/creating-and-updating-figures/
#https://plotly.com/python/renderers/


#HACER TIEMPO DE IMAGENES
'''def create_fig(retailers, skus, title, price_evolution_data):   
    ## create traces
    fig = go.Figure()

    ## navigate for each retail and sku
    for retail, sku in zip(retailers, skus):
        ## select the sku and retail
        query = price_evolution_data.loc[(price_evolution_data['sku'] == sku) & (price_evolution_data['retail'] == retail)]
        price = query["price"] ## get the price
        date = query["date"] ## get the date
        
        fig.add_trace(go.Scatter(x=date.values,
                                 y=price.values,                                
                                 name=retail))
        
    fig.update_traces(mode='lines+markers')
    fig.update_layout(title={
                            'text': title,
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    
    return fig'''

def create_fig(retailers, skus, title, price_evolution_data):   
    ## create traces
    fig = go.Figure()

    #Save prices
    prices = []
    ## navigate for each retail and sku
    for retail, sku in zip(retailers, skus):
        ## select the sku and retail
        query = price_evolution_data.loc[(price_evolution_data['sku'] == sku) & (price_evolution_data['retail'] == retail)]
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

@app.route("/prueba")
def pag_prueba():
    retailers = ["wong", "metro", "plaza_vea", "tottus", "vivanda"]
    skus = ["59539001", "59539001", "497497", "10174358", "497497"]
    title = 'INKA COLA 500ML'
    fig, price = create_fig(retailers, skus, title, price_evolution_data)
    fig.write_html("static/img/fig2.html") #NO HACE OVERWRITE, BUSCAR FORMA PARA HACERLO

    #mi,ma, mean, var_t, var_d = estadisticos(price)
    #return render_template('prueba.html', mi=mi, ma=ma, mean=mean,var_t=var_t,var_d=var_d)

    mins, maxs, variacion = estadisticos(price)
    retailers = ["WONG", "METRO", "PLAZA VEA", "TOTTUS", "VIVANDA"]


    return render_template('prueba.html',mins = mins, maxs = maxs, variacion=variacion,retailers=retailers)

'''@app.context_processor
def add_imports():
    return dict(numpy=numpy)    
'''

def estadisticos(price):
    maxs = []
    mins = []
    #1: WONG, 2: METRO, 3: PLAZA VEA, 4: TOTTUS Y 5: VIVANDA
    for i in price:
        if len(i)!=0:
            mins.append(np.nanmin(i))
            maxs.append(np.nanmax(i))
        else:
            mins.append(99999)
            maxs.append(0)

    mins = comparador_min(mins)
    maxs = comparador_max(maxs)
    var = variacion(price)
    return mins, maxs, var

'''#Para estos 3, está bien juntar todos
#MINIMO, MAXIMO, PROMEDIO DE TODA LA SEMANA O EL PERIODO DE TIEMPO
minimo = np.min(price)
maximo = np.max(price)
promedio = np.round(np.mean(price),1)

#Variación inicio a fin (NO ES DE TODOS JUNTOS)
inicio = price[0]
fin = price[-1]
variacion_total = ((fin-inicio)/inicio)*100

#Variacion ultimas 24h (NO ES DE TODOS JUNTOS)
inicio = price[-4]
fin = price[-1]
variacion_dia = ((fin-inicio)/inicio)*100

return minimo, maximo, promedio, variacion_total, variacion_dia
'''

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

