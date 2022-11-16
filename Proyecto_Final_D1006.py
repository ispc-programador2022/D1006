'''
Pasos previos a iniciar el código:
INSTALAR LIBRERIAS BEATIFULSOUP, LXML, PANDAS, MYSQL.CONNECTOR
En la terminal:

pip install beautifulsoup4
pip install lxml
pip install pandas
pip install mysql.connector
'''

''' El trabajo se va a realizar descargando los archivos HTML que se subiran complementariamente al repositorio para probar el trabajo de web scraping'''

import glob

from bs4 import BeautifulSoup

datos = []

#Acá se cambia por el directorio local de los archivos HTML"
for file in glob.glob("C:/Users/angel/PROYECTO INTEGRADOR D1006/D1006/HTML/*.html"):
    with open(file, 'r', encoding="utf8", errors='ignore') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, 'lxml')

    bloques = soup.find_all('article', attrs={"id": "modern-variant-card"})

    for bloque in bloques:
        product = ""
        seller = ""
        brand = ""
        financial_mode = ""
        financing_amount = 0
        price = 0
        sale_price = 0

        valor = bloque.find('h6',  class_="d-inline-block")
        if valor:
            product = valor.text

        valor = bloque.find('div',  class_="shop-panel d-block mt-auto")
        if valor:
            seller = valor.text.replace("-", "").strip()

        valor = bloque.find('small',  class_="ng-star-inserted")
        if valor:
            f = valor.text.split("$")
            financial_mode = f[0]
            financing_amount = float(f[1].replace(
                "$", "").replace(".", "").replace(",", "."))

        valor = bloque.find(
            'div',  class_="manufacturer-panel d-block mt-auto")
        if valor:
            brand = valor.text.strip()

        # Trata de recuperar los precios unificados, si no encuenta valor, es porque vienen por separado, precio de oferta y precio regular
        valor = bloque.find(
            'span',  class_="price sale-price ng-star-inserted")
        if valor:
            price = float(valor.text.replace(
                "$", "").replace(".", "").replace(",", "."))
            sale_price = float(valor.text.replace(
                "$", "").replace(".", "").replace(",", "."))
        else:
            valor = bloque.find('span',  class_="price ng-star-inserted")
            if valor:
                price = float(valor.text.replace(
                    "$", "").replace(".", "").replace(",", "."))

            valor = bloque.find('span',  class_="sale-price ng-star-inserted")
            if valor:
                sale_price = float(valor.text.replace(
                    "$", "").replace(".", "").replace(",", "."))

        datos.append({"product": product, "brand": brand, "seller": seller,"financing_amount": financing_amount, "sale_price": sale_price})

#print(datos) como control

import pandas as pd

#Se crea el dataframe
df = pd.DataFrame.from_dict(datos)
df.index = df.index + 1

#Salida de control
#print(df)

#Se crea la columna precio total financiado
totalpf = df.financing_amount * 18

#Se concatena la tabla "totalpf" con "df"
finaldf = pd.concat([df, totalpf], axis=1)
finaldf.set_axis([ 'product', 'brand', 'seller','financing_amount', 'sale_price', 'total_pricefin'], 
                    axis='columns', inplace=True)
#Salida de control:
# print(finaldf)

#Se crea el archivo CSV en la ruta que elijan"
finaldf.to_csv(r'C:/Users/angel/PROYECTO INTEGRADOR D1006/D1006/database.csv', index=True, header=True)

#Para importar el csv se lee el archivo guardado en la ruta que se eligió"
empdata = pd.read_csv('C:/Users/angel/PROYECTO INTEGRADOR D1006/D1006/database.csv', index_col=False, delimiter = ',')
empdata.head()


#Usamos modulos mysql.connector para conectar a la base de datos
import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', user='root',  
                        password='adolfito06')#datos de acceso del usuario
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE dbproyecto")
        print("Base de datos creada")
except Error as e:
    print("Error al conectar con MySQL", e)

import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', database='dbproyecto', user='root', password='adolfito06') #datos de acceso del usuario
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Estás conectado a la base de datos: ", record)
        cursor.execute('DROP TABLE IF EXISTS dbproyecto;') #creación
        print('Creando tabla....')
        # Se crea la tabla con las caracteristicas correspondientes a las columnas: nombres, tipo de datos y extensión
        cursor.execute("CREATE TABLE proyecto (id VARCHAR (3), products VARCHAR(100), brands VARCHAR(15), seller VARCHAR(20), amount FLOAT(12), price FLOAT(12), total_pricefin FLOAT(20))")
        print("La tabla ha sido creada....")
        #iterar cada fila del archivo csv
        for i,row in empdata.iterrows():
            #%s significa completar cada columna con los valores del DF
            sql = "INSERT INTO dbproyecto.proyecto VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Registro insertado")
            # Confirma para guardar los cambios
            conn.commit()
except Error as e:
            print("Error al conectar MySQL", e)

#Se exporta un archivo XLXS a la ruta que elijan:
finaldf.to_excel("C:/Users/angel/PROYECTO INTEGRADOR D1006/D1006/report.xlsx", index=None, header=True)

