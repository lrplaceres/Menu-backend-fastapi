from fastapi import APIRouter, status, HTTPException, UploadFile, Form
from typing import List, Annotated
from sqlalchemy.orm import Session
from database.database import Base, engine
import schemas.producto
import models.models
import os
import shutil

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()

@router.post("/producto", response_model=schemas.producto.Producto, status_code=status.HTTP_201_CREATED, tags=["producto"])
async def create_producto(nombre: Annotated[str, Form()], activo:Annotated[bool, Form()], foto: UploadFile, categoria_id:Annotated[int, Form()],establecimiento_id:Annotated[int, Form()], descripcion:Annotated[str|None, Form()]=None, precio:Annotated[float|None, Form()]=None, moneda:Annotated[str|None, Form()]=None):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    productodb = models.models.Producto(nombre = nombre, descripcion = descripcion, precio = precio, moneda = moneda, categoria_id = categoria_id, establecimiento_id = establecimiento_id, foto = foto.filename, activo = activo)

    # add it to the session and commit it
    session.add(productodb)
    session.commit()
    session.refresh(productodb)

    destino = os.getcwd() + f"/public/{productodb.establecimiento_id}/{productodb.id}"
    os.mkdir(destino)
    try:
        with open(destino + f"/{foto.filename}", "wb+") as file_object:
            shutil.copyfileobj(foto.file, file_object)
    finally:
        foto.file.close()

    # close the session
    session.close()

    # return the todo object
    return productodb

@router.get("/producto/{id}", tags=["producto"])
async def read_producto(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the establecimiento item with the given id
    productodb = session.query(models.models.Producto).get(id)

    # close the session
    session.close()

    if not productodb:
        raise HTTPException(status_code=404, detail=f"producto item with id {id} not found")

    return productodb

@router.put("/producto/{id}", tags=["producto"])
async def update_producto(id: int, nombre: Annotated[str, Form()], activo:Annotated[bool, Form()], foto: UploadFile, categoria_id:Annotated[int, Form()],establecimiento_id:Annotated[int, Form()], descripcion:Annotated[str|None, Form()]=None, precio:Annotated[float|None, Form()]=None, moneda:Annotated[str|None, Form()]=None):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the provincia item with the given id
    productodb: schemas.producto.Producto = session.query(models.models.Producto).get(id)

    destino = os.getcwd() + f"/public/{productodb.establecimiento_id}/{productodb.id}"
    os.remove(destino + f"/{productodb.foto}")

    # update todo item with the given task (if an item with the given id was found)
    if productodb:
        productodb.nombre = nombre
        productodb.activo = activo
        productodb.foto = foto.filename
        productodb.descripcion = descripcion
        productodb.precio = precio
        productodb.moneda = moneda
        productodb.categoria_id = categoria_id
        productodb.establecimiento_id = establecimiento_id
        session.commit()

    # close the session
    session.close()

    try:
        with open(destino + f"/{foto.filename}", "wb+") as file_object:
            shutil.copyfileobj(foto.file, file_object)           
    finally:
        foto.file.close()


    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not productodb:
        raise HTTPException(status_code=404, detail=f"producto item with id {id} not found")

    return productodb

@router.delete("/producto/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["producto"])
async def delete_producto(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    productodb = session.query(models.models.Producto).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if productodb:
        session.delete(productodb)
        session.commit()
        session.close()

        destino = os.getcwd() + f"/public/{productodb.establecimiento_id}/{productodb.id}"
        shutil.rmtree(destino)
    else:
        raise HTTPException(status_code=404, detail=f"producto item with id {id} not found")

    return None


























