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
    if len(pips) > 0:
        fields["Food Pips"] = pips
    register_item(name, f"Food ({ftype})", size, description, fields)

# Food
register_food("Blue Fruit", "Small", "1", "Plant", "The pupae of a bug which resembles a plant. They dangle from ceilings on black vines.")
register_food(
    "Bubble Fruit", "Small", "1", "Plant", "Acts as an inedible rock until popped, by immersing it in water for one round.")
register_food("Dandelion Peach", "Small", "1", "Plant", "Puffy plants on the end of cyan stalks, growing in regions in the clouds.")
register_food("Glow Weed", "Small", "1", "Plant", "Provides light within 3 distance of itself, but only when underwater.", {"Trade Value": "3"})
register_food("Gooieduck", "Small", "2", "Plant", "Requires 2 actions to eat instead of 1.\nWhile held, Worm Grass you enter is stunned.", {"Trade Value": "1"})
register_food(
    "Lilypuck", "Medium", "1", "Plant",
    "Lilies which grow on the surface of underground water bodies, and held by roots which extend underwater.\
    These roots are sharp and glasslike, letting them serve as a one-use spear.",
    {"Trade Value": "4", "Impact": "On first throw, 2d4 + Power damage."})
register_food("Slime Mold", "Small", "1-2", "Plant", "Provides light within 1 distance of itself.")
register_food(
    "Fire Egg", "Small", "1", "Any", "Boom.",
    {"Impact (Volatile)": "Sticks to anything it impacts. Then, one round later, it explodes,\
     dealing 6d6 damage at the point of impact, and half of that to all creatures within 6 distance of the impact point."})
register_food("Neuron Fly", "Small", "1", "Any", "Gain the luminescent adaptation if you don't have it.")
register_food("Seed", "Small", "1", "Any", "The popped kernels of popcorn plants. While hard to access, they're palatable to anyone.")
register_food("Mushroom", "Small", "", "Any", "Gain the haste condition for 4 rounds. The duration can stack.", {"Trade Value": "2"})
register_food("Karma Flower", "Small", "", "Any", "Gain the reinforcement condition.", {"Trade Value": "5"})
register_food("Eggbug Egg", "Small", "1", "Egg", "The eggs of the skittish eggbug, usually dropped in clusters.")
register_food(
    "Lizard Egg", "Small", "4", "Egg",
    "If kept safe from harm, eventually hatches into a lizard hatchling, that matches the colour of the egg.\
    The lizard is considered tamed to the group who was present during hatching.")
register_food(
    "Jellyfish", "Small", "1", "Meat",
    "A saucer shaped marine animal with long tentacles, free floating in large bodies of water.\
    They may deal a slight shock to creatures in contact with them, and can be used as an explosive stunning weapon.",
    {"Impact": "Stuns anything impacted, and recharges electrical equipment hit by it."})
# Weapons
register_item(
    "Beehive", "Weapon", "Small",
    "The impact effect will trigger if the beehive isn't pacified with spore puff gas before trying to pick it up.",
    {"Impact": "Anyone within 5 distance of the impact is pinned. (DC 3 to escape)"})
register_item(
    "Bomb", "Weapon", "Small",
    "Will not explode if thrown underwater.",
    {"Trade Value": "3", "Impact (Volatile)": "Explosion that deals 4d6 damage at the point of impact, and half of that to creatures within 5 distance of the impact point."})
register_item("Bow", "Weapon", "Medium", "While held in a hand, the impact damage of thrown spears is increased by one die.")
register_item(
    "Dagger", "Weapon", "Medium",
    "A sharpened piece of rebar equipped with a small handle. Its form factor allows it to be effective as both a thrown and melee weapon.",
    {"Impact/Strike": "Deals 2d4 + power damage."})
register_item(
    "Firebush", "Weapon", "Small",
    "A bush of explosive nuts. While not lethal, it can knock anyone in range unconscious from the noise.",
    {"Trade Value": "2", "Impact (Volatile)": "Explosion which knocks creatures unconscious for one round if within 4 distance."})
register_item(
    "Flashbang", "Weapon", "Small",
    "Inedible luminescent fruit which grows on purple stems in the darkest parts of the world.\
    The intense light released by their destruction can create a massive pulse of light to blind adversaries.",
    {"Trade Value": "2", "Impact (Volatile)": "Anyone who is able to see the flash must succeed a DC 2 perception check or receive the blinded condition for two rounds."})
register_item(
    "Rock", "Weapon", "Small",
    "It's not flashy, but it can help in dire situations.",
    {"Trade Value": "1", "Impact": "Deals 1 + power damage, and a hit creature loses one action on their next turn.\n\
     If a lizard is hit, they must succeed a DC 2 endurance skill check or be knocked unconscious for one round."})
register_item(
    "Snowball", "Weapon", "Small",
    "Useful for quickly cooling a creature.",
    {"Impact (Volatile)": "A hit creature loses one action on their next turn, and their warmth pips are reduced by 1d4."})
