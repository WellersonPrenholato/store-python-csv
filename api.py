from fastapi import FastAPI
from main import list_items_all, list_item_id

app = FastAPI()


@app.get("/items")
def get_items_all():
    return list_items_all()

@app.get("/item/{id}")
def get_item_id():
    return list_item_id()
