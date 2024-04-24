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
def register_item(name: str, kind: str, size: str, description: str, fields: dict = {}):
    item = {"name": name, "kind": kind, "description": description, "size": size, "fields": fields}
    items[name.lower()] = item
def register_food(name: str, size: str, pips: str, ftype: str, description: str, fields: dict = {}):
    food = {"Food Pips": str(pips)}
    register_item(name, f"Food ({ftype})", size, description, {**food, **fields})

# Food
register_food("Blue Fruit", "Small", "1", "Plant", "A slugcat's staple food.")
register_food("Bubble Fruit", "Small", "1", "Plant", "Inedible until immersed in water.")
register_food("Dandelion Peach", "Small", "1", "Plant", "Found in the Sky Islands.")
register_food("Glow Weed", "Small", "1", "Plant", "Has a 3 distance glow while in water.")
register_food("Gooieduck", "Small", "2", "Plant", "Requires 2 actions to eat.\nWhile held, touched worm grass is stunned.")
register_food("Lilypuck", "Small", "1", "Plant", "Sharp!", {"Impact": "On first throw, 2d4 + Power damage."})
register_food("Slime Mold", "Small", "1-2", "Plant", "Has a 1 distance glow.")
# Other Items
register_item("Batnip", "Other", "Small", "Batflies are drawn towards the batnip.", {"Value": "2"})
register_item(
    "Bubble Weed", "Other", "Small",
    "|▶| You / anyone adjacent takes a breath from it, restoring all air. Wilts after two uses.\n\
    When a breath is taken, all leeches within 3 distance are stunned for one round.",
    {"When Cooked": "+1 breath capacity for the rest of the cycle."})
register_item(
    "Centipede Plate", "Other", "Medium",
    "When trying to dodge, if you and attacker have equal successes, this blocks the hit.\n\
    This plate has 2d6 x 10 HP, and will break when it runs out.")
register_item("Inspector Eye", "Other", "Small", "Highly valued for trades and tolls.", {"Value": "20"})
register_item("Lantern", "Other", "Small", "Provides light within 4 distance of itself.", {"Value": "3"})
register_item(
    "Heated Lantern", "Other", "Small",
    "Provides light within 4 distance of itself.\n\
    Provides +1 warmth pip each round while carried, if warmth pips are below 0.",
    {"Value": "3"})
register_item(
    "Mass Rarefaction Cell", "Other", "Large",
    "|▶| Activate the cell, tripling jump height for 3 rounds. After use, it requires 3 rounds to recharge.\n\
    Leviathan jaws or iterators can shatter it, destroying everything and itself within 20 distance.")
register_item(
    "Noodlefly Egg", "Other", "Medium",
    "Angers noodleflies while held. Hatches into 2 tamed noodleflies during hibernation.",
    {"When Cooked": "+3 food pips."})
register_item("Pearl", "Other", "Small", "Highly valued for trades and tolls.", {"Value": "7"})
register_item(
    "Pearl", "Other", "Small",
    "Highly valued for trades and tolls. Can also store data, readable by iterators, lorekeepers, and similar.",
    {"Value": "10"})
register_item(
    "Spore Puff", "Other", "Small",
    "Rain Deer will head over and kneel to eat these.",
    {"Impact": "On first throw, gas emitted within 5 distance of itself for 5 rounds.\
     Arthropods and centipedes in the gas take 2d4 damage per round. Also pacifies beehives."})


@app.load
@discohook.command.slash(
    name="item",
    description="Get information about an item",
    options=[discohook.Option.string(name="item", required=True, description="Item name")]
)
async def item_command(interaction: discohook.Interaction, item: str):
    n = None
    prevMatches = []
    for x in range(len(item-1), 0, -1):
        part = item[0:x]
        matches = filter(lambda m: m[0:x] == part, items.keys())
        if len(matches) == 0:
            if len(prevMatches) > 0:
                n = prevMatches[0]
            break
        elif len(matches) == 1:
            n = matches[0]
            break
        prevMatches = matches
    if n is None and len(prevMatches) > 0:
        n = prevMatches[0]
    i = items[n]
    if i:
        e = discohook.Embed(title=i["name"], description=i["description"])
        e.add_field(name="Type", value=i["kind"], inline=True)
        e.add_field(name="Size", value=i["size"], inline=True)
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
