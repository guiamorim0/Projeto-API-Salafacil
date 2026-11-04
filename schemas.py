from pydantic import BaseModel
from datetime import date

class SalaBase(BaseModel):
    nome: str
    capacidade: int

class SalaCreate(SalaBase):
    pass

class SalaResponse(SalaBase):
    id: int
    ativa: bool
    class Config:
        from_attributes = True

class ReservaBase(BaseModel):
    sala_id: int
    responsavel: str
    data: date
    quantidade_pessoas: int

class ReservaCreate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id: int
    class Config:
        from_attributes = True

class SalaComReservas(SalaResponse):
    reservas: list[ReservaResponse] = []