import os
from app.pipeline.grafo import build_review_graph, ReviewState
from app.utils.pdf_exporter import exportar_pdf
from app.utils.carga import cargar_codigo_desde_notebook


def main(ruta_problema: str, ruta_codigo: str, salida_pdf: str, verbose: bool = True) -> None:
    problema = open(ruta_problema, encoding='utf-8').read()
    codigo = cargar_codigo_desde_notebook(ruta_codigo)

    initial_state = ReviewState(
        problema=problema,
        codigo=codigo,
        verbose=verbose
    )

    pipeline = build_review_graph()
    final_state = pipeline.invoke(initial_state)

    print("\n=== INFORME FINAL ===")
    print(final_state["informe"])
    print("\n=== EVALUACIÓN ===")
    print(final_state["evaluacion"])

    exportar_pdf(final_state["informe"], salida_pdf)
    print("PDF generado en:", salida_pdf)


if __name__ == '__main__':
    main(
        'problemaResolver.txt',
        'codigo_estudiante.ipynb',
        'informe_revision.pdf',
        verbose=False
    )
