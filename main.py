from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
import models
import schemas
from database import session_local, engine

models.base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post(
        '/salas/',
        response_model=schemas.SalaResponse)
def cadastro_salas(
    sala: schemas.SalaCreate,
    db: Session = Depends(get_db)):
    db_sala = models.Sala(**sala.model_dump())
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala

@app.get(
    '/salas/',
    response_model= List[schemas.SalaResponse])
def listar_salas(capacidade_minima: int | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Sala)
    if capacidade_minima is not None:
        query = query.filter(models.Sala.capacidade >= capacidade_minima)
    return query.all()

@app.get(
    '/salas/{sala_id}',
    response_model= schemas.SalaResponse)
def ler_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).filter(models.Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala nao encontrada!")
    return sala

@app.put(
    '/salas/{sala_id}/desativar',
    response_model= schemas.SalaResponse)
def put_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).filter(models.Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala nao encontrada!")

    if not sala.ativa:
        raise HTTPException(status_code=400, detail="Essa sala ja esta desativada!")

    sala.ativa = False
    db.commit()
    db.refresh(sala)
    return sala

@app.delete('/salas/{sala_id}')
def delete_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).filter(models.Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala nao encontrada")
    db.delete(sala)
    db.commit()
    return {"mensagem":"Sala removida com sucesso!"}

@app.post(
    '/reservas/',
    response_model= schemas.ReservaResponse)
def cadastro_reservas(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).filter(models.Sala.id == reserva.sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala nao encontrada")

    if not sala.ativa:
        raise HTTPException(status_code=400, detail="Essa sala ja esta desativada!")

    if reserva.quantidade_pessoas > sala.capacidade:
        raise HTTPException(status_code=400, detail="Capacidade excedida")

    reserva_existente = db.query(models.Reserva).filter(models.Reserva.sala_id == reserva.sala_id, models.Reserva.data == reserva.data).first()

    if reserva_existente:
        raise HTTPException(status_code=400, detail="Sala ja reservada nesse dia")

    db_reserva = models.Reserva(**reserva.model_dump())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

@app.get(
    '/reservas/',
    response_model=List[schemas.ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    query = db.query(models.Reserva)
    return query.all()

@app.delete('/reservas/{reserva_id}')
def excluir_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva nao encontrada")
    db.delete(reserva)
    db.commit()
    return {"mensagem":"reserva removida com sucesso!"}

@app.get(
    '/salas/{sala_id}/reservas',
    response_model=schemas.SalaComReservas)
def sala_reservas(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).options(joinedload(models.Sala.reservas)).filter(models.Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala nao encontrada")
    return sala 