register_item(
    "Spear", "Weapon", "Medium",
    "Can be broken into two half-spears if excessive force is applied to it.",
    {"Trade Value": "3", "Impact": "Deals 2d6 + power damage, and embeds itself."})
register_item(
    "Explosive Spear", "Weapon", "Medium",
    "A length of rebar wrapped with a bundle of fire powder. Extremely powerful, but also dangerous to handle.",
    {"Trade Value": "4", "Impact (Volatile)": "Deals 2d6 + power damage, and embeds itself. Then, one round later, it explodes.\n\
     The explosion deals 3d6 damage at the point of impact, and half of that to creatures within 3 distance of the impact point."})
register_item(
    "Electric Spear", "Weapon", "Medium",
    "Electric spears contain 2d6 + 1 charges. Add 1 trade value for every 4 charges an electric spear has.",
    {"Trade Value": "3+", "Impact": "Deals 2d6 + power damage and embeds itself. It also has these effects in order.\n\
     1. If charged, then 1 charge is spent to stun anything hit.\n\
     2. If it hits a source of electricity, charges are restored to maximum if uncharged, or the spear is destroyed if it already has charges.\
     (e.g. Jellyfish, Centipedes, Inspectors, Flux Condenser Coils)\n\
     3. If charged and in water, then all charges are spent to stun and deal 3d6 damage to anything in the water which is within 10 distance of the spear."})
register_item(
    "Flaming Spear", "Weapon", "Medium",
    "Becomes a regular spear if immersed in or hit by water.",
    {"Trade Value": "4", "Impact": "Deals 2d6 + power damage, embeds itself, and sets the target on fire."})
register_item(
    "Icicle Lance", "Weapon", "Medium",
    "Melts if exposed to flames.",
    {"Impact": "Deals 2d6 + power damage, embeds itself, and freezes the target."})
register_item(
    "Half-Spear", "Weapon", "Medium",
    "A spear that has been snapped in half from a lizard's bite or some other intense force. While less powerful, it still has some combat potential.",
    {"Trade Value": "1", "Impact": "Deals 2d4 + power damage, and embeds itself."})
register_item(
    "Singularity Bomb", "Weapon", "Small",
    "Will not explode if thrown underwater.",
    {"Trade Value": "10", "Impact (Volatile)": "One round later, pulls in anything within 10 distance of the impact point.\
     Anything pulled in is destroyed. In addition, the shockwave of the blast will recharge electrical equipment within 20 distance of the impact point."})
register_item(
    "Sword", "Weapon", "Medium",
    "Multiple adjacent targets can be attacked with a single action, making individual attack and damage rolls against each.\
    The damage to all targets is reduced by 3 for each target past the first, to a minimum of 1.",
    {"Trade Value": "5", "Strike": "Deals 2d6 + power damage."})
# Other
register_item("Batnip", "Other", "Small", "Batflies are drawn towards the batnip.", {"Trade Value": "2"})
register_item(
    "Bubble Weed", "Other", "Small",
    "|▶| You, or an adjacent or carried/carrying creature takes a breath from the bubble weed, restoring breath to maximum.\
    Can be used twice before wilting away.\nWhen a breath is taken, all leeches within 3 distance are stunned for one round.",
    {"When Cooked": "+1 breath capacity for the rest of the cycle."})
register_item(
    "Centipede Plate", "Other", "Medium",
    "When trying to dodge an attack, if you and the attacker have equal successes, the centipede plate absorbs the damage.\
    A centipede plate will break after receiving 2d6 x 10 damage.")
register_item("Inspector Eye", "Other", "Small", "Highly valued for trades and tolls.", {"Trade Value": "20"})
register_item("Lantern", "Other", "Small", "Provides light within 4 distance of itself.", {"Trade Value": "3"})
register_item(
    "Heated Lantern", "Other", "Small",
    "Provides light within 4 distance of itself.\n\
    Provides +1 warmth pip each round while carried, if warmth pips are below 0.",
    {"Trade Value": "3"})
register_item(
    "Mass Rarefaction Cell", "Other", "Large",
    "|▶| Activate the cell, tripling jump height for 3 rounds. After use, it requires 3 rounds to recharge.\n\
    Its shell is extremely durable, but extreme forces (such as a Leviathan's jaws) can shatter it.\n\
    If shattered, it will explode, destroying everything including itself within 20 distance of itself.")
register_item(
    "Noodlefly Egg", "Other", "Medium",
    "Noodleflies are angered while this is held. If carried to a shelter, it will hatch into 2 tamed infant noodleflies next cycle.",
    {"When Cooked": "+3 food pips."})
register_item("Pearl", "Other", "Small", "Highly valued for trades and tolls.", {"Trade Value": "7"})
register_item(
    "Pearl", "Other", "Small",
    "Highly valued for trades and tolls.\
    Pearls also store writings or images which can be extracted by an iterator or someone with the right knowledge and tools.",
    {"Trade Value": "10"})
