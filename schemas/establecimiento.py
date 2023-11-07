from pydantic import BaseModel

# Create Establecimiento Schema (Pydantic Model)
class EstablecimientoCreate(BaseModel):
    nombre: str
    foto: str|None
    contacto: str|None
    direccion: str|None
    facebook: str|None
    instagram: str|None
    municipio_id: int|None
    geolocalizacion: str|None
    
# Complete Establecimiento Schema (Pydantic Model)
class Establecimiento(BaseModel):
    id: int
    nombre: str
    foto: str|None
    contacto: str|None
    direccion: str|None
    facebook: str|None
    instagram: str|None
    municipio_id: int|None
    geolocalizacion: str|None