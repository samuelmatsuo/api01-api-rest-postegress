import { Model } from "mongoose";

const ProvasSchema = new Model({
  id: Number,
  descricao: String,
  dataProva: String,
  q1: String,
  q2: String,
  q3: String,
  q4: String,
  q5: String,
  q6: String,
  q7: String,
  q8: String,
  q9: String,
  q10: String,
});

ProvasSchema.index({ descricao: 1, dataProva: 1 }, { unique: true });

ProvasSchema.pre("save", async (prova) => {
  if (prova.dataProva) {
    try {
      const data = new Date(prova.dataProva);
      prova.dataProva = data;
    } catch (error) {
      throw new Error("Data inválida");
    }
  }

  if (prova.q1 && prova.q2 && prova.q3 && prova.q4 && prova.q5 && prova.q6 && prova.q7 && prova.q8 && prova.q9 && prova.q10) {
    if (prova.q1.length !== 1 || prova.q2.length !== 1 || prova.q3.length !== 1 || prova.q4.length !== 1 || prova.q5.length !== 1 || prova.q6.length !== 1 || prova.q7.length !== 1 || prova.q8.length !== 1 || prova.q9.length !== 1 || prova.q10.length !== 1) {
      throw new Error("As alternativas das questões devem ter 1 caractere");
    }
  }

  const corretas = [
    "a",
    "b",
    "c",
    "d",
  ];

  prova.nota = 0;
  for (let i = 1; i <= 10; i++) {
    if (corretas.includes(prova["q" + i])) {
      prova.nota++;
    }
  }
});

export default ProvasSchema;
