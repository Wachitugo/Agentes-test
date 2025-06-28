import os
from pipeline.grafo import build_review_graph, ReviewState
from utils.html_exporter import exportar_html
from utils.carga import cargar_codigo_desde_notebook


def main(ruta_problema: str, ruta_codigo: str, salida_html: str) -> None:
    problema = open(ruta_problema, encoding='utf-8').read()
    codigo = cargar_codigo_desde_notebook(ruta_codigo)

    initial_state = ReviewState(
        problema=problema,
        codigo=codigo
    )

    pipeline = build_review_graph()
    final_state = pipeline.invoke(initial_state)

    exportar_html(final_state["informe"], salida_html)


if __name__ == '__main__':
    main(
        'data/problemaResolver.txt',
        'data/codigo_estudiante.ipynb',
        'result/informe_revision.html',
    )
