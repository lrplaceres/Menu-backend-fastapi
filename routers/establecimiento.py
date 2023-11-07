from fastapi import APIRouter, status, HTTPException, UploadFile, Form
from typing import List, Annotated
from sqlalchemy.orm import Session
from database.database import Base, engine
import schemas.establecimiento
import models.models
import os
import shutil

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
async def create_establecimiento(nombre:Annotated[str, Form()], activo:Annotated[bool, Form()], foto: UploadFile, contacto:Annotated[str|None, Form()]=None, direccion:Annotated[str|None, Form()]=None, facebook:Annotated[str|None, Form()]=None, instagram:Annotated[str|None, Form()] = None, municipio_id:Annotated[str|None, Form()]=None, geolocalizacion:Annotated[str|None, Form()]=None):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    establecimientodb = models.models.Establecimiento(nombre = nombre, contacto = contacto, direccion = direccion, facebook = facebook, instagram = instagram, municipio_id = municipio_id, geolocalizacion = geolocalizacion, foto = foto.filename, activo = activo)
    
    # add it to the session and commit it
    session.add(establecimientodb)
    session.commit()
    session.refresh(establecimientodb)

    destino = os.getcwd() + f"/public/{establecimientodb.id}"
    os.mkdir(destino)
    try:
        with open(destino + f"/{foto.filename}", "wb+") as file_object:
            shutil.copyfileobj(foto.file, file_object)
    finally:
        foto.file.close()

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
async def update_establecimiento(id: int, nombre:Annotated[str, Form()], activo:Annotated[bool, Form()], foto: UploadFile, contacto:Annotated[str|None, Form()]=None, direccion:Annotated[str|None, Form()]=None, facebook:Annotated[str|None, Form()]=None, instagram:Annotated[str|None, Form()] = None, municipio_id:Annotated[str|None, Form()]=None, geolocalizacion:Annotated[str|None, Form()]=None):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the provincia item with the given id
    establecimientodb: schemas.establecimiento.Establecimiento = session.query(models.models.Establecimiento).get(id)

    destino = os.getcwd() + f"/public/{establecimientodb.id}"
    os.remove(destino + f"/{establecimientodb.foto}")
            
    # update todo item with the given task (if an item with the given id was found)
    if establecimientodb:
        establecimientodb.nombre = nombre
        establecimientodb.activo = activo
        establecimientodb.direccion = direccion
        establecimientodb.foto = foto.filename
        establecimientodb.facebook = facebook
        establecimientodb.instagram = instagram
        establecimientodb.municipio_id = municipio_id
        establecimientodb.geolocalizacion = geolocalizacion
        session.commit()

    # close the session
    session.close()

    try:
        with open(destino + f"/{foto.filename}", "wb+") as file_object:
            shutil.copyfileobj(foto.file, file_object)           
    finally:
        foto.file.close()

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

        destino = os.getcwd() + f"/public/{establecimientodb.id}"
        shutil.rmtree(destino)

    else:
        raise HTTPException(status_code=404, detail=f"establecimiento item with id {id} not found")

    return None


