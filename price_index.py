import numpy as np
from pytz import timezone
import datetime
import plotly.graph_objects as go
import pricemap
import pandas as pd

#Para usar pricemap necesitas uri, retail, sku
#pricemap.get_price_retail(uri, retail, sku)

#
#
#CAMBIAR ENFOQUE PORQUE NO ESTÁ SALIENDO
#
#
def dia(days=0):
    est = timezone('EST')
    now = datetime.datetime.now(est) - datetime.timedelta(days)
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    current_date = '{}-{}-{}'.format(year, month, day)
    return current_date


def create_fig(skus, title, price_evolution_index):   
    ## create traces
    fig = go.Figure()

    ## navigate for each retail and sku
    for sku in skus:
        ## select the sku and retail
        query = price_evolution_index.loc[(price_evolution_index['pack_sku'] == sku)]

        query = query.loc[query["time"]>=dia(30)]
        date = query["time"] ## get the date

        price_wong = query["wong"] ## get the price
        fig.add_trace(go.Scatter(x=date.values, y=price_wong.values, name="Wong"))

        price_metro = query["metro"] ## get the price
        fig.add_trace(go.Scatter(x=date.values, y=price_metro.values, name="Metro"))

        price_pv = query["plaza vea"] ## get the price
        fig.add_trace(go.Scatter(x=date.values, y=price_pv.values, name="Plaza Vea"))

        price_vivanda = query["vivanda"] ## get the price
        fig.add_trace(go.Scatter(x=date.values, y=price_vivanda.values, name="Vivanda"))

        price_tottus = query["tottus"] ## get the price
        fig.add_trace(go.Scatter(x=date.values, y=price_tottus.values, name="Tottus"))

    fig.update_traces(mode='lines+markers')
    fig.update_layout(title={
                            'text': title,
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})

    return fig

#Pack Fiesta
    #en ese orden
#Ya no habria retail_data para los pricemap index, sino solo esto

#Pack1 = FIESTA
    #Wong COCA COLA, Wong RON CARTAVIO, wong EVERVESS, wong SMIRNOFF Y wong PIQUEOS 

#pack2 = lonchera colegio
    #Frugos, pan d molede, jamon, queso, mantequilal, yogurt

#pack3 = Lonchera oficina (falta)

#pack4 = ALmuerzo chihuan (cambiar nombre)
    #Inca kola, atún, arroz

#pack5 = Mercado (falta revisar)

#pack6 = Desayuno familiar

#pack7 = Meet an drink

#pack8 = Campamento
    #marshmellow, galleta, pan molde, jamon, queso, mantequilla

Pack_1 = {"wong":[45035, 452311, 470198, 16561, 757207], "metro":[45035, 452311, 470198, 16561, 757207], 
"plaza_vea":[21130, 20061865, 20075684, 20190353, 20179461], "vivanda":[21130, 20061865, 20075684,
20190353, 20179461], "tottus":[10164192, 40728756,40844765,42001773,41899197]}

Pack_2 = {"wong":[718596001, 428478, 526949, 194006, 15025, 95540002], "metro":[718596001,
428478, 526949, 194006, 15025, 95540002], "plaza_vea":[20144006, 20046056, 20220539, 20047414, 831215,
86473], "vivanda":[20144006, 20046056, 20220539, 20047414, 831215, 86473], "tottus":
[41738590, 40641500, 42372433, 40865181, 10165832, 40928204]}

#Pack_3 = {"wong":[], "metro":[], "plaza_vea":[], "vivanda":[], "tottus":[]}

Pack_4 = {"wong":[45190, 294661, 171247], "metro":[45190, 294661, 171247], "plaza_vea":[21186,
20280294, 931740], "vivanda":[21186, 20280294,931740], "tottus":[10174382, 42747310, 20092463]}

#Pack_5 = {"wong":[], "metro":[], "plaza_vea":[], "vivanda":[], "tottus":[]}

#Pack_6 = {"wong":[], "metro":[], "plaza_vea":[], "vivanda":[], "tottus":[]}

