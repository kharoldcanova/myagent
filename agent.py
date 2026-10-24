from __future__ import annotations

import os

# Carga las variables de entorno desde el archivo .env (OLLAMA_MODEL_ID, OLLAMA_HOST)
from dotenv import load_dotenv

load_dotenv()

# Importa la clase Agent de Strands y el modelo Ollama
from strands import Agent
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

def main() -> None:
    # Instancia el agente con el modelo Ollama y un prompt de sistema en español
    agent = Agent(
        model=create_model(),
        # Sin manejador de callbacks (salida directa)
        callback_handler=None,
        system_prompt=(
            "Eres un secretaria de una empresa. "
            "Respondé en español, de forma breve y útil."
        ),
    )
    # Envía un mensaje inicial al agente y obtiene la respuesta
    response = agent(
        "Hola. Presentate en dos oraciones y contame qué vamos a construir."
    )
    # Imprime la respuesta en consola
    print(response)

# Punto de entrada del script
if __name__ == "__main__":
    main()
