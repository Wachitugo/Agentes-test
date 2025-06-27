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
    verbose: bool = True
    logica: Optional[str] = None
    sintaxis: Optional[str] = None
    indentacion: Optional[str] = None
    feedback: Optional[str] = None
    evaluacion: Optional[str] = None
    informe: Optional[str] = None
    valid: Optional[str] = None


def nodo_logica(st):
    prompt = f"Problema:\n{st.problema}\n\nCódigo:\n{st.codigo}"
    if st.verbose:
        print("[LÓGICA] Prompt:", prompt)
    return {"logica": revisor_logica(prompt)}

def nodo_sintaxis(st):
    if st.verbose:
        print("[SINTAXIS] Código:", st.codigo)
    return {"sintaxis": revisor_sintaxis(st.codigo)}

def nodo_indentacion(st):
    if st.verbose:
        print("[INDENTACIÓN] Código:", st.codigo)
    return {"indentacion": revisor_indentacion(st.codigo)}

def nodo_feedback(st):
    prompt = (
        f"Problema:\n{st.problema}\n\n"
        f"Lógica:\n{st.logica}\n\n"
        f"Sintaxis:\n{st.sintaxis}\n\n"
        f"Indentación:\n{st.indentacion}"
    )
    if st.verbose:
        print("[FEEDBACK] Prompt:", prompt)
    return {"feedback": creador_feedback(prompt)}

def nodo_evaluacion(st):
    prompt = (
        f"Problema:\n{st.problema}\n\n"
        f"Código:\n{st.codigo}\n\n"
        f"Feedback:\n{st.feedback}"
    )
    if st.verbose:
        print("[EVALUACIÓN] Prompt:", prompt)
    return {"evaluacion": evaluador_rubrica(prompt)}

def nodo_formateo(st):
    if st.verbose:
        print("[FORMATO] Feedback:", st.feedback)
    return {"informe": formateador_informe(st.feedback)}

def nodo_validacion(st):
    if st.verbose:
        print("[VALIDACIÓN] Informe:\n", st.informe)
    validacion = validador_forma(st.informe).strip().lower()
    return {"valid": validacion, "informe": st.informe}

def nodo_reporte_final(st):
    informe_final = st.informe + "\n\n## Evaluación según rúbrica\n" + st.evaluacion
    return {"informe": informe_final}


def build_review_graph():
    builder = StateGraph(state_schema=ReviewState)

    builder.add_node("node_logica", nodo_logica)
    builder.add_node("node_sintaxis", nodo_sintaxis)
    builder.add_node("node_indentacion", nodo_indentacion)
    builder.add_node("node_feedback", nodo_feedback)
    builder.add_node("node_evaluacion", nodo_evaluacion)
    builder.add_node("node_formateo", nodo_formateo)
    builder.add_node("node_validacion", nodo_validacion)
    builder.add_node("node_reporte_final", nodo_reporte_final)

    builder.add_edge(START, "node_logica")
    builder.add_edge(START, "node_sintaxis")
    builder.add_edge(START, "node_indentacion")

    builder.add_edge("node_logica", "node_feedback")
    builder.add_edge("node_sintaxis", "node_feedback")
    builder.add_edge("node_indentacion", "node_feedback")

    builder.add_edge("node_feedback", "node_evaluacion")
    builder.add_edge("node_evaluacion", "node_formateo")
    builder.add_edge("node_formateo", "node_validacion")

    builder.add_conditional_edges("node_validacion", {
        "node_formateo": lambda st: st.valid != "sí",
        "node_reporte_final": lambda st: st.valid == "sí",
    })

    builder.add_edge("node_reporte_final", END)

    return builder.compile()