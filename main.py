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
    default_help_command=False,
    middleware=[Middleware(SingleUseSessionMiddleware)],
)

def look_for(l: dict, target: str):
    # check for exact matches
    for i in l:
        if i == target:
            return i
    # look for the closest match
    best_match = None
    best_share = 0
    for item in l:
        shared = 0
        # find how many characters it shares
        for i in range(len(item)):
            x = 1
            while i + x <= len(item) and item[i : (i + x)] in target:
                shared = max(shared, x)
                x += 1
        if shared > best_share:
            best_share = shared
            best_match = item
    return best_match

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
    "Can speak with allies wearing a headset who are in the same region.\nAny instruments you play will also play at the headsets of your allies.\nProvides ear protection and immunity to sound-based attacks.")
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
    options=[discohook.Option.string(name="name", required=True, description="Item name")]
)
async def item_command(interaction: discohook.Interaction, name: str):
    match = look_for(items, name)
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
    "adaptations": "Adaptations are modifications to your character, allowing for vastly different abilities and playstyles.\
    You can select them at character creation or complete Passages in order to gain new ones.\n\
    You cannot have multiple copies of the same adaptation, unless they are two different variants of it.",
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
    "hiding": "You can choose to hide from creatures. When a creature may be able to spot you, using an opposed skill check (their perception VS your stealth) If you have more successes, you can remain undetected.\n\
    Attacks made against creatures who can't find you are made with +1D to hit.\n\
    If they have equal or more successes, they spot you. If it's blatantly clear that you're there, you will be spotted without a roll.",
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
    "foraging": "When travelling, it’s often that one will need to take time to search for resources.\n\
    Dependent on the cycle time, your GM may allow you to take a foraging trip in order to find items which you need.\n\
    To perform a foraging trip, each person searching will need to decide for the item category they are searching for, then perform a Perception Check.\n\
    Once done, you can roll on the tables three times. Each time, roll [2d4 + Successes] to determine what you get. Each one can be from a different category.",
    "trading": "When trading items, traders will usually want to receive 2 more value than they are giving up. In some cases, they may feel reluctant to give up certain items at all.",
    "food value": "Check off each condition on the two tables below. Skip the consumption effect table if it’s not going to be consumed. (Whether because of an incompatible diet, or the food being spoiled)\n\n\
    Provides food pips: +Pips\nGrants breath capacity increase: +2 if the region has a lot of water.\nGrants haste: +2\nGrants the luminescent adaptation: +4\nGrants reinforcement: +5\n\n\
    Provides protection against worm grass: +1 if the region has worm grass.\nProvides light within 1 distance of itself: +1\n\
    Provides light within 3+ distance of itself: +2\nHas an impact effect: +3\nCan hatch into a creature, and trader wants to hatch it: +Size of adult creature.",
    "tolls": "Some areas are guarded and require the group to be processed in order to proceed.\n\
    Typically, such guarded checkpoints have several creatures of one species, all armed with the best weapons they have access to. They may attack those who try to cross without paying, unless the people crossing are trusted by the guards.\n\
    Payment required typically must reach a trade value of 10 in order to allow the group to pass.",
    "lowering the price": "A group can try to lower the price of a trader or toll once per cycle.\n\
    To do this, they must decide on a new price. One influence check is then performed. The DC is equal to half of the price reduction, rounded up.\n\
    * Success: The offer is accepted.\n\
    * Partial Success: The trader / toll owner won’t accept, but will compromise in some way if there’s room to do so.\n\
    * Failure: The offer is rejected outright.\n\
    A particularly extreme failure can be seen as an insult to the trader or toll owner.",
    "sounds": "Most things which make noise can be heard from up to 20 distance away, plus your perception. Explosions and other loud sounds can be heard from double the range.\n\
    When trying to hear a sound when it is not in the same room, treat it as if it were 20 distance further away.",
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
    "taming creatures": "Creatures can be tamed by feeding them, then passing an influence check on them. Alternatively, rescuing them from a predator may greatly increase their trust in you.\n\
    Tamed creatures will defend and follow their owner, any may allow the owner to ride them if they trust the owner enough.\n\
    If the owner attacks them, or they're allowed to starve before fully bonding with the owner, their trust may be broken.\
    Herbivores who have their trust broken will generally run away, attacking if they feel trapped. Carnivores and omnivores may turn on their owner and the group.",
    "echoes": "The Echoes are the spiritual remnants of Rain World's previous civilized species, the Ancients. They are forever stuck between this world and transcendence.\
    They were unable to ascend due to their many vices, especially those who were too arrogant or egotistical.\n\
    Upon meeting an echo, they will speak to the group, while causing nearby non-sapient beings to fall limp. Once an echo is finished speaking, the group will awaken in the last shelter they slept in, at the start of the next cycle.\n\
    On a sapient creature's first visit to each echo, their karmic attunement will deepen.\n\
    * Their maximum karma increases by 1, to a maximum of 10.\n\
    * If this would increase their maximum karma to 6, then increase it to 7 instead.\n\
    * If maximum karma could not be increased, instead the creature selects a new rite to gain.\n\
    * Their karma is increased to their new maximum value.\n\
    * Their maximum blessings are increased by 2.",
    # Environment
    "acid": "A creature takes 2d4 damage upon moving into acid, or starting their turn within it. This damage counts as explosive damage.",
    "darkness": "Dark conditions limit the abilities of those who rely on sight. Anyone in a dark location gets -1D on any action which requires sight,\
    such as when trying to hit someone with a thrown object.Anyone who is in total darkness will also receive the blinded condition.",
    "falling": "A creature can fall up to 10 distance without being harmed, +2 per point of stealth they have.\
    Every point of distance beyond that causes them to take 1 damage.\n\
    On landing, a creature will take 1 damage for every point of distance they fell beyond 10.\n\
    If a creature falls far enough to potentially take damage, they lose half of their remaining speed on landing, rounded up.\n\
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
    "blinded": "You are unable to see, and will automatically fail any checks that involve sight, unless you have some alternative means of sensing which will work.",
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
    Once per turn, you may spend one action to make a power contest against the creature pinning you (for a creature) or a power check against the DC of the applying effect (for an object), breaking free on a success.\
    Every contest you fail, you gain +1D to free yourself until you succeed. Other creatures may also make this check once per turn, benefitting from the extra dice pool you've gained, but not adding to it.",
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
    "unconscious": "You cannot move or perform actions, and your breath capacity drops to 0, until you are conscious again.",
    # Iterators
    "superstructure hazards": "Electrical Discharge: Some sections of an iterator's superstructure are shrouded from the rain, but pass electricity through them during work.\
    Any creature in these sections when the rain arrives takes 1d6 damage per round, and any electrical equipment is charged.\n\
    Gravity: Inside most functional superstructures, there is no gravity as a side effect of mass rarefaction cells. In such conditions, these effects apply:\n\
    * Creatures can only change the direction they travel if they’re touching a surface or pole, or throw an object.\n\
    * Creatures will not fall, instead continuing to travel in a straight line until they reach a surface or leave the area with zero gravity.\n\
    Areas with multiple active mass rarefaction cells will have no gravity at all times. Areas with one functional mass rarefaction cell will result in gravity alternating between zero and standard every 3 rounds.",
    "iterator puppets": "When in a puppet room, the iterator may react differently, depending on who entered.\n\
    Assuming the iterator is in a functional state, they may, depending on their temperament:\n\
    * Provide marks of communication, so that the creature can understand the ancients' language. (which iterators speak in)\n\
    * Try to increase maximum karma as much as they can. (Usually to 10)\n\
    * More karmically unbalanced creatures will be harder to boost.\n\
    * Fill the food pips of the creature present.\n\
    * Attempt to modify those in the room, and so providing new adaptations.\n\
    * Attempt to eject or kill those in the room.\n\
    Attempting to throw a singularity bomb will have a functional iterator throw it and everyone else out of the room, causing the creatures to die from the explosion outside the chamber.\
    Against an iterator who is too damaged to fight back in such a manner, a singularity bomb will kill them.",
    # Variants
    "overeating": "You could allow characters to eat past their limit. In that case, apply these changes while above their limit:\n\
    * Speed is dropped by 1 for every excess food pip, to a minimum of 1.\n\
    * Incoming damage from attacks is reduced by 1 for every two excess food pips.\n\
    * Size is increased by 1 for every three excess food pips.",
    "shared pips": "Instead of each player having their own pip amount, all players add their pips together into an overall pool.\
    This allows for much greater use of abilities, but means poor management can result in the whole group starving.",
    # etc
    "adaptations": "Adaptations are modifications to your character, allowing for vastly different abilities and playstyles.\
    You can select them at character creation or complete Passages in order to gain new ones.\
    The number of Adaptations is determined by the column chosen on the table in Skills & Affinities.\n\
    You cannot have multiple copies of the same adaptation, unless they are two different variants of it.\n\
    The following shorthand is used in descriptions of Adaptations:\n\
    * |▶| means it costs one action.\n\
    * |⊚| means it costs one food pip.\n\
    * |⦻| means it costs one Blessing.",
    "burdens": "Optionally, up to four burdens can be taken, which reduce your capabilities in some manner.",
    "rites": "Rites are powerful abilities that relate the karmic energies of the world that use your Blessings.\
    To use certain Rites, you need to have enough Karmic Balance, which is determined by your diet and chosen adaptations.\
    You start with a number of Rites equal to your Karmic Balance (minimum of 0 Rites).\n\
    The following shorthand is used in descriptions of Rites:\n\
    * |▶| means it costs one action.\n\
    * |⊚| means it costs one food pip.\n\
    * |⦻| means it costs one Blessing.\n\
    Something 'you can sense' is anything you can see, hear, or touch.",
    "songs": "Songs are a type of rite, which require an instrument in order to use. Their effects do not stack on a creature.\n\
    |▶▶| Start a new song. It will last until the end of your next turn.\n\
    |▶| Maintain the current song, delaying its ending by one turn. You can only have one maintained at a time.\n\
    Each turn you are playing a song, perform an influence skill check. Creatures who hear it must beat your skill check with an influence or will check of their own, or be affected."
}

