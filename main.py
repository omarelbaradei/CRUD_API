from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
from typing import Optional
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

# define a basic templete to insure input suffice all requirements 

class taskcreate(BaseModel):

    title:str


# define a functionality of adding a new task to the memory list 

@app.post("/tasks",status_code=status.HTTP_201_CREATED,description="Add a new task")

def add_task(task:taskcreate):

    global next_id  # call global id variable  

    clean_title=task.title.strip()  # trim the inputed title from any extra spaces at the start or end

    if not clean_title:             # insure that the title is still present after trimming

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you should provide the title of the task to be accepted !")             # raise an error if the title was invalid in any case

    new_task={'id':next_id,"title":clean_title,"done":False}

    next_id+=1                                                                 
                                                            # adds the new task to memory list
    memory.append(new_task)

    return new_task

# define a basic templete to insure input suffice all requirements

class taskupdate(BaseModel):
    title:Optional[str]=None
    done:Optional[bool]=None


# define a functionality of updating existing task's title or done status 

@app.put("/tasks/{task_id}",status_code=status.HTTP_201_CREATED,description="Update exciting tasks")
def update_task(task_id:int,task:taskupdate):

    update=None    # a variable refers to updated task

    for cell in memory:

        if cell["id"]==task_id:

            update=cell

            break   

    if update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"invalid id")

    if task.title is None and  task.done is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="no title or done entered")


    if task.title is not None:
        clean_title=task.title.strip()
        if not clean_title: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="title not provided")
        update["title"]=clean_title

    if task.done is not None:
        update["done"]=task.done

    return update


# define a functionality to delete a certain task in memory

@app.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT,description="Delete exicting tasks")
def delete_task(task_id:int):
    for i,task in enumerate(memory):
        if task["id"]==task_id:
            memory.pop(i)
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid id")  

