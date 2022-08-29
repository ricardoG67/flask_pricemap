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
    skus = ["59539001", "59539001", "497497", "inca-kola-gaseosa-10174358/p/", "497497"]
    title = 'INKA COLA 500ML'
    fig, price = create_fig(retailers, skus, title, price_evolution_data)
    fig.write_html("static/img/fig1.html")

    mi,ma, mean, var_t, var_d = estadisticos(price)

    return render_template('prueba.html', mi=mi, ma=ma, mean=mean,var_t=var_t,var_d=var_d)

'''@app.context_processor
def add_imports():
    return dict(numpy=numpy)
'''
def estadisticos(price):
    print(price)
    maxs = []
    mins = []
    #1: WONG, 2: METRO, 3: PLAZA VEA, 4: TOTTUS Y 5: VIVANDA
    for i in price:
        if len(i)!=0:
            mins.append(np.min(i))
            maxs.append(np.max(i))
        else:
            mins.append(None)
            maxs.append(None)

    #Para estos 3, está bien juntar todos
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

if __name__ == '__main__':
    import pandas as pd
    price_evolution_data = pd.read_csv("price_evolution.csv")
    app.run(debug=True)