@app.load
@discohook.command.slash(
    name="rule",
    description="Get information about a rule",
    options=[discohook.Option.string(name="name", required=True, description="Rule name")]
)
async def rule_command(interaction: discohook.Interaction, name: str):
    match = look_for(rules, name)
    if match is not None:
        i = rules[match]
        e = discohook.Embed(match[0].upper() + match[1:], description=i)
        await interaction.response.send(embed=e)
    else:
        await interaction.response.send(content="I couldn't find that rule.")

features = {}
def register_feature(name: str, kind: str, description: str, fields: dict = {}):
    feature = {"name": name, "kind": kind, "description": description, "fields": fields}
    features[name.lower()] = feature
def register_rite(name: str, description: str, min_balance: int = 0, fields: dict = {}):
    if min_balance > 0:
        fields["Balance Required"] = str(min_balance)
    register_feature(name, "Rite", description, fields)
def register_song(name: str, description: str, fields: dict = {}):
    register_feature(name, "Song", description, fields)

# Adaptations
register_feature(
    "Acidic Bile", "Aggressive Adaptation",
    "|▶, ⊚| Shoot a glob of acid at a target. Treat as a thrown projectile that deals 2d4 + Endurance damage on impact.",
    {"Required Food": "+1"})
register_feature("Aggressive Nature", "Aggressive Adaptation", "Improve your unarmed attack's damage die by one step. (1 → 1d4 → 2d4 → 3d4)", {"Karmic Balance": "-1"})
register_feature("Powerful", "Aggressive Adaptation", "When making an attack, you may choose to reroll your damage dice once. You must take the new damage roll.")
register_feature(
    "Powerful Static", "Aggressive Adaptation",
    "|▶▶, ⊚| Recharge an item. \n\
    |▶, ⊚| Shock a creature. Treat as a thrown projectile with this impact effect: 1d6 damage, and stuns the target.\n\
    |▶▶, ⊚⊚⊚| Attack all creatures within 5 distance of you. On hit, deal 2d6 damage and stun the target.")
