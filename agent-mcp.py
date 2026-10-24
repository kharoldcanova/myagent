from __future__ import annotations

import os
import sys

# Carga las variables de entorno desde el archivo .env (OLLAMA_MODEL_ID, OLLAMA_HOST)
from dotenv import load_dotenv

load_dotenv()

# Importa la clase Agent de Strands, el modelo Ollama y el cliente MCP
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools.mcp import MCPClient


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
    # Configura el servidor MCP local que se ejecutará por stdio
    # Se lanza como subproceso: python mcp_server.py
    server_params = StdioServerParameters(
        command=sys.executable,          # Intérprete Python actual
        args=["mcp_server.py"],         # Script del servidor MCP
    )

    # Crea el cliente MCP que se conecta al servidor por stdio
    mcp_client = MCPClient(lambda: stdio_client(server_params))

    # El cliente MCP se usa como context manager para gestionar la conexión
    with mcp_client:
        # Obtiene las herramientas expuestas por el servidor MCP
        tools = mcp_client.list_tools_sync()

        # Instancia el agente con el modelo Ollama y las herramientas del MCP
        agent = Agent(
            model=create_model(),
            # Herramientas obtenidas del servidor MCP
            tools=tools,
            # Sin manejador de callbacks (salida directa)
            callback_handler=None,
            system_prompt=(
                "Sos un asistente útil. "
                "Usá las herramientas disponibles (saludar, sumar) cuando sea necesario. "
                "Respondé en español, de forma breve y clara."
            ),
        )

        # Ejemplo 1: el agente usa la herramienta "saludar" del servidor MCP
        print("=== Ejemplo 1: saludar (MCP) ===")
        response = agent("Saludá a Juan usando la herramienta disponible.")
        print(response)

        # Ejemplo 2: el agente usa la herramienta "sumar" del servidor MCP
        print("\n=== Ejemplo 2: sumar (MCP) ===")
        response = agent("¿Cuánto es 7 + 8? Usá la herramienta sumar.")
        print(response)


# Punto de entrada del script
if __name__ == "__main__":
    main()