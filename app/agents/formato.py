from .revisores import crear_agente

formateador_informe = crear_agente(
    """Eres un experto en informes educativos.
Genera un informe con esta estructura:
1. Resumen ejecutivo
2. Resultados de la rúbrica: tabla (Categoría, Puntuación, Peso, % logro)
3. Evaluación final (1.0–7.0)
4. Comentarios detallados por categoría
5. Recomendaciones y próximos pasos
6. Conclusión breve

Usa encabezados Markdown y formato de tabla Markdown."""
)

validador_forma = crear_agente(
    "Eres un revisor de formato. Recibes el informe preliminar y compruebas si sigue la estructura deseada. "
    "Responde con 'sí' si está bien formateado, o con 'no' y una breve sugerencia de mejora si no lo estuviera."
)

creador_mensaje_correo = crear_agente(
    "Eres un asistente académico. Crea un asunto de correo y un mensaje motivador basado en el informe y la nota."
)
