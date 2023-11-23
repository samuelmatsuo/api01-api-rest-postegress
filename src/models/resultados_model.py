from typing import Optional

from sqlmodel import Field, Relationship, SQLModel
from src.models.provas_model import Provas


class Resultados(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
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
    nota: float = Optional[float]
    prova_id: int = Field(nullable=False, foreign_key="provas.id")
    provas: Optional[Provas] = Relationship(back_populates="resultados")

    @property
    def resultado_final(self):
        if self.nota is not None:
            if self.nota >= 7:
                return "Aprovado"
            elif self.nota >= 5:
                return "Recuperação"
            else:
                return "Reprovado"
        return "Não informado"

    @classmethod
    def from_dict(cls, data: dict):
        if data.get("q1") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 1 deve ser a, b, c ou d.")
        if data.get("q2") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 2 deve ser a, b, c ou d.")
        if data.get("q3") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 3 deve ser a, b, c ou d.")
        if data.get("q4") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 4 deve ser a, b, c ou d.")
        if data.get("q5") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 5 deve ser a, b, c ou d.")
        if data.get("q6") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 6 deve ser a, b, c ou d.")
        if data.get("q7") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 7 deve ser a, b, c ou d.")
        if data.get("q8") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 8 deve ser a, b, c ou d.")
        if data.get("q9") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 9 deve ser a, b, c ou d.")
        if data.get("q10") not in ("a", "b", "c", "d"):
            raise ValueError("A alternativa correta da questão 10 deve ser a, b, c ou d.")
        return cls(**data)

