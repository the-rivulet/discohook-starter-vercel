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

def look_for(l: dict, target: str):
    matches = list(filter(lambda other: target.lower() in other, l.keys()))
    while len(matches) == 0 and len(target) > 0:
        target = target[:-1]
        matches = list(filter(lambda other: target.lower() in other, l.keys()))
    if len(matches) > 0:
        return sorted(matches, key=len)[0]
    return None

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
    register_item(name, f"Food ({ftype})", size, description, {**fields, "Food Pips": pips})

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
register_item("Mushroom", "Food (Any)", "Small", "Gain the haste condition for 4 rounds. The duration can stack.", {"Trade Value": "2"})
register_item("Karma Flower", "Food (Any)" "Small", "Gain the reinforcement condition.", {"Trade Value": "5"})
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
    match = look_for(items, item)
    if match is not None:
        i = items[match]
        e = discohook.Embed(title=i["name"], description=i["description"])
        e.add_field(name="Type", value=i["kind"], inline=True)
        e.add_field(name="Size", value=i["size"], inline=True)
        for x in i["fields"]:
            e.add_field(name=x, value=i["fields"][x], inline=True)
        await interaction.response.send(embed=e)
    else:
        await interaction.response.send(content="I couldn't find that item.")

rules = {
    # Core
    "overview": "Rain World is a post-apocalyptic wasteland, with creatures struggling to survive atop the metallic ruins and mountains of trash.\
    The world is regularly blanketed by deadly rainstorms, powerful enough to crush or drown almost anyone who isn't in a sealed off shelter.\
    You play as nomadic creatures who are both predator and prey. Attempting to survive in the wastes, you will encounter many perils.\n\
    Gameplay focuses on finding creative solutions to problems using your unique skills. Actions have a high chance to fail\
    unless you are skilled in them, so you are encouraged to specialize and use teamwork in order to make up for the other characters' shortcomings.\n\
    Campaigns consist of a Game Master (GM), which runs the world and controls the creatures, and a number of players, who act as characters which they create.\n\
    Both the GM and the players require a set of polyhedral dice, with it being recommended that you have multiple D6s and D4s.\
    Players also need to make a character sheet. If the GM wishes to use a map, it is recommended to use a side view map in order to make better use of movement\
    and to more accurately imitate Rain World.\n\
    While these rules are provided to help run the system, the GM is advised to bend these rules in accordance to what they and their players consider would be most fun.",
    "checks": "Checks are usually an attempt to perform a difficult task, while contests are an attempt to perform a difficult task\
    that is being opposed by another creature, such as making an attack.\nFor checks and contests, you roll a number of D6s equal to\
    2 + your skill. Rolling a 4, 5, or 6 means that that die is a success. For example, if you had 3 Comprehension, you would roll 5D (5 D6s).\
    If your number of successes is 1 below the DC (or below the opposing creature's number of successes in a contest), you may opt to partially succeed instead.\
    If you choose to do this you will succeed at the action, however it will be at a cost.\nWhen making a check, a relevant skill is chosen by the GM.\
    They also determine the Difficulty Class (DC) of the check, typically ranging from 1 (being very easy) to 4 (being very hard).\
    In order to pass a check, the number of successes must match or surpass the DC.\nContests are a variant of a check, however they use a contested roll instead of a DC.\
    Both creatures involved in it make a check using the relevant skill. The creature with the higher number of successes succeeds, while the one with less fails.\
    In the event of a tie, the initiator wins.",
    "carrying": "You can spend an action to mount or dismount another creature, or vice versa. How this resolves depends on the size of the two creatures:\n\
    * A creature that's two or more sizes smaller can be carried in a hand or back slot.\n\
    * A creature that's one size smaller can be carried in two hand slots, or a back slot.\n\
    * A creature that's the same size can be carried using every back slot.\n\
    Anyone mounted will move with who is carrying them.",
    "dragging": "You can grab a willing or unconscious creature with every hand slot to drag them with you. You will both move at your speed.\
    However, each size category you are smaller than the creature you're dragging will cut your speed in half.",
    "cooking": "Cooking requires plenty of time, and a source of heat, such as a fire. With cooking, two things can be accomplished:\n\
    * Cook a corpse (Usually DC 2)\n\
    * Merge two or more ingredients into a single meal item. (DC equal to the ingredient count)\n\
    Ingredients can be one food pip from a corpse, a food item, or an item with an effect when cooked. Meals are not ingredients.\
    If multiple identical meals are being created, only one check is needed for the batch of them.\n\
    Results of a cooking skill check (usually uses comprehension):\n\
    * Success adds 1 food pip to the result.\n\
    * Partial success cooks successfully, but without a bonus pip.\n\
    * Failure ruins half the ingredients used / half the corpse being cooked.\n\
    |▶▶| Eat a meal, giving all of the \"effects when eaten\" and cooked effects the items which make it up have.",
    "crafting": "Crafting requires a relevant skill check and enough time to put the items together. The results are as follows:\n\
    * Success: The item is created without issue.\n\
    * Partial Success: The item is created, but has an issue that must be worked around.\n\
    * Failure: Nothing is produced, and one of the items is destroyed. (Crafter's choice)",
    "death": "Upon death, a creature loses 1 karma, and wakes up at the start of the next cycle in their last safe resting place.\
    For player characters, they wake up in the next shelter the group enters (unless the entire group is wiped out).\n\
    If a creature dies at 1 karma, they disconnect from the cycles the rest of the group experiences, and so a new character must be created.",
    "karma gates": "These are colossal airlocks which separate the regions of Rain World from each other. These gates will only open once per cycle,\
    when a creature stands within the chamber, who has at least as much Karma as the symbol on the wall represents.\
    Karma Gates may have a different symbol when approaching it from the other side.\n\
    When a Karma gate is activated, the exterior door on either side closes after a one round delay, and steam is vented through the chambers as a decontaminant on the next round.\n\
    Then, the interior door opens, and waits for all living creatures to pass through before closing. The exterior doors will reopen one round after the interior door closes.\
    The Karma gate will then be inoperable for the rest of the cycle.",
    "pipes": "Pipes are shortcuts between two places, marked with an arrow or a set of three lines.\n\
    A creature next to a pipe can enter it, and appear at the destination at the start of their next turn. They cannot make actions or use movement while travelling through a pipe.",
    "shelters": "Scattered around Rain World are advanced shelters from a lost age. They feature thick metallic walls and automatic water drainage systems.\n\
    These shelters are usually used for storage and hibernation, being able to comfortably house an entire family of slugcats.\
    There is also the occasional larger shelter within trains or as a pair of massive doors, which could conceivably support a community of families (assuming food could be taken care of).\n\
    Hibernation is not restricted to shelters, but can be done anywhere that is safe from the rain.\n\
    Healing: While inside a shelter, creatures can convert 1 food pip into 2 HP as many times as they like.\
    This cannot be used if a hostile creature is within the shelter, or if the shelter is broken.\n\
    Hibernation: When hibernating, lose food pips equal to your requirement, and gain 1 karma.\n\
    * Regain HP by half of your maximum, rounded down.\n\
    * Regain all of your Blessings.\n\
    * If you hibernate with zero pips, you die.\n\
    * If the pip reduction brings your food pips into the negatives, set them to 0 and receive the starvation condition.\n\
    Shelter Breakage: Shelters can occasionally malfunction. When they do, the shelter doors are forced open, allowing water to flood some or all of the shelter.\
    Anyone inside will need to seek out another shelter, while evading regular downpours.",
    "toll passages": "Some areas are guarded and require the group to be processed in order to proceed.\
    Typically, such guarded checkpoints have several creatures of one species, all armed with the best weapons they have access to.\
    They may attack those who try to cross without paying, unless the people crossing are trusted by the guards.\n\
    Payment required typically must reach a trade value of 10. Keep in mind that different groups may value items differently from this,\
    and that players may want to make influence checks to lower or bypass the price.",
    "passages": "When you have completed a major objective, your “passage” count increases by 1. Choose from one of these bonuses when this occurs:\n\
    * +2 to one skill of your choice.\n\
    * +1 to two different skills of your choice.\n\
    * +1 to one skill of your choice, and gain an adaptation of your choice.\n\
    This cannot bring skills above the limit, which is usually 5.",
    "inventory": "Your inventory is as follows:\n\
    * Two hand slots, able to hold any small or medium item.\n\
    * Large items require all hand slots to carry.\n\
    * One back slot, able to carry any weapon.\n\
    * One mouth slot, able to carry any small item.\n\
    * One body slot, which carries a body item.\n\
    * One head slot, which carries a head item.\n\
    * One face slot, which carries a face item.\n\
    Some adaptations may provide additional item slots.\n\
    To manage your inventory:\n\
    * |▶| Drop or pick up an item.\n\
    * |▶| Swap the contents of two inventory or equipment slots with each other. \n\
    * |▶| With an adjacent creature, give or take an item in the hand. An opposing power check is required if they are unwilling.\
    Willing or not, the other creature does not spend an action as a part of the exchange.",
    # Environment
    "acid": "A creature takes 2d4 damage upon moving into acid, or starting their turn within it. This damage counts as explosive damage.",
    "darkness": "Dark conditions limit the abilities of those who rely on sight. Anyone in a dark location gets -1D on any action which requires sight,\
    such as when trying to hit someone with a thrown object.Anyone who is in total darkness will also receive the blinded condition.",
    "falling": "Creatures fall at the end of their turn if they cannot fly and they're not in water, on ground they can walk on, or hanging onto a pole.\n\
    On landing, a creature will take 1 damage for every point of distance they fell beyond 10.\n\
    A creature can use an agility skill check to reduce the damage. Each success drops the damage by 1.\n\
    If a creature lands on another, half of the fall damage is transferred from the faller to the creature fallen on, rounded up.\
    One extra point of damage is transferred for every point of size the faller has.",
    "extreme temperatures": "Warmth pips change each round, dependent on the environment:\n\
    * Normally, they shift 1 pip towards 0 each round.\n\
    * In a cold environment, the warmth pips are reduced by the tier of the cold.\n\
    * In a hot environment, the warmth pips are increased by the tier of the heat.\n\
    When a creature's warmth is past 5 + Endurance (in either direction), their speed is cut in half and they get -1D to all checks.\n\
    Whenever a creature's warmth moves beyond 8 (in either direction), they lose HP equal to the difference from 8, reduced by their Endurance.\n\
    Karma gates' steam blasts will increase warmth pips by 4 if a creature is hit by it. Any creature within a karma gate may choose to avoid the steam blast if they prefer.",
    "the rain": "At the end of a cycle, deadly rain will begin to fall. The rain causes gradually worsening effects to those directly exposed to it.\n\
    * After 3 rounds, -1D to perception checks.\n\
    * 3 rounds later, -2D to perception checks, and -1D to all other checks.\n\
    * 3 rounds later, the effects above apply, but the rain also deals 1d6 damage each round.\n\
    * 3 rounds later, the damage doubles to 2d6.\n\
    The world also floods significantly.\nIf sufficiently far from an iterator, deep underground, or above the clouds, some or all of the effects may not occur.",
    "underwater & drowning": "A creature can only remain underwater for as many rounds as their breath capacity. Afterwards, they take 1 damage per round,\
    with the damage rising by 1 for each consecutive round the creature remains without air. Damage stops when the creature is able to breathe again.\
    A creature's breath is replenished only when they spend a full round above water.\n\
    Anything thrown underwater has its damage reduced by half, and its range limited to 5 distance.",
    # Combat
    "attacking": "An attack is counted as any action which has an impact or strike effect, and/or applies a negative condition to another creature.\
    For attacks whose damage is increased by a skill, a creature can only apply this increase to the damage of one attack each round.",
    "turns & rounds": "One round consists of every creature taking their turn.\n\
    All player creatures take their turn, then the rest of the creatures take their turn. The players decide which order they take their turns in,\
    and the GM decides which order the other creatures do for them.\n\
    Creatures can perform up to two actions, in addition to movement up to their speed.",
    "movement": "Creatures can move from one spot to another at any time during their turn, as long as the total distance doesn't exceed their speed, and they don't stop/pass through any solid objects.\n\
    Movement can be done in any direction while in water, along poles, or in crawlspaces (tunnels which are one space wide).\
    Keep in mind moving one diagonal space counts as 2 spaces of movement. Otherwise, movement is horizontal for non-flying creatures.\n\
    While on the ground, a jump can be made. When jumping, follow these steps in order:\n\
    1. They move forwards and upwards by up to their jump height.\n\
    2. They move forwards by up to their jump height.\n\
    3. They may move further forwards, but dropping 1 tile for every horizontal tile moved.\n\
    And, in the air, falling can be done. (Or is automatic at the end of a creature's turn, if they're not flying or holding a pole,\
    or if the creature's turn is skipped due to being unable to act). Falling uses no movement,\
    but can't be stopped until they land on something, possibly taking fall damage.",
    "grappling": "Grapples can be fired at any target in a straight line, as long as it's within the range of the grapple.\n\
    * If the target is a surface, the grappler is pulled to that surface.\n\
    * If the target is an item, the item is pulled to the grappler, who may add it to their inventory.\n\
    When a creature is targeted by a grapple, winning an agility contest against the grappler's finesse will let the targeted creature avoid the grapple.\
    Otherwise (or if the grappled creature is willing), they're pinned to the grapple. Creatures can target a grapple, and a hit will dislodge it.\n\
    The grappler gets these options:\
    |▶| Reel in a grappled creature by [Power + 2] distance, if they succeed on a power contest against the grappled creature's power.\n\
    If a creature has been grappled on this round, the first use doesn't cost an action.\n\
    If you are in the air and not flying, you will be pulled towards them instead.\n\
    If both creatures are in the air and not flying, the topmost creature is dragged to the bottommost one.\n\
    An empty hand slot can also be used as a grapple on adjacent creatures.",
    "throwing": "|▶| Throw an object in a straight line. A thrown object will keep traveling until hitting something.\n\
    If a thrown object is about to hit a creature, they can try to avoid it.\
    It's a contest between the target's agility against the thrower's finesse. If the thrower has equal or more successes,\
    the creature is hit and suffers the object's impact effect if it has one. Otherwise, the creature avoids the thrown object, and the object will continue its path.\n\
    If the thrower is unable to sense a creature, then treat their finesse as if it were 0.\n\
    Every 30 spaces a thrown object travels, it receives -1 damage dice (unless volatile), and -1D to hit.\
    If damage dice is taken away while none are left, the object will harmlessly drop in place.\n\
    An item with the volatile keyword is destroyed after being thrown, whether it hits or not.",
    "strike attacks": "|▶| Attack an adjacent target with an unarmed attack or a weapon with a strike effect.\
    Make a finesse check contested with the target's agility check. If the attacker has equal or more successes, the attack hits.\
    An unarmed attack deals damage as specified by your species; a weapon applies its strike effect to the target.",
    # Conditions
    "blinded": "You are unable to see, and will automatically fail any checks that involve sight.",
    "exhausted": "You lose your agility bonus to your speed, and have -1D to all skill checks.\n\
    You may choose to ignore these effects for one round, but must perform a DC 3 endurance check each time you do so:\n\
    * Success: You push through.\n\
    * Partial Success: You lose all breath, and an action.\n\
    * Failure: You fall unconscious for one round.",
    "frozen": "You're pinned by ice (Escape DC 2). Alternatively, any source of heat can melt the ice.",
    "haste": "The number of actions you can take on your turn is increased by 1.\nIn addition, your speed is increased by 3 and jump height increased by 1.",
    "on fire": "You take 1d4 damage per round until you are hit by water or enter a body of water.\
    Alternatively, you can spend an action to attempt to put out the flames with a skill check.",
    "pinned": "You are stuck to a surface by the object or creature pinning you, and your agility is reduced by 2 while pinned.\
    On your turn, make a power contest against the object or creature pinning you. Every contest you fail, you gain +1D to free yourself until you succeed.\
    You may be assisted by allied creatures.",
    "reinforcement": "The next time you would lose karma, instead lose this condition.\
    If it was due to death, a karma flower will sprout near the spot you died. The condition is also lost if you enter starvation.",
    "starvation": "Unless your reserve and required pips are full, these effects apply:\n\
    * You have the exhausted condition.\n\
    * You are noticeably thinner and paler.\n\
    * Your corpse is worth half as many food pips.\n\
    * Instead of the condition being removed on hibernation, you will die of starvation.",
    "sleeping": "You cannot move or perform actions, until you are awoken by one of these methods:\n\
    * You take damage while asleep.\n\
    * You are hit by or fall in water.\n\
    * You hear a loud sound without ear protection.\n\
    * Someone adjacent to you spends an action to wake you up.",
    "stunned": "You lose your turn, instead convulsing on the ground and dropping the items held in your hands.\
    If the source was electrical, then your body will power electrical objects for the stun. After a stun ends, you are immune to being stunned for one round.",
    "terrified": "In this state, you must do one of these things:\n\
    * Flee the situation as fast as possible.\n\
    * Attack the nearest thing you fear. You have -1D to all checks while doing this.\n\
    * Lock up in place, taking no actions or movement.",
    "unconscious": "You cannot move or perform actions, and your breath capacity drops to 0, until you are conscious again."
}

@app.load
@discohook.command.slash(
    name="rule",
    description="Get information about a rule",
    options=[discohook.Option.string(name="rule", required=True, description="Rule name")]
)
async def rule_command(interaction: discohook.Interaction, rule: str):
    match = look_for(rules, rule)
    if match is not None:
        i = rules[match]
        e = discohook.Embed(rule[0].upper() + rule[1:].lower(), description=i)
        await interaction.response.send(embed=e)
    else:
        await interaction.response.send(content="I couldn't find that condition.")

async def index(request: Request):
    return JSONResponse({"success": True}, status_code=200)
app.add_route("/", index, methods=["GET"], include_in_schema=False)
