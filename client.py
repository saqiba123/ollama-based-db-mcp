import asyncio
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult, ToolCall
from llama_index.core.workflow import Context
from llama_index.llms.openai import OpenAI  # make sure llama_index has this

# Setup a local LLM (Ollama)
# Reduce context size
# You can lower the num_ctx parameter so Ollama allocates less memory:
llm = Ollama(model="llama3.2:3b", request_timeout=120.0,additional_kwargs={"num_ctx": 2048})
Settings.llm = llm

# System prompt
# SYSTEM_PROMPT = """\
# You are an AI assistant for Tool Calling.

# Before you help a user, you need to work with tools to interact with Our Database
# """

# SYSTEM_PROMPT = """\
# You are an AI assistant for Tool Calling.

# You have access to tools for working with our database.

# - To add a new person, call `add_data(name, age, profession)` with structured arguments.
# - To read data, call `read_data()` or provide a SQL query string if needed.

# Do not generate raw SQL for insertion. Use the structured parameters instead.
# """


SYSTEM_PROMPT = """\
You are an AI assistant for Tool Calling.

You have access to tools for working with our database.

- To add a new person, call `add_data` with these arguments:
    • name (string)
    • age (integer)
    • profession (string)

- To read data, call `read_data()`. You can also pass a SQL SELECT query if needed.

⚠️ Important:
- Do NOT generate raw SQL for insertions.
- Always use structured arguments when calling `add_data`.
"""

# Helper function: get_agent()
async def get_agent(tools: McpToolSpec):
    tool_list = await tools.to_tool_list_async()
    agent = FunctionAgent(
        name="Agent",
        description="An agent that can work with Our Database software.",
        tools=tool_list,
        #llm=OpenAI(model="gpt-4"),  # you can replace with Ollama if preferred
        llm=llm,  # you can replace with Ollama if preferred
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

# Helper function: handle_user_message()
async def handle_user_message(
    message_content: str,
    agent: FunctionAgent,
    agent_context: Context,
    verbose: bool = False,
):
    handler = agent.run(message_content, ctx=agent_context)
    async for event in handler.stream_events():
        if verbose and isinstance(event, ToolCall):
            print(f"Calling tool {event.tool_name} with kwargs {event.tool_kwargs}")
        elif verbose and isinstance(event, ToolCallResult):
            print(f"Tool {event.tool_name} returned {event.tool_output}")

    response = await handler
    return str(response)

# Main entry point
async def main():
    # Initialize the MCP client and tools
    mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
    mcp_tool = McpToolSpec(client=mcp_client)

    # Build agent
    agent = await get_agent(mcp_tool)
    agent_context = Context(agent)

    # Interactive loop
    while True:
        user_input = input("Enter your message: ")
        if user_input.lower().strip() == "exit":
            break
        print("User: ", user_input)
        response = await handle_user_message(user_input, agent, agent_context, verbose=True)
        print("Agent: ", response)

if __name__ == "__main__":
    asyncio.run(main())
