# SQLite MCP with Ollama

Local **Model Context Protocol (MCP)** server and client for storing and querying data in SQLite using LlamaIndex.

## Features
- 🗄️ SQLite database (`demo.db`)
- 📡 MCP server (SSE or stdio)
- 🤖 LlamaIndex client agent with tool calling
- Tools:
  - `add_data(name, age, profession)` → insert record
  - `read_data(query)` → fetch records

## Steps

### 1. Create a virtual Env and install dependencies via requirements.txt
### 2. Start the MCP server: python server.py --server_type=sse
### 3. Run the MCP client: python client.py
### 4. Expected output: Enter your message: add data to db: saqiba is developer and language used is python and her age is 29.




