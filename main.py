import uvicorn
from fastapi import FastAPI
from langserve import add_routes
from app.generator import generator

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




if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8012)
