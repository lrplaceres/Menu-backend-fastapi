from fastapi import APIRouter, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database.database import Base, engine
import schemas.categoria
import models.models

# Create the database
Base.metadata.create_all(engine)

router = APIRouter()


@router.post("/categoria", response_model=schemas.categoria.Categoria, status_code=status.HTTP_201_CREATED, tags=["categoria"])
async def create_categoria(categoria: schemas.categoria.CategoriaCreate):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    categoriadb = models.models.Categoria(nombre = categoria.nombre, establecimiento_id = categoria.establecimiento_id)

    # add it to the session and commit it
    session.add(categoriadb)
    session.commit()
    session.refresh(categoriadb)

    # close the session
    session.close()

    # return the todo object
    return categoriadb

@router.get("/categoria/{id}", tags=["categoria"])
async def read_categoria(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the establecimiento item with the given id
    categoriadb = session.query(models.models.Categoria).get(id)

    # close the session
    session.close()

    if not categoriadb:
        raise HTTPException(status_code=404, detail=f"categoria item with id {id} not found")

    return categoriadb

  
@router.put("/categoria/{id}", tags=["categoria"])
async def update_categoria(id: int, nombre: str):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the provincia item with the given id
    categoriadb: schemas.categoria.Categoria = session.query(models.models.Categoria).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if categoriadb:
        categoriadb.nombre = nombre
        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not categoriadb:
        raise HTTPException(status_code=404, detail=f"categoria item with id {id} not found")

    return categoriadb

@router.delete("/categoria/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["categoria"])
async def delete_categoria(id: int):
    
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    categoriadb = session.query(models.models.Categoria).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if categoriadb:
        session.delete(categoriadb)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"categoria item with id {id} not found")

    return None

