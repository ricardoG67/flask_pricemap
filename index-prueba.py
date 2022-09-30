from flask import Flask, render_template, request, redirect, url_for, flash, session
import ast
import mysql.connector
from flask_bcrypt import Bcrypt
from validate_email import validate_email
import datetime
from pytz import timezone
import numpy as np
import timeit

app = Flask(__name__)

cnx = mysql.connector.connect(host='localhost', user='root', password='', database='pricemap')
bcrypt = Bcrypt(app)

# SESION
app.secret_key = 'mysecretkey'

@app.route("/")
def pagina_principal():
    return render_template('index.html')

@app.route("/faqs")
def faqs():
    
    '''
    

    ###########################################
    #PARA MÁS CATEGORIAS SE TIENE QUE VER DE QUE SE TIENE PRECIOS E INFORMACIÓN

    Ver los skus y agregarlos directamente a la base de datos

    Luego correr estadisticos
    '''

    return render_template('faqs.html', fecha = fecha)

def actualizar_fecha_login(email):
    #ESTE ES EL APPROACH MÁS SENCILLO  Y EL MEJOR 
    #FALTA AGREGAR EL INICIO DE LA CONEXION Y EL CIERRE
    est = timezone('EST')
    now = datetime.datetime.now(est)
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)

    fecha = '{}/{}/{} {}:{}'.format(day, month, year , hour, minute) #Hacer que pueda ser null, y que sea string 

    cursor = cnx.cursor()
    update = ("UPDATE users SET fecha_login=%s where email=%s")
    cursor.execute(update, (fecha, email))
    cnx.commit()




@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if 'email' not in session:
        return "<h1>ERROR 401 USTED NO ESTA AUTENTIFICADO</h1>"

    try:
        dias = request.form['days']
        print(dias)
    except:
        dias = 7
    
    #Las imagenes y los estadisticos se actualizan a la par con el main
    #En este apartado solo se llama a los estadisticos

    #Se coloca con ambos tipos de datos, debido a que a veces agarra
    #como tipo string y otras como tipo entero
    if dias == "7" or dias==7:
        cursor = cnx.cursor()
        cursor.execute('SELECT Categoria,descripcion,minimo_7, maximo_7, variacion_7, media_7 FROM productos')
        data = cursor.fetchall()
        cnx.commit()
    elif dias == "14" or dias==14:
        cursor = cnx.cursor()
        cursor.execute('SELECT Categoria,descripcion,minimo_14, maximo_14, variacion_14, media_14 FROM productos')
        data = cursor.fetchall()
        cnx.commit()
    elif dias == "30" or dias==30:
        cursor = cnx.cursor()
        cursor.execute('SELECT Categoria,descripcion,minimo_30, maximo_30, variacion_30, media_30 FROM productos')
        data = cursor.fetchall()
        cnx.commit()

    minimos = []
    maximos = []
    variaciones = []
    medias = []
    productos = []
    categorias = []

    for i in data:
        categoria = i[0]
        producto_name = i[1]
        minimo = ast.literal_eval(i[2])
        maximo = ast.literal_eval(i[3])
        variacionn = ast.literal_eval(i[4])
        media = float(i[5])

        minimos.append(minimo)
        maximos.append(maximo)
        variaciones.append(variacionn)
        medias.append(media)
        productos.append(producto_name)
        categorias.append(categoria)

    productos = list(map(lambda x: "/static/img/figuras/" + x.replace(" ","") + "_" + str(dias) + ".html", productos))

    print(productos)

    retailers = ["Wong", "Metro", "Plaza Vea", "Tottus", "Vivanda"]

    print(minimos)

    return render_template('prueba.html',mins = minimos, maxs = maximos, variacion=variaciones,retailers=retailers, media=medias, productos=productos, categorias=categorias)

@app.route("/admin")
def admin():
    if 'admin' not in session:
        return "<h1>SOLO EL ADMINISTRADOR PUEDE VER ESTA PÁGINA</h1>"

    with open("log_precios.txt") as f:
        logs = f.readlines()

    return render_template("dashboard-admin.html", logs = logs)

