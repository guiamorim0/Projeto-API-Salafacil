from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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
