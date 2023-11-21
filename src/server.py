from fastapi import FastAPI, HTTPException
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine
import psycopg2

# Definição dos modelos de dados
class Prova(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    descricao: str
    data_realizacao: str
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str
    q6: str
    q7: str
    q8: str
    q9: str
    q10: str

class ResultadoProva(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    nome_aluno: str
    prova_id: int
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str
    q6: str
    q7: str
    q8: str
    q9: str
    q10: str
    nota_final: Optional[float] = None

# Configuração da conexão com o banco de dados PostgreSQL
DATABASE_URL = "postgresql+psycopg2://seu_usuario:senha@localhost/nome_do_banco"

def create_connection():
    return psycopg2.connect(DATABASE_URL)

# Criação da aplicação FastAPI
app = FastAPI()

# Rota para criar uma prova
@app.post("/provas", status_code=201)
def criar_prova(descricao: str, data_realizacao: str, q1: str, q2: str, q3: str, q4: str, q5: str, q6: str, q7: str, q8: str, q9: str, q10: str):
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        existing_prova = session.exec(Prova).filter(Prova.descricao == descricao, Prova.data_realizacao == data_realizacao).first()
        if existing_prova:
            raise HTTPException(status_code=400, detail="Prova já cadastrada.")
        
        prova = Prova(descricao=descricao, data_realizacao=data_realizacao, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9, q10=q10)
        session.add(prova)
        session.commit()
        return prova

# Rota para inserir o resultado de uma prova de um aluno
@app.post("/resultados_provas", status_code=201)
def inserir_resultado(nome_aluno: str, prova_id: int, q1: str, q2: str, q3: str, q4: str, q5: str, q6: str, q7: str, q8: str, q9: str, q10: str):
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        prova = session.get(Prova, prova_id)
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não cadastrada")
        
        nota = 0
        for i in range(1, 11):
            questao = f"q{i}"
            if getattr(prova, questao) == locals()[questao]:
                nota += 1
        
        resultado = ResultadoProva(nome_aluno=nome_aluno, prova_id=prova_id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9, q10=q10, nota_final=nota)
        session.add(resultado)
        session.commit()
        return resultado

# Rota para obter os resultados de uma prova específica
@app.get("/resultados_provas/{prova_id}")
def obter_resultados(prova_id: int):
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        prova = session.get(Prova, prova_id)
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não encontrada")
        
        resultados = session.exec(ResultadoProva).filter(ResultadoProva.prova_id == prova_id).all()
        
        alunos_resultados = []
        for resultado in resultados:
            status = "aprovado" if resultado.nota_final >= 7 else ("recuperação" if resultado.nota_final >= 5 else "reprovado")
            alunos_resultados.append({"nome": resultado.nome_aluno, "nota": resultado.nota_final, "resultado_final": status})
        
        return {"descricao_prova": prova.descricao, "data_realizacao": prova.data_realizacao, "resultados_alunos": alunos_resultados}

# Rota para alterar as respostas de um aluno em uma prova
@app.patch("/provas_aplicadas/{id}")
def alterar_respostas(id: int, novo_resultado: ResultadoProva):
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        resultado = session.get(ResultadoProva, id)
        if not resultado:
            raise HTTPException(status_code=404, detail="Resultado da prova não encontrado")
        
        prova = session.get(Prova, resultado.prova_id)
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não encontrada")
        
        nota = 0
        for i in range(1, 11):
            questao = f"q{i}"
            if getattr(prova, questao) == getattr(novo_resultado, questao):
                nota += 1
        
        resultado.q1 = novo_resultado.q1
        resultado.q2 = novo_resultado.q2
        resultado.q3 = novo_resultado.q3
        resultado.q4 = novo_resultado.q4
        resultado.q5 = novo_resultado.q5
        resultado.q6 = novo_resultado.q6
        resultado.q7 = novo_resultado.q7
        resultado.q8 = novo_resultado.q8
        resultado.q9 = novo_resultado.q9
        resultado.q10 = novo_resultado.q10
        resultado.nota_final = nota
        
        session.commit()
        return resultado

# Rota para deletar uma prova se não houver resultados de provas cadastrados
@app.delete("/provas/{id}")
def deletar_prova(id: int):
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        resultado_prova = session.exec(ResultadoProva).filter(ResultadoProva.prova_id == id).first()
        if resultado_prova:
            raise HTTPException(status_code=400, detail="Não é possível excluir, há resultados de provas vinculados")
        
        prova = session.get(Prova, id)
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não encontrada")
        
        session.delete(prova)
        session.commit()
        return {"message": "Prova deletada com sucesso"}

# Execução do servidor Uvicorn
if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)