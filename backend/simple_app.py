from fastapi import FastAPI

app = FastAPI(title="Baseball Betting Simulator")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Baseball Betting Simulator API is running"}