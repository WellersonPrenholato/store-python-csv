import csv
import os
from dotenv import load_dotenv
from functions import convert_csv_to_json

load_dotenv()

path_database = os.environ["DATABASE"]


def list_items_all():
    return convert_csv_to_json(path_database)

def list_item_id():
    return True

def create_item():
# with open(path_database, 'w', newline='') as file:
    
#     writer = csv.writer(file)
    
#     writer.writerow(["Id", "Pressao", "Temperatura", "Umidade"])
#     writer.writerow([1, 15.6, 20.1, 30.3])       
#     writer.writerow([2, 16.3, 19.8, 27.1])          
#     writer.writerow([3, 15.3, 20.2, 28.3])          
#     writer.writerow([4, 16.1, 20.5, 27.7])        
#     writer.writerow([5, 15.8, 19.7, 29.2])

    return True

def delete_item():
    
    return True