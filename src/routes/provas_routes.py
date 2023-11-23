from fastapi import APIRouter
from src.models.provas_model import Provas
from src.config.database import get_session

provas_router = APIRouter(prefix="/provas")


@provas_router.post("")
def cria_prova(prova: Provas):
    with get_session() as session:
        # Validar se existe uma prova com a mesma descrição e com a mesma data

        statement = select(Provas).where(
            and_(Provas.descricao == prova.descricao, Provas.data_prova == prova.data_prova)
        )
        prova_db = session.exec(statement).first()
        if prova_db:
            return {"status": "error", "message": "Prova já cadastrada."}

        session.add(prova)
        session.commit()
        session.refresh(prova)
        return prova


@provas_router.get("")
async def get_provas():
    with get_session() as session:
        statement = select(Provas)
        provas = session.exec(statement).all()
        return provas


@provas_router.get("/:prova_id")
async def get_provas_by_id(prova_id: int):
    with get_session() as session:
        statement = select(Provas).where(Provas.id == prova_id)
        prova = session.exec(statement).first()
        if prova:
            return prova
        else:
            return {"status": "error", "message": "Prova não encontrada"}


@provas_router.patch("/:id")
async def update_prova(id: int, prova: Provas):
    with get_session() as session:
        prova_db = session.get(Provas, id)
        if prova_db:
            prova_db.descricao = prova.descricao
            prova_db.data_prova = prova.data_prova
            prova_db.q1 = prova.q1
            prova_db.q2 = prova.q2
            prova_db.q3 = prova.q3
            prova_db.q4 = prova.q4
            prova_db.q5 = prova.q5
            prova_db.q6 = prova.q6
            prova_db.q7 = prova.q7
            prova_db.q8 = prova.q8
            prova_db.q9 = prova.q9
            prova_db.q10 = prova.q10
            session.add(prova_db)
            session.commit()
            return prova_db
        else:
            return {"status": "error", "message": "Prova não encontrada"}


@provas_router.delete("/:id")
async def delete_prova(id: int):
    with get_session() as session:
        prova_db = session.get(Provas, id)
        if prova_db:
            if not prova_db.resultados:
                session.delete(prova_db)
                session.commit()
                return {"status": "ok", "message": "Prova excluída"}
            else:
                return {"status": "error", "message": "Prova não pode ser excluída pois possui resultados associados"}
        else:
            return {"status": "error", "message": "Prova não encontrada"}
