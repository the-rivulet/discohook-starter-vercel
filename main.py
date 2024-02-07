import os

import aiohttp
import asyncio

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

import discohook

APPLICATION_ID = os.getenv("DISCORD_APP_ID")
APPLICATION_TOKEN = os.getenv("DISCORD_APP_TOKEN")
APPLICATION_PUBLIC_KEY = os.getenv("DISCORD_APP_PUBLIC_KEY")
APPLICATION_PASSWORD = os.getenv("DISCORD_APP_PASSWORD")


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        await request.app.http.session.close()
        request.app.http.session = aiohttp.ClientSession('https://discord.com')
        return await call_next(request)

app = discohook.Client(
    application_id=APPLICATION_ID,
    token=APPLICATION_TOKEN,
    public_key=APPLICATION_PUBLIC_KEY,
    password=APPLICATION_PASSWORD,
    default_help_command=True,
    middleware=[Middleware(CustomHeaderMiddleware)],
)


@app.load
@discohook.command.slash(
    name="hello",
    description="Say Hello"
)
async def beep_command(interaction: discohook.Interaction):
    username = interaction.author.global_name
    await interaction.response.send(
        f"Hello, {username}!"
    )

@app.load
@discohook.command.slash(
    name="test",
    description="test command"
)
async def test_command(interaction: discohook.Interaction):
    username = interaction.author.global_name
    await interaction.response.defer()
    await asyncio.sleep(8)
    interaction.response.followup(str(id(asyncio.get_running_loop())))

async def index(request: Request):
    return JSONResponse({"success": True}, status_code=200)

app.add_route("/", index, methods=["GET"], include_in_schema=False)
