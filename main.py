import os
import aiohttp
import asyncio
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
import discohook
from discohook.middleware import SingleUseSessionMiddleware

APPLICATION_ID = os.getenv("DISCORD_APP_ID")
APPLICATION_TOKEN = os.getenv("DISCORD_APP_TOKEN")
APPLICATION_PUBLIC_KEY = os.getenv("DISCORD_APP_PUBLIC_KEY")
APPLICATION_PASSWORD = os.getenv("DISCORD_APP_PASSWORD")

app = discohook.Client(
    application_id=APPLICATION_ID,
    token=APPLICATION_TOKEN,
    public_key=APPLICATION_PUBLIC_KEY,
    password=APPLICATION_PASSWORD,
    default_help_command=True,
    middleware=[Middleware(SingleUseSessionMiddleware)],
)

@app.load
@discohook.command.slash(name="hello", description="Say hello")
async def hello_command(interaction: discohook.Interaction):
    username = interaction.author.global_name
    await interaction.response.send(content=f"Hello, {username}!")

items = {}
def register_item(name: str, description: str, fields: dict):
    item = {"name": name, "description": description, "fields": fields}
    items[name.lower()] = item

register_item("Batnip", "Batflies are drawn towards the batnip.", {"size": "Small"})

@app.load
@discohook.command.slash(
    name="item",
    description="Get information about an item",
    options=[discohook.Option.string(name="item", required=True, description="Item name")]
)
async def item_command(interaction: discohook.Interaction, item: str):
    i = items[item.lower()]
    if i:
        e = discohook.Embed(title=i["name"], description=i["description"])
        for x in i["fields"]:
            e.add_field(name=x, value=i["fields"][x], inline=True)
        await interaction.response.send(embed=e)
    else:
        await interaction.response.send(content="I couldn't find that item.")
    

"""
@app.load
@discohook.command.slash(
    name="test-set",
    description="test set command",
    options=[
            discohook.Option.string(
                name="value",
                required=True,
                description="Value to set",
            ),
        ]
    )
"""

async def index(request: Request):
    return JSONResponse({"success": True}, status_code=200)

app.add_route("/", index, methods=["GET"], include_in_schema=False)
