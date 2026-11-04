from sqlalchemy import Integer, String, Boolean, ForeignKey, Date, Column
from sqlalchemy.orm import relationship
from database import base

class Sala(base):
    __tablename__ = 'salas'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    nome = Column(String)
    capacidade = Column(Integer)
    ativa = Column(
        Boolean,
        default=True
    )
    reservas = relationship("Reserva", back_populates="sala", cascade="all, delete-orphan")

class Reserva(base):
    __tablename__ = 'reservas'
    id = Column(
        Integer, 
        primary_key=True,
        index=True
    )
    sala_id = Column(
        Integer,
        ForeignKey('salas.id')
    )
    responsavel = Column(String)
    data = Column(Date)
    quantidade_pessoas = Column(Integer) 
    sala = relationship("Sala", back_populates="reservas")