import asyncio
import os
from browser_use import Agent, Controller
from browser_use.mcp.client import MCPClient
from browser_use.llm import ChatOpenAI

async def main():
    """
    Example showing how to connect to a Browser-use MCP server deployed on Heroku.
    
    This example demonstrates how to:
    1. Connect to a Heroku-deployed Browser-use MCP server
    2. Register the MCP server's tools to a controller
    3. Create and run an agent that uses these tools
    
    Environment Variables Required:
    - HEROKU_MCP_URL: The URL of your Heroku MCP server (e.g., https://your-app-name.herokuapp.com/mcp)
    - HEROKU_MCP_TOKEN: Your authentication token for the Heroku MCP server
    - OPENAI_API_KEY: Your OpenAI API key
    """
    # Initialize controller
    controller = Controller()
    
    # Connect to the Heroku-deployed Browser-use MCP server
    browser_client = MCPClient(
        server_name="browser-use",
        url=os.environ.get("HEROKU_MCP_URL"),
        token=os.environ.get("HEROKU_MCP_TOKEN"),
    )
    
    try:
        # Connect to the MCP server
        await browser_client.connect()
        print("Successfully connected to Browser-use MCP server")
        
        # Register the MCP server's tools to the controller
        await browser_client.register_to_controller(controller)
        print("Successfully registered MCP tools to controller")
        
        # Create an agent with the MCP-enabled controller
        agent = Agent(
            task="Compare the price of gpt-4o and DeepSeek-V3",
            llm=ChatOpenAI(model="gpt-4o", temperature=1.0),
            controller=controller
        )
        
        # Run the agent
        await agent.run()
    finally:
        # Ensure we disconnect from the MCP server
        await browser_client.disconnect()
        print("Disconnected from Browser-use MCP server")

if __name__ == "__main__":
    asyncio.run(main())