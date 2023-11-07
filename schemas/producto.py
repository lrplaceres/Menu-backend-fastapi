from pydantic import BaseModel

# Create Producto Schema (Pydantic Model)
class ProductoCreate(BaseModel):
    nombre: str
    foto: str
    descripcion: str|None
    precio: float|None
    moneda: str|None
    categoria_id: int
    establecimiento_id: int
    activo: bool
    
# Complete Producto Schema (Pydantic Model)
class Producto(BaseModel):
    id: int
    nombre: str
    foto: str
    descripcion: str|None
    precio: float|None
    moneda: str|None
    categoria_id: int
    establecimiento_id: int
    activo: bool