# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "pydantic-ai>=0.0.10",
#     "httpx",
# ]
# ///

import marimo

__generated_with = "0.19.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    menu_api_url = mo.ui.text(
        label="Menu API Base URL",
        placeholder="https://...",
    )

    openai_key = mo.ui.text(
        label="OpenAI API Key",
        kind="password",
        placeholder="sk-...",
    )

    menu_api_key = mo.ui.text(
        label="Menu API Key",
        kind="password",
        placeholder="your-api-key",
    )

    config = mo.vstack([
        mo.md("### API Configuration"),
        menu_api_url,
        openai_key,
        menu_api_key,
    ])
    config
    return menu_api_key, menu_api_url, openai_key


@app.cell
def _(menu_api_key, menu_api_url, mo, openai_key):
    import httpx
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    from datetime import datetime

    m_api_url = menu_api_url.value
    oai_key = openai_key.value
    m_api_key = menu_api_key.value
    import os
    os.environ['OPENAI_API_KEY'] = oai_key

    if not oai_key or not m_api_key:
        output = mo.md("⚠️ Enter both API keys to start.")
    else:
        model = OpenAIChatModel('gpt-4o-mini')
        agent = Agent(
            model,
            system_prompt=(
                "You are a helpful restaurant menu assistant. "
                "Help users find restaurants and look up menus. Be friendly. "
                "You are concise."
            ),
        )

        @agent.tool_plain
        def list_restaurants() -> str:
            """List available restaurants."""
            return "Available restaurants: indya, bjorkmans, poppels"

        @agent.tool_plain
        def get_meny(restaurant_name: str) -> str:
            """Get menu for a restaurant."""
            url = f"{m_api_url}/api/menus/{restaurant_name}?api_key={m_api_key}"
            try:
                response = httpx.get(url, timeout=10.0)
                response.raise_for_status()
                return f"Menu for {restaurant_name}: {response.json()}"
            except Exception as e:
                return f"Error: {e}"

        @agent.tool_plain
        def get_current_date() -> str:
            """Get the current day of the week."""
            return datetime.now().strftime("%A")

        async def chat_handler(messages):
            """Handle chat messages."""
            if not messages:
                return None

            user_msg = messages[-1].content
            try:
                result = await agent.run(user_msg)
                return result.output
            except Exception as e:
                return f"Error: {e}"

        chat = mo.ui.chat(
            chat_handler,
            prompts=[
                "What restaurants are available?",
                "Show me the menu for indya",
            ],
        )

    chat
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
