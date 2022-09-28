#Este script sirve para hallar los estadisticos dentro del apartado de reportes
#Para los outputs tener en cuenta las tablas de salida en el html
#Ver si crear un mysql de los reportes o un .csv

import pandas as pd
import mysql.connector
from pytz import timezone
import datetime
import numpy as np

#cnx = mysql.connector.connect(host='neurometricslab.mysql.pythonanywhere-services.com', user='neurometricslab', password='pricemap', database='neurometricslab$default')

price_evol = pd.read_csv("price_evolution.csv")

#Me da todos los productos dentro de la bd mysql 
'''cursor = cnx.cursor()
cursor.execute('SELECT descripcion, sku_wong, sku_metro, sku_pv, sku_vivanda, sku_tottus FROM productos')
data = cursor.fetchall()
cuadro_tabla_1 = tabla1(data) #Devuelve una matriz de 2 dimensiones
cnx.commit()
'''
#If data[0] == .... : 
#   wong = price_evol[(price_evol["sku"] == data[1]) & (price_evol["retail"] == "wong")]
#   metro = price_evol[(price_evol["sku"] == data[2]) & (price_evol["retail"] == "metro")]
#   pv = price_evol[(price_evol["sku"] == data[3]) & (price_evol["retail"] == "plaza_vea")]
#   vivanda = price_evol[(price_evol["sku"] == data[4]) & (price_evol["retail"] == "vivanda")]
#   tottus = price_evol[(price_evol["sku"] == data[5]) & (price_evol["retail"] == "tottus")]
#
#   reporte = pd.concat([wong,metro,pv,vivanda,tottus], axis=0)
#
# ¿QUE HACER SI FALTAN DATOS? Rellenar con el promedio de los valores anteriores y posteriores + cercanos de la misma tienda
# ¿TRABAJAR CON DATA DE MÁS DÍAS?, no habría problema, pero se cambiarian algunas tablas
# 
#
#

#Arroz extra costeño 5kg

#Falta agregar azucar blanca a la bd

#Azúcar Rubia Dulfina Bolsa 1 kg

#Coca Cola 500 ml

#Fideo Spaghetti Don Vittorio 950g

#Inca Kola 500 ml

#Leche Evaporada Entera Gloria Lata 400 gr

#Falta agregar pan a la bd

#Trozos de Atún en Aceite Vegetal Florida 150g

def sieteDias():
    est = timezone('EST')
    now = datetime.datetime.now(est) - datetime.timedelta(days=7)
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    current_date = '{}-{}-{}'.format(year, month, day)
    return current_date

def tabla1(data):
    '''wong = price_evol[(price_evol["sku"] == "294661") & (price_evol["retail"] == "wong")]
    metro = price_evol[(price_evol["sku"] == "294661") & (price_evol["retail"] == "metro")]
    pv = price_evol[(price_evol["sku"] == "20280294") & (price_evol["retail"] == "plaza_vea")]
    vivanda = price_evol[(price_evol["sku"] == "20280294") & (price_evol["retail"] == "vivanda")]
    tottus = price_evol[(price_evol["sku"] == "42747310") & (price_evol["retail"] == "tottus")]'''


    cuadro_tabla_1 = []
    current_date = sieteDias()

    for producto_fila in data:

        wong = price_evol[(price_evol["sku"] == producto_fila[1]) & (price_evol["retail"] == "wong")]
        metro = price_evol[(price_evol["sku"] == producto_fila[2]) & (price_evol["retail"] == "metro")]
        pv = price_evol[(price_evol["sku"] == producto_fila[3]) & (price_evol["retail"] == "plaza_vea")]
        vivanda = price_evol[(price_evol["sku"] == producto_fila[4]) & (price_evol["retail"] == "vivanda")]
        tottus = price_evol[(price_evol["sku"] == producto_fila[5]) & (price_evol["retail"] == "tottus")]

        reporte = pd.concat([wong,metro,pv,vivanda,tottus], axis=0)
        #SOLO SE TRABAJA CON LA COLUMNA PRICE (ONLINE)
        reporte.drop("price_tarjeta", axis=1, inplace=True)
        reporte.drop("price_tienda", axis=1, inplace=True)

        reporte = reporte.loc[reporte["date"]>=current_date]

        promedio = reporte['price'].mean()
        promedio = np.round(promedio,2)

        minimo = reporte['price'].min()
        minimo = np.round(minimo,2)

        maximo = reporte['price'].max()
        maximo = np.round(maximo,2)

        rango = maximo - minimo
        rango = np.round(rango,2)

        sensibilidad = reporte['price'].std() #Desviacion estandar
        sensibilidad = np.round(sensibilidad,2)

        reporte['price'].fillna((promedio), inplace=True) #Se llena con el promedio de todas las tiendas
        #TENER EN CONSIDERACION LO DE KELVER DE RELLENAR LA DATA CON EL PROMEDIO PERO PORRRRR TIENDA

        fila_tabla_1 = [producto_fila[0], promedio, maximo, minimo, sensibilidad, rango]
        cuadro_tabla_1.append(fila_tabla_1)

    return cuadro_tabla_1

