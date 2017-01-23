import csv 
import psycopg2
import sys

file_path = 

with open(/osnap_legacy/DC_inventory.csv) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['asset tag'], row['product'], row['intake date'])

print(row)
