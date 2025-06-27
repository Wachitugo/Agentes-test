import pandas as pd
from .revisores import crear_agente

rubric_df = pd.read_excel("rubricaDemo.xlsx")
rubric_str = rubric_df.to_string(index=False)

evaluador_rubrica = crear_agente(
    f"""Eres un evaluador experto. Aplica esta rúbrica al código:
{rubric_str}

Recibe el problema, el código y el feedback; asigna puntuaciones de 1 a 7 según los criterios,
calcula el % de logro de cada categoría y una nota final de 1.0 a 7.0, justificando cada calificación."""
)
