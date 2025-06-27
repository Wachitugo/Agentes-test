# Sistema de Revisión Automatizada de Código

Sistema que utiliza agentes de IA para revisar y evaluar código Python, generando informes detallados.

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- Poetry
- OpenAI API Key

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Wachitugo/Agentes-test
cd Agentes-test
```

2. **Crear entorno virtual con Poetry**
```bash
poetry install
```

3. **Configurar variables de entorno**
Crear archivo `.env` en la raíz del proyecto:
```properties
OPENAI_API_KEY=tu-api-key-aquí
```

### Uso

1. **Preparar archivos de entrada**
- Crear archivo `problemaResolver.txt` con el enunciado del problema
- Crear archivo `codigo_estudiante.ipynb` con el código a revisar
- Asegurar que existe `rubricaDemo.xlsx` con los criterios de evaluación

2. **Ejecutar el sistema**
```bash
poetry run python main.py
```

## 📁 Estructura del Proyecto

```
Agentes-test/
├── app/
│   ├── agents/          # Agentes de IA
│   ├── pipeline/        # Pipeline de procesamiento
│   └── utils/          # Utilidades
├── poetry.lock
├── pyproject.toml
└── README.md
```

## 🔧 Configuración Docker

```bash
# Construir imagen
docker build -t agentes-review .

# Ejecutar contenedor
docker run -it --rm -v "%CD%/data:" -e OPENAI_API_KEY=tu-api-key agentes-review
```