register_item(
    "Spore Puff", "Other", "Small",
    "Spore Puffs draw in Rain Deer, who will kneel to eat them, providing an opportunity to board them.",
    {"Trade Value": "2", "Impact": "If it's the first time this spore puff has been thrown, it releases gas within 5 distance of itself for five rounds.\
     Any arthropod or centipede takes 2d4 damage each round they spend in the gas."})
# Body
register_item("Cloak", "Body", "Small", "Reduces the tier of extreme temperatures experienced by 1. Doesn't help with cold conditions if wet.")
register_item("Pouches", "Body", "Medium", "Has three \"pouch\" item slots. These can store small items.")
register_item(
    "Aquapede Shell", "Body", "Large",
    "Electrical attacks have their damage reduced by 4 instead, and cannot stun the wearer.\nMovement speed in water is increased by 2.",
    {"Damage Reduction": "1"})
register_item(
    "Centipede Shell", "Body", "Large",
    "Electrical attacks have their damage reduced by 4 instead, and cannot stun the wearer.",
    {"Damage Reduction": "2", "Weight": "1"})
register_item(
    "Centiwing Shell", "Body", "Large",
    "Electrical attacks have their damage reduced by 4 instead, and cannot stun the wearer.\n\
    Damage taken when landing from a long fall is reduced by 4.",
    {"Damage Reduction": "1"})
register_item(
    "Red Centipede Shell", "Body", "Large",
    "Electrical attacks have their damage reduced by 4 instead, and cannot stun the wearer.",
    {"Damage Reduction": "3", "Weight": "2"})
register_item(
    "Metal Shell", "Body", "Large",
    "Does not provide any protection against electricity.",
    {"Damage Reduction": "3", "Weight": "2"})
register_item(
    "Wooden Shell", "Body", "Large",
    "The armour is destroyed if it is hit by fire.",
    {"Damage Reduction": "2"})
register_item(
    "Hat", "Head", "Medium",
    "+1 influence while worn. This can bring influence beyond its usual maximum.\nReduces the tier of high temperatures experienced by 1.")
register_item(
    "Headset", "Head", "Medium",
    "Can speak with allies wearing a headset who are in the same region.\nEar protection, and provides immunity to sound-based attacks.")
register_item("Head Lantern", "Head", "Small", "Provides light within 4 distance of itself.", {"Trade Value": "3"})
register_item(
    "Chieftain Scavenger Mask", "Face", "Medium",
    "+2D for influence checks on scavengers who can see the mask.\n\
    +1D when trying to intimidate lizards who can see the mask. Doesn't work on red lizards, and green lizards are pacified instead of terrified.",
    {"Trade Value": "∞"})
register_item(
    "Elite Scavenger Mask", "Face", "Medium",
    "+1D for influence checks on scavengers who can see the mask.\n\
    +1D when trying to intimidate lizards who can see the mask. Doesn't work on red lizards, and green lizards are pacified instead of terrified.",
    {"Trade Value": "10"})
register_item("Eyepatch", "Face", "Small", "Can cover a chosen eye. Effects of darkness on you are halved if the eye covered is functional.")
register_item(
    "Vulture Mask", "Face", "Medium",
    "+1D when trying to intimidate lizards who can see the mask. Doesn't work on red lizards, and green lizards are pacified instead of terrified.",
    {"Trade Value": "10"})
register_item(
    "King Vulture Mask", "Face", "Medium",
    "+2D when trying to intimidate lizards who can see the mask. Doesn't work on red lizards.",
    {"Trade Value": "10"})
register_item(
    "Backpack", "Back", "Large",
    "You cannot wear more than one backpack, regardless of type.\nHas four \"pouch\" item slots. These can store small items.")
register_item(
    "Large Backpack", "Back", "Large",
    "You cannot wear more than one backpack, regardless of type.\nHas four \"pouch\" item slots. These can store small items.",
    {"Weight": "1"})
register_item("Water Fins", "Back", "Large", "Movement speed in water is increased by 2.")

@app.load
@discohook.command.slash(
    name="item",
    description="Get information about an item",
    options=[discohook.Option.string(name="item", required=True, description="Item name")]
)
async def item_command(interaction: discohook.Interaction, item: str):
    n = None
    prevMatches = []
    for x in range(len(item.lower())-1, 0, -1):
        if part in items:
            n = part
            break
        part = item[0:x]
        matches = list(filter(lambda other: part in other, items.keys()))
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
    if n in items:
        i = items[n]
        e = discohook.Embed(title=i["name"], description=i["description"])
        e.add_field(name="Type", value=i["kind"], inline=True)
        e.add_field(name="Size", value=i["size"], inline=True)
        for x in i["fields"]:
            e.add_field(name=x, value=i["fields"][x], inline=True)
        await interaction.response.send(embed=e)
    else:
        await interaction.response.send(content="I couldn't find that item.")

async def index(request: Request):
    return JSONResponse({"success": True}, status_code=200)

app.add_route("/", index, methods=["GET"], include_in_schema=False)