register_feature(
    "Proboscis", "Aggressive Adaptation",
    "Select an inventory slot to replace with a Proboscis. If you have Astomatous, it does not replace a slot.\n\
    Improve your unarmed attack's damage die by one step. (1 → 1d4 → 2d4 → 3d4). In addition, your unarmed attacks provide 1 food pip each time you hit a living creature your diet considers edible.\n\
    |▶| Drink one food pip out of a piece of food your diet gives you full pips for. This does not work for anything which is dry.",
    {"Required Food": "+1", "Reserve Food": "-1"})
register_feature(
    "Ricospear", "Aggressive Adaptation",
    "Your projectiles can bounce off up to two surfaces. The path of a previous projectile you used on the same turn is also a valid surface. However, you take -1D to hit if you choose to have it bounce twice.\n\
    Impact effects do not apply for anything projectiles bounce off.")
register_feature(
    "Slowing Spit", "Aggressive Adaptation",
    "|▶| Spit at a creature. Treat as a thrown projectile with this impact effect: Creature's movement speed is reduced by 2 and they suffer -1D on any Agility checks made during their next turn.",
    {"Required Food": "+1"})
register_feature("Spontaneous Combusion", "Aggressive Adaptation", "|⊚| Receive the on fire condition.\nIncoming damage from burning is halved.\nYour unarmed attack sets anything you hit on fire while you are burning.")
register_feature("Blood Drain", "Protective Adaptation", "Every time you hit a size 2+ creature with a melee/unarmed attack, you gain 1 HP. ", {"Required Food": "+1"})
register_feature(
    "Chromatophores", "Protective Adaptation",
    "|▶| Enter camouflage, granting you +2D when making stealth checks. You must spend 1 food pip for every action you make during camouflage. This may be deactivated at any time.",
    {"Required Food": "+1"})
