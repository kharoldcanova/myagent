from __future__ import annotations

import os
from datetime import datetime

# Carga las variables de entorno desde el archivo .env (OLLAMA_MODEL_ID, OLLAMA_HOST)
from dotenv import load_dotenv

load_dotenv()

# Importa la clase Agent de Strands, el modelo Ollama y el decorador @tool
from strands import Agent, tool
from strands.models.ollama import OllamaModel


def create_model() -> OllamaModel:
    """Crea y devuelve el modelo Ollama configurado mediante variables de entorno."""
    return OllamaModel(
        # Identificador del modelo a usar (por defecto: qwen3:4b)
        model_id=os.getenv("OLLAMA_MODEL_ID", "qwen3:4b"),
        # Dirección del servidor Ollama (por defecto: localhost:11434)
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        # Argumentos adicionales: desactiva el modo "think" del modelo
        additional_args={"think": False},
        # Temperatura de muestreo: valores bajos = respuestas más deterministas
        temperature=0.2,
        # Máximo de tokens a generar en la respuesta
        max_tokens=2048,
        # Tamaño de la ventana de contexto (tokens)
        options={"num_ctx": 8192},
    )


# Herramienta 1: suma dos números enteros y devuelve el resultado
@tool
def sumar(a: int, b: int) -> int:
    """Suma dos números enteros y devuelve el resultado.

    Args:
        a: Primer número.
        b: Segundo número.

    Returns:
        La suma de a y b.
    """
    return a + b


# Herramienta 2: devuelve la fecha y hora actual del sistema
@tool
def fecha_actual() -> str:
    """Devuelve la fecha y hora actual del sistema en formato legible.

    Returns:
        Cadena con la fecha y hora actuales.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    # Instancia el agente con el modelo Ollama, las herramientas y un prompt de sistema
    agent = Agent(
        model=create_model(),
        # Lista de herramientas que el agente puede usar
        tools=[sumar, fecha_actual],
        # Sin manejador de callbacks (salida directa)
        callback_handler=None,
        system_prompt=(
            "Sos un asistente útil. "
            "Usá las herramientas disponibles cuando sea necesario. "
            "Respondé en español, de forma breve y clara."
        ),
    )

    # Ejemplo 1: el agente decide usar la herramienta "sumar"
    print("=== Ejemplo 1: suma ===")
    response = agent("¿Cuánto es 12 + 34?")
    print(response)

    # Ejemplo 2: el agente decide usar la herramienta "fecha_actual"
    print("\n=== Ejemplo 2: fecha actual ===")
    response = agent("¿Qué fecha y hora es ahora?")
    print(response)


# Punto de entrada del script
if __name__ == "__main__":
    main()