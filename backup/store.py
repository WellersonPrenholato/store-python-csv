import csv
import os
from dotenv import load_dotenv
from model import Item

load_dotenv()

path_database = os.environ["DATABASE"]


class Store:
    
    def list_items_all(self):
        data = {"Items":[]}
        
        with open(path_database, encoding='utf-8') as csvf:
            csv_reader = csv.DictReader(csvf)

            for rows in csv_reader:
                data['Items'].append(rows)

        return data


    def list_item_id(self):
        data = {
            "Items":{
                "nome":[],
                "marca":[],
                "codigo":[]
            }
        }
        with open(path_database) as csv_file:
        
            csv_reader = csv.reader(csv_file, delimiter=';')

            csv_reader.__next__()

            for row in csv_reader:
                # print( row[0] + ', ' + row[1] + ', ' + row[2] )
                data['Items']['nome'].append(row[0])
                data['Items']['marca'].append(row[1])
                data['Items']['codigo'].append(row[2])

            return data
        
        