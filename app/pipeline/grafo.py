from langgraph.graph import StateGraph, START, END     
from dataclasses import dataclass
from typing import Optional

from app.agents.revisores import revisor_logica, revisor_sintaxis, revisor_indentacion
from app.agents.feedback import creador_feedback
from app.agents.evaluaciones import evaluador_rubrica
from app.agents.formato import formateador_informe, validador_forma


@dataclass
class ReviewState:
    problema: str
    codigo: str
    logica: Optional[str] = None
    sintaxis: Optional[str] = None
    indentacion: Optional[str] = None
    feedback: Optional[str] = None
    evaluacion: Optional[str] = None
    informe: Optional[str] = None
    valid: Optional[str] = None


def nodo_logica(st):
    prompt = f"Problema:\n{st.problema}\n\nCódigo:\n{st.codigo}"
    respuesta = revisor_logica(prompt)
    return {"logica": respuesta}

def nodo_sintaxis(st):
    prompt = st.codigo
    respuesta = revisor_sintaxis(prompt)
    return {"sintaxis": respuesta}

def nodo_indentacion(st):
    prompt = st.codigo
    respuesta = revisor_indentacion(prompt)
    return {"indentacion": respuesta}

def nodo_feedback(st):
    prompt = (
        f"Problema:\n{st.problema}\n\n"
        f"Lógica:\n{st.logica}\n\n"
        f"Sintaxis:\n{st.sintaxis}\n\n"
        f"Indentación:\n{st.indentacion}"
    )
    respuesta = creador_feedback(prompt)
    return {"feedback": respuesta}

def nodo_evaluacion(st):
    prompt = (
        f"PROBLEMA A RESOLVER:\n{st.problema}\n\n"
        f"CÓDIGO DEL ESTUDIANTE:\n{st.codigo}\n\n"
        f"REVISIÓN DE LÓGICA ALGORÍTMICA:\n{st.logica}\n\n"
        f"REVISIÓN DE SINTAXIS:\n{st.sintaxis}\n\n"
        f"REVISIÓN DE INDENTACIÓN/ESTILO:\n{st.indentacion}\n\n"
        f"FEEDBACK PEDAGÓGICO:\n{st.feedback}\n\n"
        f"INSTRUCCIÓN: Evalúa este código usando ESPECÍFICAMENTE los criterios de la rúbrica proporcionada. "
        f"Asigna puntuaciones del 1 al 7 para cada criterio y calcula la nota final ponderada."
    )
    respuesta = evaluador_rubrica(prompt)
    return {"evaluacion": respuesta}

def nodo_formateo(st):
    prompt = f"FEEDBACK PEDAGÓGICO:\n{st.feedback}\n\nEVALUACIÓN SEGÚN RÚBRICA:\n{st.evaluacion}"
    respuesta = formateador_informe(prompt)
    return {"informe": respuesta}


def nodo_reporte_final(st):
    # El informe ya debería incluir la evaluación, pero asegurar que esté completo
    informe_final = st.informe
    if "Evaluación según rúbrica" not in informe_final:
        informe_final = st.informe + "\n\n## Evaluación según rúbrica\n" + st.evaluacion
    return {"informe": informe_final}

def nodo_validacion(st):

    respuesta = validador_forma(st.informe).strip().lower()
    return {"valid": respuesta, "informe": st.informe}

def build_review_graph():
    builder = StateGraph(state_schema=ReviewState)

    # Registro de nodos
    builder.add_node("node_logica", nodo_logica)
    builder.add_node("node_sintaxis", nodo_sintaxis)
    builder.add_node("node_indentacion", nodo_indentacion)
    builder.add_node("node_feedback", nodo_feedback)
    builder.add_node("node_evaluacion", nodo_evaluacion)
    builder.add_node("node_formateo", nodo_formateo)
    builder.add_node("node_validacion", nodo_validacion)
    builder.add_node("node_reporte_final", nodo_reporte_final)

    # Aristas iniciales en paralelo desde START
    builder.add_edge(START, "node_logica")
    builder.add_edge(START, "node_sintaxis")
    builder.add_edge(START, "node_indentacion")

    # Flujo secuencial después de las tres revisiones
    builder.add_edge("node_logica", "node_feedback")
    builder.add_edge("node_sintaxis", "node_feedback")
    builder.add_edge("node_indentacion", "node_feedback")
    builder.add_edge("node_feedback", "node_evaluacion")
    builder.add_edge("node_evaluacion", "node_formateo")

    # Bucle de refinamiento: formateo ↔ validación
    builder.add_edge("node_formateo", "node_validacion")
    
    def route_from_validation(state):
        # Verificar si la validación indica que el formato es correcto
        valid_response = state.valid.strip().lower() if state.valid else ""
        if valid_response.startswith("sí") or valid_response.startswith("si"):
            return "node_reporte_final"
        else:
            return "node_formateo"
    
    builder.add_conditional_edges(
        "node_validacion",
        route_from_validation,
        ["node_formateo", "node_reporte_final"]
    )

    builder.add_edge("node_reporte_final", END)

    return builder.compile()