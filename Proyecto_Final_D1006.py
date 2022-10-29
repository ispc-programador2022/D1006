'''
Pasos previos a iniciar el código:
INSTALAR LIBRERIAS BEATIFULSOUP y LXML
En la terminal:

pip install beautifulsoup4
pip install lxml
'''

''' El trabajo se va a realizar descargando los archivos HTML que se subiran complementariamente al repositorio para probar el trabajo de web scraping'''

from bs4 import BeautifulSoup

#MODIFICAR EL NOMBRE DEL ARCHIVO CON EL NOMBRE FINAL DEL MISMO:
with open('NOMBRE DEL ARCHIVO HTML LOCAL', 'r', encoding="utf-8") as html_file:
     content = html_file.read()

soup = BeautifulSoup(content, 'lxml')