#NO TIENE FILL NA, SI NO FUNCIONA CONSIDERAR ESTO
def tabla1_1(data):
    #TABLA 1.1 Y TABLA 1.2 (DIAPO 3)
    current_date = sieteDias()

    cuadro_tabla1_1 = []
    fila_tabla1_1 = []

    for producto_fila in data:
        wong = price_evol[(price_evol["sku"] == producto_fila[1]) & (price_evol["retail"] == "wong")]
        metro = price_evol[(price_evol["sku"] == producto_fila[2]) & (price_evol["retail"] == "metro")]
        pv = price_evol[(price_evol["sku"] == producto_fila[3]) & (price_evol["retail"] == "plaza_vea")]
        vivanda = price_evol[(price_evol["sku"] == producto_fila[4]) & (price_evol["retail"] == "vivanda")]
        tottus = price_evol[(price_evol["sku"] == producto_fila[5]) & (price_evol["retail"] == "tottus")]

        supermercados = [wong, metro, pv, vivanda, tottus]

        #ESTA EN EL ORDEN DE SUPERMERCADOS
        estadisticos_x_super = []

        for supermercado in supermercados:
            supermercado = supermercado.loc[supermercado["date"]>=current_date]
            supermercado.drop("price_tarjeta", axis=1, inplace=True)
            supermercado.drop("price_tienda", axis=1, inplace=True)

            promedio = supermercado['price'].mean()
            promedio = np.round(promedio,2)

            minimo = supermercado['price'].min()
            minimo = np.round(minimo,2)

            maximo = supermercado['price'].max()
            maximo = np.round(maximo,2)

            rango = maximo - minimo
            rango = np.round(rango,2)

            sensibilidad = supermercado['price'].std() #Desviacion estandar
            sensibilidad = np.round(sensibilidad,2)

            supermercado['price'].fillna((promedio), inplace=True)

            estadisticos_x_super.append([promedio, maximo, minimo, sensibilidad, rango])
        
        fila_tabla1_1.append([data[0], estadisticos_x_super])
    
    cuadro_tabla1_1.append(fila_tabla1_1)
     
    return cuadro_tabla1_1

#LA TABLA ESTA HECHA SIN EMBARGO AUN FALTA DETERMINAR LOS TITULOS DE 2.1 Y 2.2 (la tabla es la misma en 2, 2.1 , 2.2)
def tabla2(data):
    #MAÑANA -> 4 A 12 A TARDE -> 12 A 20 A NOCHE -> 20 A 4

    current_date = sieteDias()

    cuadro_tabla_2 = []
    for producto_fila in data:

        wong = price_evol[(price_evol["sku"] == producto_fila[1]) & (price_evol["retail"] == "wong")]
        metro = price_evol[(price_evol["sku"] == producto_fila[2]) & (price_evol["retail"] == "metro")]
        pv = price_evol[(price_evol["sku"] == producto_fila[3]) & (price_evol["retail"] == "plaza_vea")]
        vivanda = price_evol[(price_evol["sku"] == producto_fila[4]) & (price_evol["retail"] == "vivanda")]
        tottus = price_evol[(price_evol["sku"] == producto_fila[5]) & (price_evol["retail"] == "tottus")]

        reporte = pd.concat([wong,metro,pv,vivanda,tottus], axis=0)
        #SOLO SE TRABAJA CON LA COLUMNA PRICE (ONLINE)
        reporte.drop("price_tarjeta", axis=1, inplace=True)
        reporte.drop("price_tienda", axis=1, inplace=True)

        reporte = reporte.loc[reporte["date"]>=current_date]
        #SEPARAR POR DIA TARDE Y NOCHE

        #SI FUNCIONA
        reporte_dia = reporte.loc[(reporte['time'] >= '04:00') & (reporte['time'] < '12:00')]
        reporte_tarde = reporte.loc[(reporte['time'] >= '12:00') & (reporte['time'] < '20:00')]
        reporte_noche = reporte.loc[(reporte['time'] >= '20:00') & (reporte['time'] < '04:00')]

        time = [reporte_dia, reporte_tarde, reporte_noche]
        
        estadisticos_x_tiempo = [] #ESTA EN ORDEN

        for tiempos in time:
            promedio = tiempos['price'].mean()
            promedio = np.round(promedio,2)

            sensibilidad = tiempos['price'].std()
            sensibilidad = np.round(sensibilidad,2)

            estadisticos_x_tiempo.append([promedio, sensibilidad])
        
        promedios = [i[0] for i in estadisticos_x_tiempo]
        min_prom = np.min(promedios)

        #Solo para encontrar si hay duplicado osea empate
        u, c = np.unique(promedios, return_counts=True)
        dup = u[c > 1]
        if len(dup)!=0:
            periodo_mas_barato_prom = "empate"
        elif min_prom == promedios[0]:
            periodo_mas_barato_prom = "mañana"
        elif min_prom == promedios[1]:
            periodo_mas_barato_prom = "tarde"
        elif min_prom == promedios[2]:
            periodo_mas_barato_prom = "noche"

        #SI SALE FEO, COLOCARLE [] AL PERIODO+...
        cuadro_tabla_2.append([producto_fila[0], estadisticos_x_tiempo, periodo_mas_barato_prom])

    return cuadro_tabla_2