register_feature("Evasive Hop", "Protective Adaptation", "You will always dodge the first incoming attack you failed to dodge in each combat encounter.")
register_feature("Final Stand", "Protective Adaptation", "If you have at least 2 HP when you are damaged, your HP will not drop below 1.")
register_feature("Hearty", "Protective Adaptation", "Gain +3 max HP. Healing in shelters is increased to 3 HP per food pip.")
register_feature("Natural Armour", "Protective Adaptation", "Reduces incoming damage from attacks by 2, to a minimum of 1.")
register_feature(
    "Parry", "Protective Adaptation",
    "When an attack is aimed at you, you can choose to try to parry instead of trying to dodge. To do this, you must be holding an item which is able to parry, from this list:\n\
    * Any type of spear.\n\
    * Any dagger.\n\
    * Any medium or large weapon.\n\
    Make a DC 2 finesse check. The DC increases by 1 for every 4 damage the attack has. A partial success prevents the attack from dealing damage.\
    A full success causes the attack or thrown object to hit the attacker instead. (Unless they're able to dodge or parry it).")
register_feature("Radiative", "Protective Adaptation", "Reduces the tier of heat experienced by 1.")
register_feature("Spiny Tail", "Protective Adaptation", "Creatures who hit you in melee range or grapple you will take 2d4 damage.")
register_feature("Thick Fur", "Protective Adaptation", "While dry, reduce the tier of cold experienced by 1, and any creature adjacent to you who has less warmth pips than you gains 1 warmth pip per round.")
register_feature("Adrenaline Rush", "Movement Adaptation", "|▶| Enter a rush state. While in this state, you have the haste condition. However, lose 1 HP or 1 food pip a round. You may end the effect at any time.")
register_feature("Aquatic", "Movement Adaptation", "Your breath capacity is increased by five rounds, and items thrown by you act normally underwater. Speed is also increased by 2 while in water.")
register_feature(
    "Energy Launch", "Movement Adaptation",
    "|▶, ⊚| Travel up to 10 distance in a straight line. If you crash into something, you stop.\n\
    |▶, ⊚⊚| Travel up to 20 distance in a straight line. If you crash into something, you stop, and it takes 2d4 + Size damage. If the target is a creature, they are able to try and dodge.\n\
    Neither of these can be done in the air.")
register_feature("Grapple", "Movement Adaptation", "Select either a mouth, hand or back slot - they become a range 5 grapple, however it only functions when that slot is empty.", {"Reserve Food": "-2"})
register_feature("High Metabolism", "Movement Adaptation", "You may take an extra action, but you cannot do this two turns in a row. Your speed is increased by 4, and your jump height is increased by 3.", {"Required Food": "+1", "Reserve Food": "-2"})
register_feature("Pole Weaver", "Movement Adaptation", "While on a pole, your speed increases by your agility skill.\nYour jump height is increased by 4 while on a pole.")
register_feature("Sticky Paws", "Movement Adaptation", "You are able to climb on walls or larger creatures.", {"Required Food": "+1"})
register_feature(
    "Volatile Anatomy", "Movement Adaptation",
    "|▶| Create a small explosion that sends you 5 distance in a straight line.\n\
    |▶▶| Create a small explosion that stuns creatures within 3 distance of you.\n\
    If a Volatile Anatomy action is used more than once in a round, you must succeed on a DC 2 endurance check or be stunned for one round.\n\
    Incoming damage from explosions is halved.",
    {"Karmic Balance": "-1"})
register_feature(
    "Wings", "Movement Adaptation",
    "|⊚| You will not fall at the end of your turn for this round.\n\
    |⊚| Until the end of your turn, you can move freely, ignoring jump height.\n\
    Wings do not function while they are wet.",
    {"Required Food": "+1"})
