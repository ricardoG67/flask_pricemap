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

#Pack_3 = {}

Pack_4 = {"wong":[45190, 960487, 171247], "metro":[45190, 960487, 171247], "plaza_vea":[21186,
20257683, 931740], "vivanda":[21186, 20257683,931740], "tottus":[10174382, 42699556, 20092463]}

#Pack_5 = {}

#Pack_6 = {}

#Pack_7 = {}

Pack_8 = {"wong":[131712001, 348486, 428478, 526949, 194006, 15025], "metro":[131712001, 
348486, 428478, 526949, 194006, 15025], "plaza_vea":[1089881001, 502139, 20046056, 
20220539, 20047414, 831215], "vivanda":[1089881001, 502139, 20046056, 20220539, 20047414,
831215], "tottus":[10388641, 10255990, 40641500, 42372433, 40865181, 10165832]}

data = pd.read_csv("retail_data_final.csv")

#recibe diccionario y bota los precios de los packs por tienda
def precios_pack(pack):
    pack_precios = []
    for supermercado in pack:

        precio_total_pack = 0
        for productos in pack.get(supermercado):
            fila = (data[(data["sku"] == str(productos)) & (data["retail"] == supermercado)].values)[0]
            precio = pricemap.get_price_retail(str(fila[3]),str(supermercado),str(productos))
            if precio is None:
                print("HAHA")

            print(fila, "\n", precio, "\n", precio_total_pack, "\n\n\n")
            precio_total_pack += precio[1]
        
        pack_precios.append(precio_total_pack) #Se guarda wong, metro, pv, vivanda, tottus
    
    return pack_precios

precios_pack_1 = precios_pack(Pack_1)
precios_pack_1 = ['Fiesta', precios_pack_1]

precios_pack_2 = precios_pack(Pack_2)
precios_pack_2 = ['Lonchera colegio', precios_pack_2]

#precios_pack_3 = precios_pack(Pack_3)
precios_pack_4 = precios_pack(Pack_4)
precios_pack_4 = ['Almuerzo barato', precios_pack_4]

#precios_pack_5 = precios_pack(Pack_5)
#precios_pack_6 = precios_pack(Pack_6)
#precios_pack_7 = precios_pack(Pack_7)
precios_pack_8 = precios_pack(Pack_8)
precios_pack_8 = ['Campamento', precios_pack_8]

precios = [precios_pack_1, precios_pack_2, precios_pack_4, precios_pack_8]


for precio in precios:
            #sku, wong, metro, pv, vivanda, tottus
    date, time = pricemap.get_time()
    fila = [precio[0], precio[1][0],precio[1][1],precio[1][2],precio[1][3],precio[1][4], date, time]
    df = pd.DataFrame(fila, columns=["sku", "Precio_wong", "Precio_Metro", "Precio_pv", "Precio_vivanda", "Precio_tottus", "date", "time"])
    df.to_csv("price_evolution_index.csv", index=False)



