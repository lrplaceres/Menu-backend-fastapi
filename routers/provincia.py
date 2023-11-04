from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database.database import Base, engine
import schemas.provincia
import models.models

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()

@router.get("/provincia", response_model = List[schemas.provincia.Provincia], tags=["provincia"])
def read_provincia_list(start: int = 0, limit: int = 10):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all todo items
    provinciadb_list = session.query(models.models.Provincia).offset(start).limit(limit).all()

    # close the session
    session.close()

    return provinciadb_list

@router.get("/provincia/{id}", tags=["provincia"])
async def read_provincia(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the provincia item with the given id
    provinciadb = session.query(models.models.Provincia).get(id)

    # close the session
    session.close()

    if not provinciadb:
        raise HTTPException(status_code=404, detail=f"provincia item with id {id} not found")

    return provinciadb
    
@router.post("/provincia", response_model=schemas.provincia.Provincia, status_code=status.HTTP_201_CREATED, tags=["provincia"])
async def create_provincia(provincia: schemas.provincia.ProvinciaCreate):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    provinciadb = models.models.Provincia(nombre = provincia.nombre, orden = provincia.orden)

    # add it to the session and commit it
    session.add(provinciadb)
    session.commit()
    session.refresh(provinciadb)

    # close the session
    session.close()

    # return the todo object
    return provinciadb

@router.put("/provincia/{id}", tags=["provincia"])
async def update_provincia(id: int, nombre: str, orden: str):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the provincia item with the given id
    provinciadb: schemas.provincia.Provincia = session.query(models.models.Provincia).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if provinciadb:
        provinciadb.nombre = nombre
        provinciadb.orden = orden
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not provinciadb:
        raise HTTPException(status_code=404, detail=f"provincia item with id {id} not found")

    return provinciadb

@router.delete("/provincia/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["provincia"])
async def delete_provincia(id: int):
        
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    provinciadb = session.query(models.models.Provincia).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if provinciadb:
        session.delete(provinciadb)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"provincia item with id {id} not found")

    return None















