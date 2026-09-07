from fastapi import FastAPI,HTTPException,status

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

# define an initial tasks page loading response

@app.get("/tasks",description="show all saved tasks")
def get_tasks():

    return memory            # return all tasks in memory list 


# define a functionality in tasks page which is the ability to fetch any task in memory by providing its id

@app.get("/tasks/{id}",status_code=status.HTTP_200_OK,description="Show specific task")  # specify that id have to be passed in the path parameters

def get_task(id:int):
    for task in memory:     # loop through the memory list
        if task['id']==id:  # try to fetch and return task from memory 
            return task
    raise HTTPException(status_code=404,detail=f"task {id} not found 404")  # raise an error message when the task is not present in memory


