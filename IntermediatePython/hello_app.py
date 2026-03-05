from fastapi import FastAPI

app = FastAPI()

#GET
@app.get("/")
def root():
    return {"message":"Hello World NBA"}
