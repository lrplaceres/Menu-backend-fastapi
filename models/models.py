from sqlalchemy import Column, Integer, String, ForeignKey, Float
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

# Define Provincia class inheriting from Base
class Provincia(Base):
    __tablename__ = 'provincia'
    id: Mapped[int] = Column(Integer, primary_key=True)
    nombre: Mapped[str]= Column(String(256))
    orden: Mapped[int] = Column(Integer)

    municipios: Mapped[int|None] = relationship("Municipio", back_populates="provincia")


class Municipio(Base):
    __tablename__ = 'municipio'
    id: Mapped[int] = Column(Integer, primary_key=True)
    nombre: Mapped[str] = Column(String(256))
    orden: Mapped[int] = Column(Integer)
    provincia_id: Mapped[int|None] = Column(Integer, ForeignKey("provincia.id"))

    provincia: Mapped[int] = relationship("Provincia", back_populates = "municipios")


class Establecimiento(Base):
    __tablename__ = 'establecimiento'
    id: Mapped[int] = Column(Integer, primary_key=True)
    nombre: Mapped[str] = Column(String(256))
    contacto: Mapped[str|None] = Column(String(256))
    direccion: Mapped[str|None] = Column(String(256))
    instagram: Mapped[str|None] = Column(String(256))
    facebook: Mapped[str|None] = Column(String(256))
    municipio_id: Mapped[int] = Column(Integer)
    geolocalizacion: Mapped[str|None] = Column(String(256))

    categorias: Mapped[int|None] = relationship("Categoria", back_populates="establecimiento")
    productos: Mapped[int|None] = relationship("Producto", back_populates="establecimiento")


class Categoria(Base):
    __tablename__ = 'categoria'
    id: Mapped[int] = Column(Integer, primary_key=True)
    nombre: Mapped[str] = Column(String(256))
    establecimiento_id: Mapped[int] = Column(Integer, ForeignKey("establecimiento.id"))

    establecimiento: Mapped[int] = relationship("Establecimiento", back_populates = "categorias")
    productos: Mapped[int] = relationship("Productos", back_populates="categoria")


class Producto(Base):
    __tablename__ = 'producto'
    id: Mapped[int] = Column(Integer, primary_key=True)
    nombre: Mapped[str] = Column(String(256))
    descripcion: Mapped[str|None] = Column(String(256))
    precio: Mapped[float] = Column(Float)
    categoria_id : Mapped[int] = Column(Integer, ForeignKey("categoria.id"))
    establecimiento_id: Mapped[int] = Column(Integer, ForeignKey("establecimiento.id"))

    categoria: Mapped[int] = relationship("Categoria", back_populates = "productos")
    establecimiento: Mapped[int] = relationship("Establecimiento", back_populates = "productos")