register_feature("Spirit Syphon", "Karmic Balance Adaptation", "When a size 2+ creature is killed, which you have dealt damage to this cycle, you gain 1 Blessing.", {"Required Food": "+1"})
register_feature("The Wheel", "Karmic Balance Adaptation", "You gain +3 Max Blessings that cannot be reduced by negative Karmic Balance. Additionally, choose 1 Rite to gain.")
register_feature(
    "Childbearer", "Ally Adaptation",
    "Create a new character sheet, with two less passages than you (can go into the negatives).\n\
    * Take the first adaptation from each parent. Ignore ally adaptations, and duplicate adaptations.\n\
    * Take the first burden that makes sense, from the first parent.\n\
    * Add a copy of Small Build to the child. If they get old enough, this copy can be removed.\n\
    * Finally, assign their remaining skill points as normal.\n\
    If the child is lost, all checks receive -1D unless the check is related to them.")
register_feature(
    "Lizard Friend", "Ally Adaptation",
    "You now have a tamed lizard of your choice. You may choose their age, although it might be restricted depending on your choice:\n\
    * Blue lizards can be hatchings, young, or adult.\n\
    * Most lizards must be hatchlings or young.\n\
    * Red, caramel, and train lizards must be hatchlings.")
register_feature(
    "Neuron Cluster", "Ally Adaptation",
    "Your comprehension represents neuron flies. Once per cycle, you can spend 1 comprehension to fully block an attack aimed at you, or to add a neuron fly to your inventory.\
    You cannot if it's at  -1, as you'd lose your last neuron fly.\n\
    |▶| Add a held neuron fly to your neuron cluster. Remove the item, and gain 1 comprehension. This cannot bring comprehension above 6.")
register_feature("Operator", "Ally Adaptation", "You have an overseer which you can send commands to by spending an action. If the overseer is destroyed, it cannot be used until a new one shows up at the start of the next cycle.")
register_feature(
    "Anesthetic Barbs", "Support Adaptation",
    "|⊚| Your next unarmed strike, if it hits, will remove an action from the target. They must also pass an endurance check or fall asleep. The DC for the check depends on their size compared to yours:\n\
    * Smaller than you: DC 3.\n\
    * The same size as you: DC 2.\n\
    * Larger than you: DC 1.")
register_feature("Imitator", "Support Adaptation", "|▶| Imitate the sound of a known creature, and/or make your voice seem like it is coming from a different place than it is.")
register_feature("Luminescent", "Support Adaptation", "You provide light within 5 distance of yourself.")
register_feature("Signal Antennae", "Support Adaptation", "|▶| Send a telepathic message to another creature within the same region as you.")
register_feature(
    "Terrifying Presence", "Support Adaptation",
    "The first time a creature senses you in a cycle, you may perform a contest of your Influence against their Will or Comprehension. (Their choice)\n\
    You receive -1D for every 2 size you are smaller than the creature. If the creature wins, they are unaffected.\
    Equal successes means they will not attack you if possible (cornering them can override that). If you win, the creature gains the terrified condition.")
register_feature(
    "Tracker", "Support Adaptation",
    "|▶, ⊚| Mark a creature which you can sense.\
    For 3 rounds, or until another creature is marked, you and your allies roll an extra 1D to hit the creature, and deal extra damage upon a successful hit, equal to your perception + 1.",
    {"Required Food": "+1"})
register_feature("Trophallaxis", "Support Adaptation", "|⊚| Grant an adjacent creature one food pip.", {"Karmic Balance": "+1"})
register_feature(
    "Water Secretions", "Support Adaptation",
    "|▶| Pop a touched bubble fruit.\n\
    |▶| Fire a blast of water at a creature. Treat as a thrown projectile with this impact effect: The target is pushed away by 1d4 distance and is drenched.")
register_feature(
    "Calcified Spears", "Item Adaptatation",
    "|▶▶| A needle grows from your tail, which is added to an empty hand or back slot and functions as a spear. No more than 3 of your needles may exist at a time.\n\
    If you have the Astomatous Adaptation, you are able to eat through this needle. When hitting an edible item, it is consumed. If it is a living creature you can eat, it gives 1 food pip on hit.\n\
    Unlike other spears, calcified spears cannot conduct electricity.")
register_feature(
    "Crafty Nature", "Item Adaptation",
    "|▶▶, ⊚| Roll 2d6 on the table below and spit out an item into a free hand or onto the ground. This only functions when your mouth slot is empty.\n\
    2 - Bomb, 3 - Spore Puff, 4 - Lantern, 5 - Firebush, 6 - Bubble Fruit, 7 - Batnip, 8 - Mushroom, 9 - Bubble Weed, 10 - Vulture Grub, 11 - Beehive, 12 - Pearl\n\
    Gain +1D when crafting.", {"Required Food": "+2"})
