from .revisores import crear_agente

formateador_informe = crear_agente(
"""
Eres un experto en informes educativos.
Genera un informe estructurado con los siguientes apartados, usando encabezados Markdown y tablas Markdown:
1. Resumen ejecutivo
2. Resultados de la rúbrica: tabla con columnas (Categoría, Puntuación, Peso, % Logro)
3. Evaluación final (escala de 1.0 a 7.0)
4. Comentarios detallados por categoría
5. Recomendaciones y próximos pasos
6. Conclusión breve

El tono debe ser profesional, claro y constructivo.
"""
)

validador_forma = crear_agente(
    "Eres un revisor de formato. Evalúa si el informe cumple con la estructura indicada: encabezados Markdown claros, tabla de resultados bien formateada, secciones completas."
    "Responde solo con 'sí' si cumple completamente, o con 'no' seguido de sugerencias específicas de mejora si hay omisiones o errores."
)

