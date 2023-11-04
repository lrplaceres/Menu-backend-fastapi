from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database.database import Base, engine
import schemas.establecimiento
import models.models

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()

@router.get("/establecimiento", response_model = List[schemas.establecimiento.Establecimiento], tags=["establecimiento"])
def read_establecimiento_list(start: int = 0, limit: int = 10):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all todo items
    establecimientodb_list = session.query(models.models.Establecimiento).offset(start).limit(limit).all()

    # close the session
    session.close()

    return establecimientodb_list

@router.post("/establecimiento", response_model=schemas.establecimiento.Establecimiento, status_code=status.HTTP_201_CREATED, tags=["establecimiento"])
async def create_establecimiento(establecimiento: schemas.establecimiento.EstablecimientoCreate):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    establecimientodb = models.models.Establecimiento(nombre = establecimiento.nombre, contacto = establecimiento.contacto, direccion = establecimiento.direccion, facebook = establecimiento.facebook, instagram = establecimiento.instagram,municipio_id = establecimiento.municipio_id, geolocalizacion = establecimiento.geolocalizacion)

    # add it to the session and commit it
    session.add(establecimientodb)
    session.commit()
    session.refresh(establecimientodb)

    # close the session
    session.close()

    # return the todo object
    return establecimientodb

@router.get("/establecimiento/{id}", tags=["establecimiento"])
async def read_establecimiento(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the establecimiento item with the given id
    establecimientodb = session.query(models.models.Establecimiento).get(id)

    # close the session
    session.close()

    if not establecimientodb:
        raise HTTPException(status_code=404, detail=f"establecimiento item with id {id} not found")

    return establecimientodb

@router.put("/establecimiento/{id}", tags=["establecimiento"])
async def update_establecimiento(id: int, nombre: str, contacto: str|None = None, direccion: str|None = None, facebook: str|None = None, instagram: str|None = None, municipio_id: int|None = None, geolocalizacion: str|None = None):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the provincia item with the given id
    establecimientodb: schemas.establecimiento.Establecimiento = session.query(models.models.Establecimiento).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if establecimientodb:
        establecimientodb.nombre = nombre
        establecimientodb.direccion = direccion
        establecimientodb.facebook = facebook
        establecimientodb.instagram = instagram
        establecimientodb.municipio_id = municipio_id
        establecimientodb.geolocalizacion = geolocalizacion
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not establecimientodb:
        raise HTTPException(status_code=404, detail=f"establecimiento item with id {id} not found")

    return establecimientodb

@router.delete("/establecimiento/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["establecimiento"])
async def delete_establecimiento(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    establecimientodb = session.query(models.models.Establecimiento).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if establecimientodb:
        session.delete(establecimientodb)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"establecimiento item with id {id} not found")

    return None






