register_feature("Combustible Bile", "Item Adaptation", "|▶▶, ⊚| Turn a rock into a bomb or a spear into an explosive spear.", {"Karmic Balance": "-1"})
register_feature("Heirloom", "Item Adaptation", "Select an item that you have when this Adaptation is taken or when hibernating. You have +1D with any checks made using or involving this item. If Item Recall is used on this item, it costs only one Blessing.", {"Karmic Balance": "+1"})
register_feature(
    "Lorekeeper", "Item Adaptation",
    "|▶▶| Change the text or function of an unencrypted pearl.\n\
    |▶▶| Encrypt a pearl so that in order to access the contents the decryption key must be used, or a check with a DC equal to your Comprehension must be passed.\n\
    You gain pearl affinity if you don't have it already.")
register_feature("Sheath Pouch", "Item Adaptation", "Gain an extra inventory slot for the storage of spears. Multiple spears may be stored here, however there can only be one of each type.")
register_feature("Stretchy Cheeks", "Item Adaptation", "|▶| Spit an item stored within a mouth slot out. Treat it as if you threw the item.\nYou can store 2 additional items in your mouth.", {"Required Food": "+1"})
register_feature("Strong Back", "Item Adaptation", "You gain two additional item slots on your back.", {"Required Food": "+1", "Reserve Food": "+1"})
register_feature("Tendril Swarm", "Item Adaptation", "You gain two additional hand item slots.\nYou can walk along any surface and pick up any item that's within 3 distance of you.\nYour jump height is reduced by 4.", {"Required Food": "+1"})
register_feature("Astomatous", "Other Adaptation", "You do not have a mouth, so are unable to eat items or store items within it.", {"Reserve Food": "+2"})
register_feature(
    "Conversion", "Other Adaptation",
    "Select one resource conversion from the list below. You will be able to use this at any time. Conversions can only be done 10 times per cycle.\n\
    * ⊚ → 1 HP\n* ⊚⊚ → ⦻\n* ⦻ → 1 HP\n* ⦻⦻ → Substitute for 1 food pip in an ability.\n* 2 HP → Substitute for 1 food pip in an ability.\n* 3 HP → ⦻",
    {"Karmic Balance": "+1"})
register_feature(
    "Cystic Core", "Other Adaptation",
    "Your unarmed attack now pins creatures to the rot cysts on your body. If you kill a creature using an unarmed attack, you destroy the corpse and gain every food pip its corpse had.\n\
    Incoming damage from explosions is doubled.",
    {"Required Food": "+2"})
register_feature("Fat Stores", "Other Adaptation", "When falling on a creature from at least 5 distance up, you deal damage equal to 1d6 + your size. This is in addition to any fall damage you transfer to them.\nYour speed is reduced by 1.", {"Reserve Food": "+1"})
register_feature("Gigantism", "Other Adaptation", "Your move speed and size are both increased by 1. Your corpse is worth 2 more food pips.", {"Required Food": "+1"})
register_feature("Minimalist", "Other Adaptation", "+1D when trying to ignore the effects of exhaustion.", {"Required Food": "-1"})
register_feature(
    "Sensitive Ears", "Other Adaptation",
    "Unless you are wearing ear protection, these effects apply:\n\
    Your ears can pick up the most minute of sounds and have +1D when making Perception checks using your ears.\n\
    In loud conditions, you have -1D when making any checks and the Perception bonus does not apply.")
register_feature(
    "Small Build", "Other Adaptation",
    "You deal 2 less damage with all physical attacks, to a minimum of 1.\n\
    Your size is decreased by 1. Your corpse is worth 1 less food pip.",
    {"Required Food": "-1", "Reserve Food": "-1"})
register_feature("Survival Instincts", "Other Adaptation", "|⊚⊚| Reroll any failures on your current skill check, once.")
register_feature(
    "Internal Reactor", "Item Adaptation",
    "You have one 'Core' slot, which fits certain items. There, they provide food pips at the start of each cycle, and can be ejected, which is effectively a throw.\n\
    * Electric Spear: +1 pip/cycle if charged.\n\
    * Jellyfish: +1 pip/cycle.\n\
    * Infant Centipede (Dead): +1 pip/cycle\n\
    * Infant Centipede (Alive): +2 pips/cycle. Won't attack.\n\
    * Fire Egg: +d4 - 1 pips/cycle.\n\
    * Singularity Bomb: +3 pips/cycle.\n\
    * MRC: +4 pips/cycle, can be used.",
    {"Required Pips": "+2"})
# Burdens
register_feature(
    "Blinded", "Burden",
    "You always have the blinded condition.\n\
    You are immune to the effects of darkness and bright lights.",
    {"Required Food": "-1"})