Pack_7 = {"wong":[942480, 45035, 757207], "metro":[942480, 45035, 757207], "plaza_vea":[20253490, 21130,20179461], 
"vivanda":[20253490, 21130,20179461], "tottus":[42522653, 10164192, 41899197]}

Pack_8 = {"wong":[131712001, 348486, 428478, 526949, 194006, 15025], "metro":[131712001, 
348486, 428478, 526949, 194006, 15025], "plaza_vea":[1089881001, 502139, 20046056, 
20220539, 20047414, 831215], "vivanda":[1089881001, 502139, 20046056, 20220539, 20047414,
831215], "tottus":[10388641, 10255990, 40641500, 42372433, 40865181, 10165832]}

data = pd.read_csv("retail_data_final.csv")

#recibe diccionario y bota los precios de los packs por tienda

#Se cambia eso
data = pd.read_csv("price_evolution.csv")
current_date = dia()
data_mensual = data.loc[data["date"]>=current_date] #No es mensual es diaria

def precios_pack(pack):
    lista_precios_pack_x_supermercado = []
    for supermercado in pack:
        precio_total_pack = 0

        for producto in pack.get(supermercado):
            precio_producto = (data_mensual[(data_mensual["sku"] == str(producto)) & (data_mensual["retail"] == supermercado)].values)[0][1]
            
            if np.isnan(precio_producto):
                cuadro = data[(data["sku"] == str(producto)) & (data["date"]>=dia(7))]
                cuadro.fillna(cuadro.mean().round(1), inplace=True)
                precio_producto = (cuadro.values)[0][1]
            
            precio_total_pack+=precio_producto
        
        lista_precios_pack_x_supermercado.append(np.round(precio_total_pack, 2))
    return lista_precios_pack_x_supermercado


data_index = pd.read_csv("price_evolution_index.csv")

def pasar_a_csv(precios_p, sku):
    fila = pd.DataFrame([[str(sku),precios_p[0],precios_p[1],precios_p[2],precios_p[3],precios_p[4],current_date]], columns=["pack_sku","wong", "metro", "plaza vea", "vivanda", "tottus", "time"])

    fig = create_fig([str(sku)], "Fiesta", data_index)

    #url = "/home/neurometricslab/flask_pricemap/static/img/figuras_index/" + "pack1" +".html"
    url = "./static/img/figuras_index/" + str(sku) +".html"

    fig.write_html(url)

    return fila

########################################################################
#PACK 1
precios_pack_1 = precios_pack(Pack_1)

'''fila1 = pd.DataFrame([["Pack1",precios_pack_1[0],precios_pack_1[1],precios_pack_1[2],precios_pack_1[3],precios_pack_1[4],current_date]], columns=["pack_sku","wong", "metro", "plaza vea", "vivanda", "tottus", "time"])

###################

fig = create_fig(["Pack1"], "Fiesta", data_index)

#url = "/home/neurometricslab/flask_pricemap/static/img/figuras_index/" + "pack1" +".html"
url = "./static/img/figuras_index/" + "pack1" +".html"

fig.write_html(url) '''

fila1 = pasar_a_csv(precios_pack_1, "Pack1")
########################################################################
#PACK 2
precios_pack_2 = precios_pack(Pack_2)
fila2 = pasar_a_csv(precios_pack_2, "Pack2")

########################################################################
#PACK 4
precios_pack_4 = precios_pack(Pack_4)
fila4 = pasar_a_csv(precios_pack_4, "Pack4")

########################################################################
#PACK 7
precios_pack_7 = precios_pack(Pack_7)
fila7 = pasar_a_csv(precios_pack_7, "Pack7")

########################################################################
#PACK 8
precios_pack_8 = precios_pack(Pack_8)
fila8 = pasar_a_csv(precios_pack_8, "Pack8")

########################################################################

#Guardado en csv
data_index_excel = pd.concat([data_index, fila1, fila2, fila4, fila7, fila8], axis=0, ignore_index=True)

#data_index_excel.to_csv("price_evolution_index.csv", index=False)