@app.route("/register")
def signup():
    return render_template("signup.html")

@app.route('/signup_comprobacion', methods=['POST'])
def signup_comprobacion():
    email = request.form['email']
    pass1 = request.form['pass']
    pass2 = request.form['pass2']

    errores = validar(email)

    if (pass1 == pass2) and (errores == False):
        cursor = cnx.cursor()
        passFinal = bcrypt.generate_password_hash(pass1)
        insert = "INSERT INTO `users`(email, password) VALUES(%s, %s)"
        cursor.execute(insert, (email, passFinal))
        cnx.commit()
        flash('USUARIO CREADO')
    
    elif (pass1!=pass2):
        flash('Las constraseñas son diferentes')

    return redirect(url_for('signup'))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/login_comprobacion', methods=['POST'])
def login_comprobacion():
    email = request.form['email']
    pass1 = request.form['pass']

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s', [email])
    data = cursor.fetchone()        
    cnx.commit()

    if data!=None:
        if bcrypt.check_password_hash(data[2],pass1):

            session["email"] = email

            if data[3] == "admin":

                session["admin"] = data[3]
                return redirect(url_for('admin'))

            return redirect(url_for('dashboard'))
        else:
            flash('La contraseña es incorrecta')
    else:
        flash('La cuenta no existe')


    return redirect(url_for('login'))

def validar(e):
    errores = False

    if validate_email(e) == False:
        errores = True
        flash('Ingrese un correo valido')

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s', [e])
    data = cursor.fetchone()
    cnx.commit()

    if data!=None:
        errores = True
        flash('La cuenta ya existe')

    return errores

@app.route("/logout")
def logout():
    if "email" in session:
        session.pop("email")
    if "admin" in session:
        session.pop("admin")
    return redirect(url_for("login"))

@app.route("/usuarios")
def usuarios():
    if 'admin' not in session:
        return "<h1>SOLO EL ADMINISTRADOR PUEDE VER ESTA PÁGINA</h1>"

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()

    return render_template("usuarios.html", data = data)

# decimos que esta al lado de un string llamado id
@app.route('/delete_task/<string:id>')
def delete_contact(id):
    cursor = cnx.cursor()
    eliminar = 'DELETE FROM users WHERE id=%s'
    # (id,) tambien sirve, es un error que no recibe string solo list o tuplas
    cursor.execute(eliminar, [id])
    cnx.commit()
    return redirect(url_for('usuarios'))

@app.route('/update_task/<string:id>')
def update_contact(id):
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM users WHERE id=%s', [id])
    data = cursor.fetchone()
    cnx.commit()
    return render_template('usuarios-edit.html', data=data)


@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    email = request.form['email']
    tipo_usuario = request.form['tipo_usuario']

    cursor = cnx.cursor()
    update = ("UPDATE users SET email=%s, tipo_usuario=%s where id=%s")
    cursor.execute(update, (email, tipo_usuario, id))
    cnx.commit()

    return redirect(url_for('usuarios'))

@app.route('/reportes')
def reportes():
    
    cuadro_1 = np.load("cuadro_1.npy")
    cuadro_1_1 = np.load("cuadro_1_1.npy", allow_pickle=True)
    cuadro2= np.load("cuadro2.npy", allow_pickle=True)  
    cuadro2_chiquito= np.load("cuadro2_chiquito.npy", allow_pickle=True)
    cuadro2_3 = np.load("cuadro2_3.npy", allow_pickle=True)
    cuadro3 = np.load("cuadro3.npy", allow_pickle=True)
    cuadro4 = np.load("cuadro4.npy", allow_pickle=True)
    cuadro5 = np.load("cuadro5.npy", allow_pickle=True)

    titulo1, titulo2_1, titulos2_2, titulo3, titulo4, titulo5 = titulos_reportes(cuadro_1, cuadro2, cuadro3, cuadro4, cuadro5)

    return render_template('reportes.html', cuadro_1 = cuadro_1, cuadro_1_1 = cuadro_1_1, cuadro2 = cuadro2,
    cuadro2_chiquito = cuadro2_chiquito, cuadro2_3 = cuadro2_3, cuadro3 = cuadro3, cuadro4=cuadro4, cuadro5 = cuadro5,
    titulo1=titulo1, titulo2_1=titulo2_1, titulos2_2=titulos2_2, titulo3=titulo3, titulo4=titulo4, titulo5=titulo5)

