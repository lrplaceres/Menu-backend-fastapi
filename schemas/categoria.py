from pydantic import BaseModel

# Create Categoria Schema (Pydantic Model)
class CategoriaCreate(BaseModel):
    nombre: str
    establecimiento_id: int
    
# Complete Categoria Schema (Pydantic Model)
class Categoria(BaseModel):
    id: int
    nombre: str
    establecimiento_id: int