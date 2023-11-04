from pydantic import BaseModel

# Create Municipio Schema (Pydantic Model)
class MunicipioCreate(BaseModel):
    nombre: str
    orden: int
    provincia_id: int
    
# Complete Municipio Schema (Pydantic Model)
class Municipio(BaseModel):
    id: int
    nombre: str
    orden: int
    provincia_id: int