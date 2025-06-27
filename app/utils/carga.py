import nbformat

def cargar_codigo_desde_notebook(ruta: str) -> str:
    nb = nbformat.read(ruta, as_version=4)
    return "\n\n".join(cell.source for cell in nb.cells if cell.cell_type == 'code')
