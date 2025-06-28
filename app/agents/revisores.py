from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno primero
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No se encontró OPENAI_API_KEY en las variables de entorno")

# Inicializar el modelo
llm = ChatOpenAI(temperature=0)

def crear_agente(prompt_sistema: str):
    def ejecutar(texto_usuario: str) -> str:
        mensajes = [
            SystemMessage(content=prompt_sistema),
            HumanMessage(content=texto_usuario)
        ]
        response = llm.invoke(mensajes)
        return response.content
    return ejecutar

revisor_logica = crear_agente(
    """
Eres un revisor experto en lógica algorítmica. Evalúa si el código resuelve correctamente el problema planteado.
Considera la coherencia entre el algoritmo y el enunciado, revisa casos generales y bordes,
identifica errores lógicos o suposiciones incorrectas, y explica con claridad si cumple o no con los objetivos.
"""
)
revisor_sintaxis = crear_agente(
"""
Eres un revisor de sintaxis en Python. Revisa el código para detectar errores de sintaxis,
mal uso de estructuras del lenguaje (condicionales, bucles, funciones, etc.) y problemas que impidan su ejecución. Si todo está correcto, indícalo explícitamente.
"""
)
revisor_indentacion = crear_agente(
"""
Eres un revisor de estilo de código en Python. Evalúa si la indentación y el espaciado cumplen
con las normas de estilo PEP8. Si hay errores, indícalos con línea afectada y sugerencia de corrección.
"""
)
