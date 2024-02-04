import os

import logging

from starlette.requests import Request
from starlette.responses import JSONResponse

import discohook


APPLICATION_ID = os.getenv("DISCORD_APP_ID")
APPLICATION_TOKEN = os.getenv("DISCORD_APP_TOKEN")
APPLICATION_PUBLIC_KEY = os.getenv("DISCORD_APP_PUBLIC_KEY")
APPLICATION_PASSWORD = os.getenv("DISCORD_APP_PASSWORD")

LOG_CHANNEL_ID = os.getenv("DISCORD_LOG_CHANNEL_ID")

app = discohook.Client(
    application_id=APPLICATION_ID,
    token=APPLICATION_TOKEN,
    public_key=APPLICATION_PUBLIC_KEY,
    password=APPLICATION_PASSWORD,
    default_help_command=True,
)

SUCCESS = 'success'

if LOG_CHANNEL_ID:

    import asyncio

    class DiscordLog:
        def __init__(self, client, channel_id):
            self._client = client
            self._channel_id = channel_id

        def _log(self, msg):
            # loop = self._client.http.session.loop
            asyncio.create_task(self._client.send(self._channel_id, msg))

        def warning(self, msg):
            self._log(msg)

        def info(self, msg):
            self._log(msg)

    LOG = DiscordLog(app, LOG_CHANNEL_ID)

else:
    LOG = logging.getLogger(__name__)


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
