from fastapi import FastAPI

app = FastAPI()

#GET Return Greeting
@app.get("/")
def root():
    return {"status":"ok"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id" : item_id}