def titulos_reportes(cuadro_1, cuadro2, cuadro3, cuadro4, cuadro5):

    #TITULOS
    #Titulo 1:
    sensibilidad = []
    productos = {}
    for fila in cuadro_1:
        sensibilidad.append(fila[4])
        productos[fila[4]] = fila[0]
    
    mayor_sensibilidad = np.nanmax(list(map(lambda x: float(x), sensibilidad)))
    mayor_sensibilidad = productos.get(str(mayor_sensibilidad))
    titulo1 = f"El producto más sensible en todo el mercado es {mayor_sensibilidad}"

    #Titulo 1_1 (FALTA)

    #Titulo 2 (HACERLO EN EL HTML Ver máxima desviación en cuadro chiquito)
    #Titulo 2_1 (Ver que producto varía más en cada periodo del día)
    sens_dia = []
    sens_tarde = []
    sens_noche = []
    productos = {}
    ganadores = {}
    for fila in cuadro2:
        dia_desv = fila[1][0][1]
        sens_dia.append(dia_desv)

        tarde_desv = fila[1][1][1]
        sens_tarde.append(tarde_desv)

        noche_desv = fila[1][2][1]
        sens_noche.append(noche_desv)

        productos[fila[0]] = [dia_desv, tarde_desv, noche_desv]
        ganadores[fila[0]] = fila[2]
    
    mayor_sensibilidad_dia = np.nanmax(list(map(lambda x: float(x), sens_dia)))
    mayor_sensibilidad_tarde = np.nanmax(list(map(lambda x: float(x), sens_tarde)))
    mayor_sensibilidad_noche = np.nanmax(list(map(lambda x: float(x), sens_noche)))

    for i in productos:
        sensibilidades = productos.get(i)
        if sensibilidades == [mayor_sensibilidad_dia, mayor_sensibilidad_tarde, mayor_sensibilidad_noche]:
            titulo2_1 = f"El producto cuyo precio tiene más variación en los tres periodos es {i}"
        else:
            titulo2_1 = ""
    
    titulos2_2 = []
    for i in ganadores:
        ganador = ganadores.get(i)
        if ganador != "empate":
            titulos2_2.append(f"El producto {i} es más barato en promedio en la {ganador}")

    #titulo2_3 AUN NO HACER PORQUE NO ME SALE NADA

    #Titulo3 
    ganadores = []
    for fila in cuadro3:
        if fila[2]!="empate":
            ganadores.append(fila[2])

    mas_repetido = max(set(ganadores), key = ganadores.count)
    titulo3 = f"{mas_repetido} tuvo el menor precio mínimo {ganadores.count(mas_repetido)} veces" 

    #Titulo4 
    ganadores = []
    for fila in cuadro4:
        if fila[2]!="empate":
            ganadores.append(fila[2])

    mas_repetido = max(set(ganadores), key = ganadores.count)
    titulo4 = f"{mas_repetido} tuvo el mayor precio máximo {ganadores.count(mas_repetido)} veces" 

    #Titulo 5
    ganadores = []
    for fila in cuadro5:
        if fila[2]!="empate":
            ganadores.append(fila[2])

    mas_repetido = max(set(ganadores), key = ganadores.count)
    titulo5 = f"{mas_repetido} tuvo el menor precio promedio {ganadores.count(mas_repetido)} veces" 

    return titulo1, titulo2_1, titulos2_2, titulo3, titulo4, titulo5

if __name__ == '__main__':
    app.run(debug=True)

