from pydantic import BaseModel

# Create Producto Schema (Pydantic Model)
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: int
    establecimiento: int
    
# Complete Producto Schema (Pydantic Model)
class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str|None
    precio: float
    categoria: int
    establecimiento: int