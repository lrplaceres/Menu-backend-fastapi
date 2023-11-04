from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database.database import Base, engine
import schemas.producto
import models.models

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()

@router.post("/producto", response_model=schemas.producto.Producto, status_code=status.HTTP_201_CREATED, tags=["producto"])
async def create_producto(producto: schemas.producto.Producto):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    productodb = models.models.Producto(nombre = producto.nombre, descripcion = producto.descripcion, precio = producto.precio, categoria = producto.categoria, establecimiento = producto.establecimiento)

    # add it to the session and commit it
    session.add(productodb)
    session.commit()
    session.refresh(productodb)

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
async def update_producto(id: int, nombre: str, precio: float, categoria: int, establecimiento: int, descripcion: str|None = None):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the provincia item with the given id
    productodb: schemas.producto.Producto = session.query(models.models.Producto).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if productodb:
        categoriadb.nombre = nombre
        categoriadb.descripcion = descripcion
        categoriadb.precio = precio
        categoriadb.categoria = categoria
        categoriadb.establecimiento = establecimiento
        session.commit()

    # close the session
    session.close()

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
    else:
        raise HTTPException(status_code=404, detail=f"producto item with id {id} not found")

    return None


























