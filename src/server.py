from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.database import create_db_and_tables
from src.routes.provas_routes import provas_router
from src.routes.resultados_routes import resultados_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(provas_router)
app.include_router(resultados_router)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.get("/provas/:prova_id")
async def get_provas_by_id(prova_id: int):
    with get_session() as session:
        statement = select(Provas).where(Provas.id == prova_id)
        prova = session.exec(statement).first()
        if prova:
            return prova
        else:
            return {"status": "error", "message": "Prova não encontrada"}


@app.patch("/resultados/:id")
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


@app.delete("/provas/:id")
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