register_feature("Declawed", "Burden", "Lose a hand item slot.", {"Required Food": "-1"})
register_feature(
    "Exhausting Throw", "Burden",
    "All of your thrown objects gain an additional damage die. After throwing an object, you gain the exhausted condition until you spend two actions to remove it.\n\
    Neither of these effects apply if you have the exhausted condition.")
register_feature(
    "Frail", "Burden",
    "You are unable to throw spears, except Flaming and Ice Spears. Your maximum HP is reduced by 4, and when hit by a stun, you are stunned for double the duration.",
    {"Karmic Balance": "+2"})
register_feature(
    "Innate Wrath", "Burden",
    "Your maximum karma is lowered to 1, but is always reinforced upon hibernation.\n\
    You have +2D when trying to hit a creature.\n\
    When holding a sapient creature's corpse, their Karma is added to yours.",
    {"Karmic Balance": "-2"})
register_feature(
    "Landlubber", "Burden",
    "Your speed is increased by 2, and your jump height is increased by 1.\n\
    Speed is decreased by 4 while in water. Your breath capacity is reduced by 2 rounds, and you get -1D to all checks while in water.")
register_feature("Light Sensitivity", "Burden", "The usual penalties for dim lighting conditions do not apply.\nAny flashes of light which blind you will also stun you for one round.")
register_feature("Master of None", "Burden", "You may increase one skill by 2 points, or two skills by 1 point.\nYou cannot raise any skill above 2 while creating your character. Passages are unaffected.")
register_feature(
    "Overwhelming Haze", "Burden",
    "You may increase one skill by 1 point.\nRoll 1d4 at the start of each cycle. Up to that many times, the GM may ask for a DC 3 will check.\n\
    * Success: A slight red haze encompasses your vision, dropping your perception by 1 for one round.\n\
    * Partial Success: Red haze creeps in, lowering perception to 0 and dropping your speed to half its usual value, rounded down. This lasts for one round.\n\
    * Failure: The hallucination is overwhelming, and you are stunned for the round.")
register_feature("Pacifist", "Burden", "You are unable to purposely harm creatures.", {"Karmic Balance": "+2"})
# Rites
register_rite(
    "Blast",
    "When hitting a creature with an unarmed attack, you may choose to spend blessings to add damage.\n\
    The first blessing per attack adds 1d4 + Will damage, and each extra one adds an extra 1d4.", 1)
register_rite("Bubble", "|⦻| A chosen creature you can sense is given two additional rounds of air.", 1)
register_rite(
    "Connection",
    "Once per cycle, select a creature you can sense (other than yourself) to link with. Attacking someone you are connected to breaks the connection.\n\
    |▶, ⦻|Restore 1d4 + Will HP to the linked creature.\n\
    If the linked creature dies, you can spend 1 karma to allow them to return at the start of the next cycle.", 2)
register_rite("Delay", "|⦻| Lock a projectile you can sense in time. You may end this effect at any time to allow it to continue its path. Locking a projectile requires a will contest if it isn't yours.", 1)
register_rite("Energy Spear", "|⦻| Materialise a spear made of hard light, to somewhere you can sense. It functions as a normal spear, but it will disappear at the end of the cycle.", 1)
register_rite("Evade", "|⦻| A chosen creature you can sense gains +1D to their next dodge or parry. This bonus cannot stack with itself.")
register_rite("Flash", "|▶, ⦻⦻| Create a bright flash of light somewhere you can sense. Anyone else who can see the flash must succeed a DC 2 perception check or receive the blinded condition for 2 rounds.")
register_rite("Flight", "|⦻⦻⦻| You are flying for this round.", 3)
register_rite(
    "Frost",
    "|▶, ⦻| Cool down an object or creature you can sense by 3 warmth pips.\n\
    |▶, ⦻| Create a snowball in one's hand.\n\
    |▶, ⦻⦻⦻| Freeze everything within 5 distance of a chosen location you can sense.")
register_rite(
    "Gateway",
    "|▶, ⦻⦻| Open a portal between two locations you can sense, treating them as adjacent.\n\
    If you want to keep a portal open past the round you opened it, you must spend an action each turn, or it will close. It will also close after [Will + 3] rounds have passed.\n\
    Creatures who have a gateway opened on them may want to avoid going through. In that case, a contest of their agility versus the gateway user’s will occurs.\
    If the creature trying to evade wins, they move one space instead of going through.")
