import csv
with open('C:/Users/angel/PROYECTO INTEGRADOR D1006/D1006/database.csv', encoding="utf8", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|', )
    for row in spamreader:
        print(', '.join(row))
