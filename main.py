from typing import Optional

from fastapi import FastAPI, Request
from fastapi.logger import logger 
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import logging
import sys
import os 

class Item(BaseModel):
    item_id: int
    name: Optional[str] = None

app = FastAPI()

#logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)

root_logger = logging.getLogger()
if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    gunicorn_logger = logging.getLogger("gunicorn")

    root_logger.setLevel(gunicorn_logger.level)
    root_logger.handlers = gunicorn_error_logger.handlers

    uvicorn_logger = logging.getLogger("uvicorn.access")
    uvicorn_logger.handlers = gunicorn_error_logger.handlers
else:
    # https://github.com/tiangolo/fastapi/issues/2019
    LOG_FORMAT2 = "%(asctime)s | %(levelname)s | %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT2)

root_logger = logging.getLogger()
print('+ [%s] {%s} ' % (str.ljust( "RootLogger", 20)  , str(root_logger.__class__)[8:-2]) )
for h in root_logger.handlers:
    print('     +++',str(h.__class__)[8:-2] )
for k,v in  logging.Logger.manager.loggerDict.items()  :
        print('+ [%s] {%s} ' % (str.ljust( k, 20)  , str(v.__class__)[8:-2]) ) 
        if not isinstance(v, logging.PlaceHolder):
            for h in v.handlers:
                print('     +++',str(h.__class__)[8:-2] )

items = {"count":1}

@app.on_event("startup")
async def startup_event():
    ...

@app.get("/", response_class=RedirectResponse)
def redirect_docs():
    url = app.url_path_for("swagger_ui_html")
    return url

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "name": q}

@app.get("/items/random/random", response_model=Item)
def get_random_item():
    return {"item_id":1}

@app.get('/list_endpoints/', description="Get all endpoints")
def list_endpoints(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list

@app.get('/get_count', response_model=Item)
def get_count():
    return {"item_id": items["count"]}

@app.post('/add_count', response_model=Item)
def add_count():
    items["count"] += 1
    return {"item_id": items["count"]}


