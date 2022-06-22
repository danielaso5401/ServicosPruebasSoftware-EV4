import json
from flask import Flask,redirect,url_for,render_template,request
from numpy import empty
from bd import obtener_conexion
from datetime import date, datetime
conexion = obtener_conexion()

def insertar_alumno(nombre, apellido, fechanacimiento,celular,email,pais,direccion ):    
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO t_alumno(nombre, apellido, fechanacimiento, celular, email, pais, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       ((nombre, apellido, fechanacimiento, celular, email, pais, direccion)))
    conexion.commit()

def insertar_producto(nombre, precio, stock ):    
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO t_productos(nombre, precio, stock) VALUES (%s, %s, %s)",
                       ((nombre, precio, stock)))
    conexion.commit()

def insertar_pago(nombre, contraseña):    
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO t_pagos(nombre, contraseña) VALUES (%s, %s)",
                       ((nombre, contraseña)))
    conexion.commit()
def insertar_empleado(nombre,apellido,cargo):
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO t_empleado(nombre, apellido, cargo) VALUES (%s, %s, %s)",
                       ((nombre, apellido, cargo)))
    conexion.commit()
def obtener_correo(email):
    val = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT email FROM t_alumno WHERE email = %s", (email,))
        val = cursor.fetchone()
        if val is None:
            return "none"
    return val

def calculateAge(birthDate): 
    today = date.today() 
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    return age 

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    return ("ServerPruebas")
    
@app.route("/registroPersona", methods=['POST'])
def create_alumno():
    content = request.json
    if content is empty:
        return("solicitud denegada",500)
    elif content["nombre"]=="" or content["apellido"]=="" or content["fechanacimiento"]=="" or content["celular"]=="" or content["email"]=="" or content["pais"]=="" or content["direccion"]=="":
        return("solicitud denegada",500)
    edad = datetime.strptime(content["fechanacimiento"], '%Y-%m-%d')
    if calculateAge(edad)<=18:
        return("registro en espera por ser menor de edad")
    elif content["email"]==obtener_correo(content["email"])[0]:
        return("solicitud denegada por correo duplicado",500)
    insertar_alumno(content["nombre"],content["apellido"],content["fechanacimiento"],content["celular"],content["email"],content["pais"],content["direccion"])
    return("OK registro completado",200)

@app.route("/registroProductos", methods=['POST'])
def create_productos():
    content = request.json
    insertar_producto(content["nombres"],content["precio"],content["stock"])
    return("producto seleccionado",200)

@app.route("/registroTarjeta", methods=['POST'])
def regist_tarjeta():
    content=request.json
    value2={
        "Response":{
            "Verificacion": "error"
        }
    }
    if content["nombre"]=="" and content["contra"]:
        return json.dumps(value2)
    insertar_pago(content["nombre"],content["contra"])
    value={
        "Response":{
            "Verificacion": "validado"
        }
    }
    return json.dumps(value)

@app.route("/registroEmpleados")
def regis_empl():
    content=request.json
    insertar_empleado(content["nombre"],content["apellido"],content["cargo"])
    return ("Carga exitosa",200)

if __name__ == '__main__':
    
    app.run(port=5000,debug=True)