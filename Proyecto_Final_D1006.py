'''
Pasos previos a iniciar el código:
INSTALAR LIBRERIAS BEATIFULSOUP y LXML
En la terminal:

pip install beautifulsoup4
pip install lxml
'''

''' El trabajo se va a realizar descargando los archivos HTML que se subiran complementariamente al repositorio para probar el trabajo de web scraping'''

from bs4 import BeautifulSoup

import glob

#MODIFICAR EL NOMBRE DEL ARCHIVO CON LA RUTA:
datos = []
product1 = []
brand1 = []
seller1 = []
#financial_mode1 = [] todas dicen 18 cuotas así que no es relevante
financing_amount1 = []
#price1 = [] al final el precio termina siendo el de sale price
sale_price1 = []

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

        datos.append({"product": product, "brand": brand, "seller": seller, "financial_mode": financial_mode,"financing_amount": financing_amount, "price": price, "sale_price": sale_price})
        #datos.append({product, brand, seller, financial_mode, financing_amount, price, sale_price})
        product1.append(product)
        brand1.append(brand)
        seller1.append(seller)
        #financial_mode1.append(financial_mode)
        financing_amount1.append(financing_amount)
        #price1.append(price)
        sale_price1.append(sale_price)

#print(product1)


import pandas as pd

dict = {'product': product1, 'brand': brand1, 'seller': seller1, 'financing_amount': financing_amount1,'sale_price': sale_price1}
df = pd.DataFrame((dict), index=list(range(len(product1))))
df.to_csv('database.csv')

#print(df)

empdata = pd.read_csv('C:/Users/angel/PROYECTO INTEGRADOR D1006/D1006/.ipynb_checkpoints/database.csv', index_col=False, delimiter = ',')
empdata.head()

#print(empdata)

import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', user='root',  
                        password='adolfito06')#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE dbproyecto")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)

import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', database='dbproyecto', user='root', password='adolfito06')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS dbproyecto;')
        print('Creating table....')
# in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE proyecto (id VARCHAR (3), products VARCHAR(100), brands VARCHAR(15), seller VARCHAR(20), amount FLOAT(12), price FLOAT(12))")
        print("Table is created....")
        #loop through the data frame
        for i,row in empdata.iterrows():
            #here %S means string values 
            sql = "INSERT INTO dbproyecto.proyecto VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)