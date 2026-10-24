## Creacion de agente usando strands

Strands Agents es un kit de herramientas open-source que permite construir agentes de IA en Python.

La libreria esta desarrollada por AWS.

Se instala con el comando:

`pip install strands`

Se puede definir herramientas personalizadas, integrar con MCP, soporta streaming bidireccional, tambien permite gestionar el contexto.

## Requisitos previos: Ollama

Este proyecto usa Ollama como proveedor de modelos locales.

### 1. Instalar Ollama

En Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verifica la instalacion:

```bash
ollama --version
```

Inicia el servicio (si no esta corriendo):

```bash
ollama serve
```

### 2. Descargar un modelo

Descarga un modelo de ejemplo (elige el que prefieras):

```bash
ollama pull qwen3:4b
```

Otros modelos disponibles: `llama3.2`, `mistral`, `gemma2`, etc. Puedes listar los modelos descargados con:

```bash
ollama list
```

### 3. Configurar el entorno Python

Activa el entorno virtual del proyecto:

```bash
source myagent/bin/activate
```

Instala las dependencias:

```bash
pip install strands-agents python-dotenv ollama
```

Configura las variables de entorno en el archivo `.env`:

```env
OLLAMA_MODEL_ID=qwen3:4b
OLLAMA_HOST=http://localhost:11434
```

### 4. Ejecutar el agente

Con el entorno activado:

```bash
python agent.py
```

O en una sola linea (sin activar manualmente el entorno):

```bash
myagent/bin/python agent.py
```