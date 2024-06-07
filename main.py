import uvicorn
from fastapi import FastAPI
from langserve import add_routes
from core.app.llm.generator import generator
from core.app.api.schemas import UserRegisterSchema
from core.app.api.controllers import CoreController

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"

)

add_routes(
    app,
    generator,
    path='/test'
)


@app.post('/register', response_description='User Registeration')
def register(params: UserRegisterSchema):
    return CoreController().register(params)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8012)
