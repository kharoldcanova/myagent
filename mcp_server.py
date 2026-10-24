"""Servidor MCP simple de ejemplo.

Expone herramientas llamadas "saludar" y "sumar".
Se ejecuta por stdio para que un cliente MCP (Strands) pueda conectarse.
"""

from mcp.server.mcpserver import MCPServer

# Crea la instancia del servidor MCP con un nombre descriptivo
mcp = MCPServer("servidor-ejemplo")


@mcp.tool()
def saludar(nombre: str) -> str:
    """Devuelve un saludo personalizado para el nombre dado.

    Args:
        nombre: Nombre de la persona a saludar.

    Returns:
        Un saludo en español.
    """
    return f"¡Hola, {nombre}! Bienvenido al ejemplo de MCP con Strands."


@mcp.tool()
def sumar(a: int, b: int) -> int:
    """Suma dos números enteros.

    Args:
        a: Primer número.
        b: Segundo número.

    Returns:
        La suma de a y b.
    """
    return a + b


if __name__ == "__main__":
    # Ejecuta el servidor por stdio (transporte estándar para MCP local)
    mcp.run(transport="stdio")