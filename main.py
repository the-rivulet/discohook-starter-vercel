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
        request.app.http.session = aiohttp.ClientSession('https://discord.com', loop = asyncio.get_event_loop())
        return await call_next(request)

app = discohook.Client(
    application_id=APPLICATION_ID,
    token=APPLICATION_TOKEN,
    public_key=APPLICATION_PUBLIC_KEY,
    password=APPLICATION_PASSWORD,
    default_help_command=True,
    middleware=[Middleware(CustomHeaderMiddleware)],
)

# Set before invoke (if lifespan didn't work on serverless instance)
#@app.before_invoke()
#async def before_invoke(interaction): # force new sessions every request is the only way to fix it atm
#    if interaction.kind != discohook.InteractionType.ping:
#        loop = asyncio.get_event_loop()
#        await app.http.session.close()
#        app.http.session = aiohttp.ClientSession('https://discord.com', loop = loop)


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


async def index(request: Request):
    return JSONResponse({"success": True}, status_code=200)

app.add_route("/", index, methods=["GET"], include_in_schema=False)
