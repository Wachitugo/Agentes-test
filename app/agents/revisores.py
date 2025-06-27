from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno primero
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0)

def crear_agente(prompt_sistema: str):
    def ejecutar(texto_usuario: str) -> str:
        mensajes = [
            SystemMessage(content=prompt_sistema),
            HumanMessage(content=texto_usuario)
        ]
        return llm(mensajes).content
    return ejecutar

revisor_logica = crear_agente(
    "Eres un revisor de lógica algorítmica. Analiza si el código resuelve el problema planteado."
)
revisor_sintaxis = crear_agente(
    "Eres un revisor de sintaxis Python. Evalúa errores de sintaxis y uso de estructuras."
)
revisor_indentacion = crear_agente(
    "Eres un revisor de estilo Python. Evalúa la indentación según PEP8."
)