def tabla2_3(data):
    current_date = sieteDias()
    cuadro_tabla2_3 = []
    for producto_fila in data:

        wong = price_evol[(price_evol["sku"] == producto_fila[1]) & (price_evol["retail"] == "wong")]
        metro = price_evol[(price_evol["sku"] == producto_fila[2]) & (price_evol["retail"] == "metro")]
        pv = price_evol[(price_evol["sku"] == producto_fila[3]) & (price_evol["retail"] == "plaza_vea")]
        vivanda = price_evol[(price_evol["sku"] == producto_fila[4]) & (price_evol["retail"] == "vivanda")]
        tottus = price_evol[(price_evol["sku"] == producto_fila[5]) & (price_evol["retail"] == "tottus")]

        reporte = pd.concat([wong,metro,pv,vivanda,tottus], axis=0)
        #SOLO SE TRABAJA CON LA COLUMNA PRICE (ONLINE)
        reporte.drop("price_tarjeta", axis=1, inplace=True)
        reporte.drop("price_tienda", axis=1, inplace=True)

        reporte = reporte.loc[reporte["date"]>=current_date]
        #SEPARAR POR DIA TARDE Y NOCHE

        #SI FUNCIONA
        reporte_dia = reporte.loc[(reporte['time'] >= '04:00') & (reporte['time'] < '12:00')]
        reporte_tarde = reporte.loc[(reporte['time'] >= '12:00') & (reporte['time'] < '20:00')]
        reporte_noche = reporte.loc[(reporte['time'] >= '20:00') & (reporte['time'] < '04:00')]

        time = [reporte_dia, reporte_tarde, reporte_noche]
        
        minimos = []
        maximos = []
        for tiempos in time:
            minimo = tiempos["price"].min()
            minimo = np.round(minimo,2)
            minimos.append(minimo)

            maximo = tiempos["price"].max()
            maximo = np.round(maximo,2)
            maximos.append(maximo)

        #ESTA EN ORDEN
        cuadro_tabla2_3.append([producto_fila[0], minimos, maximos])
    
    return cuadro_tabla2_3

def tabla3(data):
    current_date = sieteDias()

    cuadro_tabla3= []

    for producto_fila in data:
        wong = price_evol[(price_evol["sku"] == producto_fila[1]) & (price_evol["retail"] == "wong")]
        metro = price_evol[(price_evol["sku"] == producto_fila[2]) & (price_evol["retail"] == "metro")]
        pv = price_evol[(price_evol["sku"] == producto_fila[3]) & (price_evol["retail"] == "plaza_vea")]
        vivanda = price_evol[(price_evol["sku"] == producto_fila[4]) & (price_evol["retail"] == "vivanda")]
        tottus = price_evol[(price_evol["sku"] == producto_fila[5]) & (price_evol["retail"] == "tottus")]

        supermercados = [wong, metro, pv, vivanda, tottus]

        #ESTA EN EL ORDEN DE SUPERMERCADOS
        minimos_x_super = []

        for supermercado in supermercados:
            supermercado = supermercado.loc[supermercado["date"]>=current_date]
            supermercado.drop("price_tarjeta", axis=1, inplace=True)
            supermercado.drop("price_tienda", axis=1, inplace=True)

            minimo = supermercado['price'].min()
            minimo = np.round(minimo,2)

            minimos_x_super.append(minimo)
        
        minimo_de_minimos = np.min(minimos_x_super)

        #Se hace para ver si hay empate
        if len(minimos_x_super) != len(set(minimos_x_super)):
            ultima_columna = "empate"
        elif minimo_de_minimos == minimos_x_super[0]:
            ultima_columna = "wong"
        elif minimo_de_minimos == minimos_x_super[1]:
            ultima_columna = "metro"
        elif minimo_de_minimos == minimos_x_super[2]:
            ultima_columna = "plaza vea"
        elif minimo_de_minimos == minimos_x_super[3]:
            ultima_columna = "vivanda"
        elif minimo_de_minimos == minimos_x_super[4]:
            ultima_columna = "tottus"

        cuadro_tabla3.append(minimos_x_super, ultima_columna)
    
    return cuadro_tabla3

def tabla3_1(data):
    current_date = sieteDias()

    for producto_fila in data:

        wong = price_evol[(price_evol["sku"] == producto_fila[1]) & (price_evol["retail"] == "wong")]
        metro = price_evol[(price_evol["sku"] == producto_fila[2]) & (price_evol["retail"] == "metro")]
        pv = price_evol[(price_evol["sku"] == producto_fila[3]) & (price_evol["retail"] == "plaza_vea")]
        vivanda = price_evol[(price_evol["sku"] == producto_fila[4]) & (price_evol["retail"] == "vivanda")]
        tottus = price_evol[(price_evol["sku"] == producto_fila[5]) & (price_evol["retail"] == "tottus")]

        supermercados = [wong, metro, pv, vivanda, tottus]

        return 'No see...'

