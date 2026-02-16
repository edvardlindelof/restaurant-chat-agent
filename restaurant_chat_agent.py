# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "pydantic-ai>=0.0.10",
#     "httpx",
# ]
# ///

import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return


app._unparsable_cell(
    """
    import httpx
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    from datetime import datetime
    from os import environ

    m_api_url = environ[\"MENU_API_URL\"]
    m_api_key = environ[\"MENU_API_KEY\"]

    model = OpenAIChatModel('gpt-4o-mini')
    agent = Agent(
        model,
        system_prompt=(
            \"You are a helpful restaurant menu assistant. \"
            \"Help users find restaurants and look up menus. Be friendly. \"
            \"You are concise.\"
        ),
    )

    @agent.tool_plain
    def list_restaurants() -> str:
        \"\"\"List available restaurants.\"\"\"
        return \"Available restaurants: indya, bjorkmans, poppels\"

    @agent.tool_plain
    def get_meny(restaurant_name: str) -> str:
        \"\"\"Get menu for a restaurant.\"\"\"
        url = f\"{m_api_url}/api/menus/{restaurant_name}?api_key={m_api_key}\"
        try:
            response = httpx.get(url, timeout=10.0)
            response.raise_for_status()
            return f\"Menu for {restaurant_name}: {response.json()}\"
        except Exception as e:
            return f\"Error: {e}\"

    @agent.tool_plain
    def get_current_date() -> str:
        \"\"\"Get the current day of the week.\"\"\"
        return datetime.now().strftime(\"%A\")

    async def chat_handler(messages):
        \"\"\"Handle chat messages.\"\"\"
        if not messages:
            return None

        user_msg = messages[-1].content
        try:
            result = await agent.run(user_msg)
            return result.output
        except Exception as e:
            return f\"Error: {e}\"

    mo.ui.chat(
        chat_handler,
        prompts=[
            \"What restaurants are available?\",
            \"Show me the menu for indya\",
        ],
    )
    """,
    name="_"
)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
