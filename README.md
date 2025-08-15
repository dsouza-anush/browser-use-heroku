<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./static/browser-use-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./static/browser-use.png">
  <img alt="Shows a black Browser Use Logo in light color mode and a white one in dark color mode." src="./static/browser-use.png"  width="full">
</picture>

<h1 align="center">Enable AI to control your browser 🤖</h1>

<p align="center">
  <a href="https://www.heroku.com/deploy?template=https://github.com/dsouza-anush/browser-use-heroku">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku">
  </a>
</p>

[![GitHub stars](https://img.shields.io/github/stars/gregpr07/browser-use?style=social)](https://github.com/gregpr07/browser-use/stargazers)
[![Discord](https://img.shields.io/discord/1303749220842340412?color=7289DA&label=Discord&logo=discord&logoColor=white)](https://link.browser-use.com/discord)
[![Cloud](https://img.shields.io/badge/Cloud-☁️-blue)](https://cloud.browser-use.com)
[![Documentation](https://img.shields.io/badge/Documentation-📕-blue)](https://docs.browser-use.com)
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/intent/user?screen_name=gregpr07)
[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/intent/user?screen_name=mamagnus00)
[![Weave Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fapp.workweave.ai%2Fapi%2Frepository%2Fbadge%2Forg_T5Pvn3UBswTHIsN1dWS3voPg%2F881458615&labelColor=#EC6341)](https://app.workweave.ai/reports/repository/org_T5Pvn3UBswTHIsN1dWS3voPg/881458615)

🌐 Browser-use is the easiest way to connect your AI agents with the browser.

💡 See what others are building and share your projects in our [Discord](https://link.browser-use.com/discord)! Want Swag? Check out our [Merch store](https://browsermerch.com).

🌤️ Skip the setup - try our <b>hosted version</b> for instant browser automation! <b>[Try the cloud ☁︎](https://cloud.browser-use.com)</b>.

# Quick start

With pip (Python>=3.11):

```bash
pip install browser-use
```

Install the browser:

```bash
playwright install chromium --with-deps --no-shell
```

Spin up your agent:

```python
import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent
from browser_use.llm import ChatOpenAI

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=ChatOpenAI(model="o4-mini", temperature=1.0),
    )
    await agent.run()

asyncio.run(main())
```

Add your API keys for the provider you want to use to your `.env` file.

```bash
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
GOOGLE_API_KEY=
DEEPSEEK_API_KEY=
GROK_API_KEY=
NOVITA_API_KEY=
```

For other settings, models, and more, check out the [documentation 📕](https://docs.browser-use.com).

### Test with UI

You can test browser-use using its [Web UI](https://github.com/browser-use/web-ui) or [Desktop App](https://github.com/browser-use/desktop).

### Test with an interactive CLI

You can also use our `browser-use` interactive CLI (similar to `claude` code):

```bash
pip install "browser-use[cli]"
browser-use
```

## MCP Integration

Browser-use supports the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), enabling integration with Claude Desktop and other MCP-compatible clients.

## Deploy to Heroku

Browser-use can be easily deployed to Heroku. This will set up a Heroku application with all the necessary configurations to run Browser-use as an MCP server.

### Using the Heroku Button

The simplest way to deploy is by clicking the Heroku Button at the top of this README. This will:

1. Create a new Heroku app with the Browser-use code
2. Configure the necessary buildpacks for Python, APT dependencies, and Chrome
3. Set up the Heroku AI add-on for MCP integration
4. Deploy the application automatically

### Manual Deployment

If you prefer to deploy manually, follow these steps:

```bash
# Clone the repository
git clone https://github.com/browser-use/browser-use.git
cd browser-use

# Create a Heroku app
heroku create

# Add required buildpacks
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome

# Add Heroku AI add-on
heroku addons:create heroku-ai:standard

# Configure environment variables (replace with your actual API keys)
heroku config:set OPENAI_API_KEY=your_openai_key_here
heroku config:set ANTHROPIC_API_KEY=your_anthropic_key_here
heroku config:set IN_DOCKER=true

# Deploy the application
git push heroku main
```

### Connecting to the MCP Server

Once deployed to Heroku, your Browser-use application will function as an MCP server that can be connected to from various clients. The MCP server process is named `mcp-browser` in the Procfile to comply with Heroku's MCP naming requirements.

> **Important:** The MCP server is configured to scale to 0 dynos by default, as recommended by Heroku for MCP servers. When you need to use it, you'll need to scale it up using the Heroku CLI or dashboard: `heroku ps:scale mcp-browser=1 -a your-app-name`

#### Using with Claude Desktop or Other MCP-Compatible Clients

Add your Heroku-deployed browser-use instance to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "browser-use": {
      "url": "https://your-app-name.herokuapp.com/mcp",
      "token": "your_heroku_ai_token"
    }
  }
}
```

Replace `your-app-name` with your actual Heroku app name and `your_heroku_ai_token` with the authentication token from your Heroku AI add-on settings.

#### Using the MCP Server Programmatically

You can also connect to your Heroku-deployed Browser-use MCP server programmatically. Here's an example Python script that demonstrates how to do this:

```python
import asyncio
import os
from browser_use import Agent, Controller
from browser_use.mcp.client import MCPClient
from browser_use.llm import ChatOpenAI

async def main():
    # Initialize controller
    controller = Controller()
    
    # Connect to the Heroku-deployed Browser-use MCP server
    browser_client = MCPClient(
        server_name="browser-use",
        url=os.environ.get("HEROKU_MCP_URL"),  # e.g., "https://your-app-name.herokuapp.com/mcp"
        token=os.environ.get("HEROKU_MCP_TOKEN"),  # Your Heroku AI token
    )
    
    try:
        # Connect to the MCP server
        await browser_client.connect()
        
        # Register the MCP server's tools to the controller
        await browser_client.register_to_controller(controller)
        
        # Create an agent with the MCP-enabled controller
        agent = Agent(
            task="Compare the price of gpt-4o and DeepSeek-V3",
            llm=ChatOpenAI(model="gpt-4o"),
            controller=controller
        )
        
        # Run the agent
        await agent.run()
    finally:
        # Ensure we disconnect from the MCP server
        await browser_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

A full working example can be found in the `examples/heroku_mcp_client.py` file.

#### Getting Your Heroku AI Token

To get your Heroku AI token for MCP integration:

1. Deploy your application using the Heroku Button or CLI
2. Go to your Heroku Dashboard and select your application
3. Navigate to the "Resources" tab and click on "Heroku AI" add-on
4. Find your API key/token in the add-on dashboard
5. Alternatively, use the Heroku CLI: `heroku config:get INFERENCE_KEY -a your-app-name`

#### MCP Server Environment Variables

The following environment variables can be configured for your MCP server:

| Variable | Description | Default |
|----------|-------------|--------|
| `OPENAI_API_KEY` | Your OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | - |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint | - |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | - |
| `GOOGLE_API_KEY` | Your Google API key | - |
| `DEEPSEEK_API_KEY` | Your Deepseek API key | - |
| `GROK_API_KEY` | Your Grok API key | - |
| `NOVITA_API_KEY` | Your Novita API key | - |
| `ANONYMIZED_TELEMETRY` | Enable/disable anonymous telemetry | `true` |
| `BROWSER_USE_LOGGING_LEVEL` | Logging level (result, debug, info) | `info` |
| `BROWSER_USE_CALCULATE_COST` | Enable cost calculations | `false` |
| `IN_DOCKER` | Optimize Chrome for Docker environments | `true` |
| `WEB_CONCURRENCY` | Number of concurrent web workers | `1` |
| `STDIO_MODE_ONLY` | Use only STDIO mode, disable HTTP server | `false` |
| `API_KEY` | Security key for API authentication | Auto-generated |

You can set these environment variables in the Heroku dashboard after deployment or include them in the deployment process.

### Keeping Your Deployment Updated

#### Automatic Updates via GitHub Actions

This repository includes a GitHub Actions workflow that automatically syncs with the upstream repository on a daily basis while preserving all Heroku-specific configurations. The workflow:

1. Runs daily at 00:00 UTC (can also be triggered manually)
2. Fetches the latest changes from the upstream repository
3. Preserves all Heroku-specific files during the update
4. Commits and pushes the merged changes to the main branch

No manual intervention is needed to keep your repository updated with the latest features and fixes from the original repository.

#### Manual Updates

If you prefer to update manually, this repository also includes a script to sync with the upstream repository. To update your deployment with the latest changes:

```bash
# Clone your repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Run the sync script
./bin/sync_upstream.sh

# Push the updates to your Heroku app
git push heroku main
```

The script automatically preserves your Heroku configuration files while pulling in the latest updates from the original repository.

### Use as MCP Server with Claude Desktop

Add browser-use to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "browser-use": {
      "command": "uvx",
      "args": ["browser-use[cli]", "--mcp"],
      "env": {
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

This gives Claude Desktop access to browser automation tools for web scraping, form filling, and more.

### Connect External MCP Servers to Browser-Use Agent

Browser-use agents can connect to multiple external MCP servers to extend their capabilities:

```python
import asyncio
from browser_use import Agent, Controller
from browser_use.mcp.client import MCPClient
from browser_use.llm import ChatOpenAI

async def main():
    # Initialize controller
    controller = Controller()
    
    # Connect to multiple MCP servers
    filesystem_client = MCPClient(
        server_name="filesystem",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/documents"]
    )
    
    github_client = MCPClient(
        server_name="github", 
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_TOKEN": "your-github-token"}
    )
    
    # Connect and register tools from both servers
    await filesystem_client.connect()
    await filesystem_client.register_to_controller(controller)
    
    await github_client.connect()
    await github_client.register_to_controller(controller)
    
    # Create agent with MCP-enabled controller
    agent = Agent(
        task="Find the latest report.pdf in my documents and create a GitHub issue about it",
        llm=ChatOpenAI(model="gpt-4o"),
        controller=controller  # Controller has tools from both MCP servers
    )
    
    # Run the agent
    await agent.run()
    
    # Cleanup
    await filesystem_client.disconnect()
    await github_client.disconnect()

asyncio.run(main())
```

See the [MCP documentation](https://docs.browser-use.com/customize/mcp-server) for more details.

# Demos

<br/><br/>

[Task](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/shopping.py): Add grocery items to cart, and checkout.

[![AI Did My Groceries](https://github.com/user-attachments/assets/a0ffd23d-9a11-4368-8893-b092703abc14)](https://www.youtube.com/watch?v=L2Ya9PYNns8)

<br/><br/>

Prompt: Add my latest LinkedIn follower to my leads in Salesforce.

![LinkedIn to Salesforce](https://github.com/user-attachments/assets/50d6e691-b66b-4077-a46c-49e9d4707e07)

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/use-cases/find_and_apply_to_jobs.py): Read my CV & find ML jobs, save them to a file, and then start applying for them in new tabs, if you need help, ask me.'

https://github.com/user-attachments/assets/171fb4d6-0355-46f2-863e-edb04a828d04

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/browser/real_browser.py): Write a letter in Google Docs to my Papa, thanking him for everything, and save the document as a PDF.

![Letter to Papa](https://github.com/user-attachments/assets/242ade3e-15bc-41c2-988f-cbc5415a66aa)

<br/><br/>

[Prompt](https://github.com/browser-use/browser-use/blob/main/examples/custom-functions/save_to_file_hugging_face.py): Look up models with a license of cc-by-sa-4.0 and sort by most likes on Hugging face, save top 5 to file.

https://github.com/user-attachments/assets/de73ee39-432c-4b97-b4e8-939fd7f323b3

<br/><br/>

## More examples

For more examples see the [examples](examples) folder or join the [Discord](https://link.browser-use.com/discord) and show off your project. You can also see our [`awesome-prompts`](https://github.com/browser-use/awesome-prompts) repo for prompting inspiration.

# Vision

Tell your computer what to do, and it gets it done.

## Roadmap

### Agent

- [ ] Improve agent memory to handle +100 steps
- [ ] Enhance planning capabilities (load website specific context)
- [ ] Reduce token consumption (system prompt, DOM state)

### DOM Extraction

- [ ] Enable detection for all possible UI elements
- [ ] Improve state representation for UI elements so that all LLMs can understand what's on the page

### Workflows

- [ ] Let user record a workflow - which we can rerun with browser-use as a fallback
- [ ] Make rerunning of workflows work, even if pages change

### User Experience

- [ ] Create various templates for tutorial execution, job application, QA testing, social media, etc. which users can just copy & paste.
- [ ] Improve docs
- [ ] Make it faster

### Parallelization

- [ ] Human work is sequential. The real power of a browser agent comes into reality if we can parallelize similar tasks. For example, if you want to find contact information for 100 companies, this can all be done in parallel and reported back to a main agent, which processes the results and kicks off parallel subtasks again.

## Contributing

We love contributions! Feel free to open issues for bugs or feature requests. To contribute to the docs, check out the `/docs` folder.

## 🧪 How to make your agents robust?

We offer to run your tasks in our CI—automatically, on every update!

- **Add your task:** Add a YAML file in `tests/agent_tasks/` (see the [`README there`](tests/agent_tasks/README.md) for details).
- **Automatic validation:** Every time we push updates, your task will be run by the agent and evaluated using your criteria.

## Local Setup

To learn more about the library, check out the [local setup 📕](https://docs.browser-use.com/development/local-setup).

`main` is the primary development branch with frequent changes. For production use, install a stable [versioned release](https://github.com/browser-use/browser-use/releases) instead.

---

## Swag

Want to show off your Browser-use swag? Check out our [Merch store](https://browsermerch.com). Good contributors will receive swag for free 👀.

## Citation

If you use Browser Use in your research or project, please cite:

```bibtex
@software{browser_use2024,
  author = {Müller, Magnus and Žunič, Gregor},
  title = {Browser Use: Enable AI to control your browser},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/browser-use/browser-use}
}
```

 <div align="center"> <img src="https://github.com/user-attachments/assets/06fa3078-8461-4560-b434-445510c1766f" width="400"/> 
 
[![Twitter Follow](https://img.shields.io/twitter/follow/Gregor?style=social)](https://x.com/intent/user?screen_name=gregpr07)
[![Twitter Follow](https://img.shields.io/twitter/follow/Magnus?style=social)](https://x.com/intent/user?screen_name=mamagnus00)
 
 </div>

<div align="center">
Made with ❤️ in Zurich and San Francisco
 </div>