register_rite("Hasten", "|⦻| You or an adjacent creature receives the haste condition until the end of the round.")
register_rite(
    "Heat",
    "|▶, ⦻| Heat up an object or creature you can sense by up to 3 warmth pips.\n\
    |▶, ⦻| Set an adjacent object/creature on fire.\n\
    |▶, ⦻⦻⦻| Set everything on fire within 5 distance of a chosen location you can sense.")
register_rite(
    "Item Recall",
    "Select an item that you have when this rite is taken or when hibernating.\n\
    |▶, ⦻⦻| The selected item is recalled into an empty slot or onto the ground in front of you.")
register_rite("Karmic Barrier", "|▶, ⦻⦻| Materializes a karmic barrier for you or an adjacent target.\nA karmic barrier reduces the damage of the next incoming attack by Will + 1.", 2)
register_rite("Leech", "When hitting a creature with an unarmed attack, you may choose to spend blessings to drain food pips from it, to add to your own. Every 2 blessings used drains 1 pip.")
register_rite(
    "Nullify",
    "|▶, ⦻⦻⦻| Projects a nullification field at a point you can sense. The field affects anything within 5 distance of its centre, and lasts for up to [Will + 1] rounds or until you dismiss it.\n\
    Any abilities used in there, which cost blessings or food pips, have those costs increased by 2.")
register_rite("Reach", "|▶, ⦻| Perform an unarmed attack on a creature within [Will + 1] distance.")
register_rite("Rejuvenation", "|▶▶, ⦻⦻| Restore 1d4 + Will HP to yourself or an adjacent target.", 3)
register_rite(
    "Rupture",
    "|⦻| Shatters a spear within 10 distance of you that's on the ground or embedded. If it's embedded in a creature, it deals 1d6 damage to them.\n\
    |▶, ⦻|: Attempt a DC 2 will check. A success lets you shatter a spear a creature within 10 distance is carrying.")
register_rite("Sense", "Select an item when you take this rite.\n|▶, ⦻⦻| Determine the direction and rough distance of the nearest one. Blocked by karma gates.")
register_rite(
    "Telekinesis",
    "|▶, ⦻|: Levitate items within 15 distance, up to a limit of your Will. Any items held by someone else require you succeed on a Will check contested by their Power check in order to grab them.\
    Treat them as being in their own, temporary hand slots that last until you throw or drop them, or you move out of levitation range of them.", 2)
register_rite(
    "Void Room",
    "|▶▶, ⦻⦻| Creates a portal to a shelter sized room. The portal lasts as long as is required, and lets anything through it. Only one portal can be open at a time. Any living creatures will be forced out of the room when the portal closes.\n\
    Each creature with the Void Room rite has their own unique room. Closing a void room also closes any void rooms inside of it.")
# Songs
register_song("Deafening Harmony", "Everyone who can hear it gets -1D to any checks involving hearing for its duration. It’s also considered very loud for anyone with sensitive ears.")
register_song(
    "Encouraging Melody",
    "One specific creature, chosen at the start, gets +1D on skill checks during their turn, on each round this is playing.\n\
    Outside of battle, it can be used before a check to try and aid another. It is a DC 3 influence check, with a success meaning the recipient gets +1D on their own check.")
register_song("Relay Melody", "One specific creature, chosen at the start of the song, gets haste for rounds this is playing.")
register_song("Slow Melody", "Hostile creatures are slowed for rounds this is playing.")
register_song("Staggering Melody", "Hostile creatures are staggered for rounds this is playing.")
register_song("Taunting Melody", "Hostile creatures will only target you for rounds this is playing.")

@app.load
@discohook.command.slash(
    name="feature",
    description="Get information about an adaptation, rite, or burden",
    options=[discohook.Option.string(name="name", required=True, description="Feature name")]
)
async def item_command(interaction: discohook.Interaction, name: str):
    match = look_for(features, name)
    if match is not None:
        i = features[match]
        e = discohook.Embed(title=i["name"], description=i["description"])
        e.add_field(name="Type", value=i["kind"], inline=True)
        for x in i["fields"]:
            e.add_field(name=x, value=i["fields"][x], inline=True)
        await interaction.response.send(embed=e)
    else:
        await interaction.response.send(content="I couldn't find that feature.")

@app.load
@discohook.command.slash(
    name = "help",
    description="Get info & help about the bot",
    options=[]
)
async def help_command(interaction: discohook.Interaction):
    await interaction.response.send(content="Neuron is a Monsoon reference bot developed by Rivu (the.rivulet) and it is updated as of Monsoon **1.0.0**.")

async def index(request: Request):
    return JSONResponse({"success": True}, status_code=200)
app.add_route("/", index, methods=["GET"], include_in_schema=False)
