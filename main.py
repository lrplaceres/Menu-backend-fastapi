from fastapi import FastAPI
from routers import provincia, municipio, establecimiento, categoria, producto

app = FastAPI()

app.include_router(provincia.router)
app.include_router(municipio.router)
app.include_router(establecimiento.router)
app.include_router(categoria.router)
app.include_router(producto.router)

@app.get("/")
def index():
    return {"mensaje": "Inicio"}











