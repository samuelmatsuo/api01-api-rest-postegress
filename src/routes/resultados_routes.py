from fastapi import APIRouter
from sqlmodel import select

from src.config.database import get_session
from src.models.provas_model import Provas
from src.models.resultados_model import Resultados

resultados_router = APIRouter(prefix="/resultados")


@resultados_router.post("")
def cria_prova(resultado: Resultados):
    with get_session() as session:
        # Calcular a nota baseado nas questòes da prova

        # Buscar a prova do banco de dados
        statement = select(Provas).where(Provas.id == resultado.prova_id)
        prova = session.exec(statement).first()

        # se tiver prova, vai calcular a nota

        if prova:
            acertos = 0
            for i in range(1, 11):
                if resultado.q{i} == prova.q{i}:
                    acertos += 1
            resultado.nota = acertos / 10

        session.add(resultado)
        session.commit()
        session.refresh(resultado)
        return resultado


@resultados_router.get("")
async def get_resultados():
    with get_session() as session:
        statement = select(Resultados)
        resultados = session.exec(statement).all()
        return resultados


@resultados_router.get("/:prova_id")
async def get_resultados_by_prova_id(prova_id: int):
    with get_session() as session:
        statement = select(Resultados).where(Resultados.prova_id == prova_id)
        resultados = session.exec(statement).all()
        return resultados


@resultados_router.patch("/:id")
async def update_resultado(id: int, resultado: Resultados):
    with get_session() as session:
        resultado_db = session.get(Resultados, id)
        if resultado_db:
            for i in range(1, 11):
                resultado_db.q{i} = resultado.q{i}
            acertos = 0
            for i in range(1, 11):
                if resultado_db.q{i} == resultado.prova.q{i}:
                    acertos += 1
            resultado_db.nota = acertos / 10
            session.add(resultado_db)
            session.commit()
            return resultado_db
        else:
            return {"status": "error", "message": "Resultado não encontrado"}


@resultados_router.delete("/:id")
async def delete_resultado(id: int):
    with get_session() as session:
        resultado_db = session.get(Resultados, id)
        if resultado_db:
            session.delete(resultado_db)
            session.commit()
            return {"status": "ok", "message": "Resultado excluído"}
        else:
            return {"status": "error", "message": "Resultado não encontrado"}
