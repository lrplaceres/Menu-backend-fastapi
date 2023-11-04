from pydantic import BaseModel

# Create Provincia Schema (Pydantic Model)
class ProvinciaCreate(BaseModel):
    nombre: str
    orden: int
    
# Complete Provincia Schema (Pydantic Model)
class Provincia(BaseModel):
    id: int
    nombre: str
    orden: int