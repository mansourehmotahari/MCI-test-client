from fastapi import FastAPI
import random
import uvicorn
from pydantic import BaseModel
from fastapi.responses import JSONResponse

class GroupRequest(BaseModel):
    groupId: str 

app = FastAPI()

group_data = {}

@app.post("/v1/group")
def create(data: GroupRequest):
    global group_data
    number = random.randint(1, 10)
    result = number > 2
    if result:
        group_data[data.groupId] = True
        return JSONResponse(
            content={
                "result": result},
            status_code=201
        )
    else:
        return JSONResponse(
                content={
                    "error": "Perhaps the object exists"},
                status_code=400
            )


@app.delete("/v1/group")
def delete(data: GroupRequest):
    try:
        del group_data[data.groupId]
        return JSONResponse(
            content={"result": "ok :)"},
            status_code=200
        )
    except KeyError:
        return JSONResponse(
            content={"result": "not found"},
            status_code=404
        )


@app.get("/v1/group/{groupId}")
def get_id(groupId: str):
    try:
        group = group_data[groupId]
        return JSONResponse(
            content={"result": f"found groupId: {groupId}"},
            status_code=200
        )
    except KeyError:
        return JSONResponse(
            content={"result": "not found"},
            status_code=404)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)