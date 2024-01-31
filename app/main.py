import os
import random

import logging
LOG = logging.getLogger(__name__)


from deta import Base

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel  # pylint: disable=no-name-in-module

import discohook

APPLICATION_ID = os.getenv("DISCORD_APP_ID")
APPLICATION_TOKEN = os.getenv("DISCORD_APP_TOKEN")
APPLICATION_PUBLIC_KEY = os.getenv("DISCORD_APP_PUBLIC_KEY")

CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

app = discohook.Client(
    application_id=APPLICATION_ID,
    token=APPLICATION_TOKEN,
    public_key=APPLICATION_PUBLIC_KEY
)

# To serve static images
# app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
async def index():
    with open("./static/index.html") as file:
        return HTMLResponse(file.read())


items_base = Base("items")


@app.command(
    id="",
    name="hello",
    description="Say Hello"
)
async def beep_command(interaction: discohook.Interaction):
    await interaction.response(
        f"Hello, {interaction.author}!"
    )


@app.command(
    id="",
    name="add-item",
    description="Add an item",
    options=[
        discohook.StringOption(name='item', description='An Item', required=True, max_length=50),
    ]
)
async def add_item_command(interaction: discohook.CommandInteraction):

    options = dict()
    for opt in interaction.command_data.options:
        options[opt['name']] = opt['value']

    items_base.put(1, key=options['item'])

    await interaction.response(
        f"{options['item']} added to the list",
        ephemeral=True,
    )


async def handle_random_item():
    items = items_base.fetch()

    if items.count:
        msg = random.choice(items.items)
        resp = await app.send_message(CHANNEL_ID, content=msg)
        LOG.warning(f"send_message response: {resp}")


class Event(BaseModel):
    event: dict


@app.post("/__space/v0/actions")
async def actions(item: Event):
    LOG.warning(f"Received event: id={item.event['id']}")
    if item.event['id'] == 'random_item':
        await handle_random_item()



@app.get("/api/items")
async def get_items():
    # Fetch all items from the Base.
    items = items_base.fetch()
    # Return the items as JSON.
    return items.items
