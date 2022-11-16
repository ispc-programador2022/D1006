


import csv
with open('C:/Users/angel/PROYECTO INTEGRADOR D1006/D1006/database.csv', encoding="utf8", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|', )
    for row in spamreader:
        print(', '.join(row))

print('''
¡¡¡BIENVENIDO, ESTAMOS PARA BRINDARTE TODA LA INFORMACION QUE NECESITES!!!
''')

import mysql.connector as msql
from mysql.connector import Error

quest = str(input("¿Querés hacer una consulta? / Ingresá SI o NO: "))
quest = quest.lower()
def querrys():
    try:
        global querr
        global answ

        querr = str(input("Ingresá la opción correspondiente / 1. Precios, 2. Otros, Cualquier ingreso: Salir: "))

        if querr == '1':
            answ = str(input("Ingresá la opcion: 1. Precios de todos los productos, 2. Los precios más caros (+ de 145.000), 3 Los precios más baratos (- de 145.000), Cualquier ingreso: Salir: "))
            if answ == '1':
                answ = "SELECT id,products, price from proyecto"
            elif answ == '2':
                answ = "SELECT id, products, brands, price, price, total_pricefin FROM proyecto WHERE price > 145000 ORDER BY price DESC"
            elif answ == '3':
                answ = "SELECT id,products, brands, price, price, total_pricefin FROM proyecto WHERE price < 145000 ORDER BY price ASC"
            else:
                return 
        if querr == '2':
            answ = str(input("Ingresá la opción: 1. Productos por Marcas, 2. Productos por vendedores, Cualquier ingreso: Salir: "))
            if answ == '1':
                answ = "SELECT id, brands, products, price, total_pricefin from proyecto ORDER BY brands"
            elif answ == '2':
                answ = "SELECT id, seller products, price, price, total_pricefin from proyecto ORDER BY seller"
    except:
        print("Querés salir o algo ha fallado...!")



contador = 1
while contador == 1:
    if quest == "si":
        try:
            conn = msql.connect(host='localhost', database='dbproyecto', user='root', password='adolfito06')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Estamos procesando tu consulta")
                (querrys())
                if answ is False:
                    raise Exception
                sql = answ
                cursor.execute(sql)
                proyecto = cursor.fetchone()
                print('Procesando')
                while proyecto:
                        print(proyecto)
                        proyecto = cursor.fetchone()
        except Error as e:
                    print("¿Deseás salir o algo ha fallado?")
        except Exception:
            print("¿Deseás salir o algo a fallado")
        quest = str(input("¿Querés hacer otra consulta o salir? / NO para salir, cualquier ingreso para continuar: "))   
        contador = 1
    if quest == "no":
        contador = 0
    else:
        quest = str(input("Hay un problema... / Ingresá si para continuar, NO para salir: ")).lower()
        if quest == "si":
            contador = 1
        if quest == "no":
            contador = 0   
print("¡Muchas gracias, esperamos verte pronto!")
