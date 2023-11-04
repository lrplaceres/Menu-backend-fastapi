from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database.database import Base, engine
import schemas.municipio
import models.models

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()

@router.post("/municipio", response_model=schemas.municipio.Municipio, status_code=status.HTTP_201_CREATED, tags=["municipio"])
async def create_municipio(municipio: schemas.municipio.MunicipioCreate):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    municipiodb = models.models.Municipio(nombre = municipio.nombre, orden = municipio.orden, provincia_id = municipio.provincia_id)

    # add it to the session and commit it
    session.add(municipiodb)
    session.commit()
    session.refresh(municipiodb)

    # close the session
    session.close()

    # return the todo object
    return municipiodb

@router.get("/municipio/provincia/{id}", tags=["municipio"])
async def read_municipio_provincia(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the municipio item with the given id
    municipiodb = session.query(models.models.Municipio).filter(models.models.Municipio.provincia_id == id).all()

    # close the session
    session.close()

    if not municipiodb:
        raise HTTPException(status_code=404, detail=f"municipio item with id {id} not found")

    return municipiodb

@router.get("/municipio/{id}", tags=["municipio"])
async def read_municipio(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the municipio item with the given id
    municipiodb = session.query(models.models.Municipio).get(id)

    # close the session
    session.close()

    if not municipiodb:
        raise HTTPException(status_code=404, detail=f"municipio item with id {id} not found")

    return municipiodb

@router.put("/municipio/{id}", tags=["municipio"])
async def update_municipio(id: int, nombre: str, orden: str, provincia_id: int | None = None):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the provincia item with the given id
    municipiodb: schemas.municipio.Municipio = session.query(models.models.Municipio).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if municipiodb:
        municipiodb.nombre = nombre
        municipiodb.orden = orden
        municipiodb.provincia_id = provincia_id
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not municipiodb:
        raise HTTPException(status_code=404, detail=f"municipio item with id {id} not found")

    return municipiodb

@router.delete("/municipio/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["municipio"])
async def delete_municipio(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    municipiodb = session.query(models.models.Municipio).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if municipiodb:
        session.delete(municipiodb)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"municipio item with id {id} not found")

    return None
