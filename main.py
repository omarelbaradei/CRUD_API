from fastapi import FastAPI

# a static memory for storing app's data

memory=[{"id":1,"title":"get a job","done":False},{"id":2,"title":"get a house","done":False},{"id":3,"title":"buy a car","done":True}]

#create a fastapi object
app = FastAPI()

#define an initial homepage loading response

@app.get("/",description="Show your homepage")
async def root():
    return {
        "name":"Task API",
        "version":"1.0",
        "endpoints":"/tasks",
        "message": "Hello World"}

# define an initial health page loading response

@app.get("/health",description="Go to health page")
async def get_health():
    return {"status":"ok"}

