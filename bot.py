import discord
from discord.ext import commands
import asyncio
import world
import player
import utils
import config
import emoji

bot = commands.Bot(command_prefix='!', description=config.discord_description)
update_rate = 15  # In seconds.
channel = discord.Object(id=config.discord_channel)


# == PLAYER FACING COMMANDS ==
@bot.command(pass_context=True)
async def join(ctx):
    """Registers you as an adventurer!"""

    id = ctx.message.author.id
    player_instance = world.get_player(id)
    message = "<@" + id + ">:"

    if player_instance is None:
        new_player = player.Player()
        new_player.create()
        new_player.id = id

        world.add_player(new_player)

        message += "You will now get adventures. You are a level 1 " + new_player.race + "! Welcome! " + emoji.welcome
    else:
        message += "You are already an adventurer. " + emoji.no

    await bot.say(message)


@bot.command(pass_context=True)
async def pause(ctx):
    """Puts your adventures on hold."""

    id = ctx.message.author.id
    player_instance = world.get_player(id)
    message = "<@" + id + ">:"

    if player_instance is None:
        message += "You do not have a character. Register one with `!join`. " + emoji.no
    else:
        message += "Your adventures have been put on a hold! You rest. Resume adventures with `!resume`. " + emoji.warning
        player_instance.paused = True

    await bot.say(message)


@bot.command(pass_context=True)
async def resume(ctx):
    """Resumes your adventures if you had paused them."""

    id = ctx.message.author.id
    player_instance = world.get_player(id)
    message = "<@" + id + ">: "

    if player_instance is None:
        message += "You do not have a character. Register one with `!join`. " + emoji.no
    else:
        message += "You will receive adventures again! " + emoji.welcome
        player_instance.paused = False

    await bot.say(message)


@bot.command(pass_context=True)
async def inspect(ctx):

    id = ctx.message.author.id
    player_instance = world.get_player(id)

    if player_instance is None:
        message = "<@" + id + ">:\n"
        message += "You do not have a character. Register one with `!join`. " + emoji.no
        await bot.say(message)
        return

    message = player_instance.get_inspect_text()
    await bot.say(message)


# == ADMIN DEBUG COMMANDS ==

@bot.command(pass_context = True)
async def debug_stats(ctx):

    id = ctx.message.author.id
    player_instance = world.get_player(id)
    message = "<@" + id + ">: "

    if player_instance is None:
        message += "You do not have a character. Register one with `!join`. " + emoji.no
    else:
        message += "This is a debug command that will **not** be included in the final version. " + emoji.warning
        message += "Your stats are as follows:\n```yaml\n"

        message += "id: " + player_instance.id + "\n\n"

        message += "strength: " + str(player_instance.strength) + "\n"
        message += "dexterity: " + str(player_instance.dexterity) + "\n"
        message += "intellect: " + str(player_instance.intellect) + "\n"
        message += "charisma: " + str(player_instance.charisma) + "\n"
        message += "luck: " + str(player_instance.luck) + "\n"

        message += "strength_affinity:" + str(player_instance.strength_affinity) + "\n"
        message += "dexterity_affinity:" + str(player_instance.dexterity_affinity) + "\n"
        message += "intellect_affinity:" + str(player_instance.intellect_affinity) + "\n"
        message += "charisma_affinity:" + str(player_instance.charisma_affinity) + "\n"

        message += "gold: " + str(player_instance.gold) + "\n"
        message += "loot: " + str(player_instance.loot) + "\n"
        message += "exp: " + str(player_instance.exp) + "\n\n"

        message += "alignment: " + str(player_instance.alignment) + "\n"
        message += "race: " + str(player_instance.race) + "\n"

        message += "```"

    await bot.say(message)


@bot.command(pass_context = True)
async def debug_join(ctx):
    id = ctx.message.author.id
    player_instance = world.get_player(id)
    message = "<@" + id + ">:"

    if player_instance is None:
        new_player = player.Player()
        new_player.create()

        # Set what you want here:
        new_player.intellect = 4
        new_player.intellect_affinity = 4
        new_player.level = 2

        new_player.id = id

        world.add_player(new_player)

        message += "You will now get adventures. You are a level " + str(new_player.level) + " " + new_player.race + "! Welcome! " + emoji.welcome
    else:
        message += "You are already an adventurer. " + emoji.no

    await bot.say(message)


@bot.command(pass_context = True)
async def debug_visits(ctx):

    id = ctx.message.author.id
    player_instance = world.get_player(id)
    message = "<@" + id + ">: "

    if player_instance is None:
        message += "You do not have a character. Register one with `!join`. " + emoji.no
    else:
        message += "This is a debug command that will **not** be included in the final version. " + emoji.warning
        message += "Your visits are as follows:\n```json\n"
        message += str(player_instance.visits)
        message += "\n```"

    await bot.say(message)


@bot.command(pass_context = True)
async def debug_world_visits(ctx):

    id = ctx.message.author.id
    message = "<@" + id + ">: "

    message += "This is a debug command that will **not** be included in the final version. " + emoji.warning
    message += "All visits are as follows:\n```json\n"
    message += str(world.visits)
    message += "\n```"

    await bot.say(message)


# == ADMIN COMMANDS ==
@bot.command(pass_context = True)
async def admin_force(ctx):
    text = ctx.message.content
    text = text.lower()
    text = text.split(' ', 1)[-1]

    id = ctx.message.author.id

    message = "<@" + id + ">: "

    if id not in config.discord_admins:
        message += "**This is an admin-only command.** " + emoji.no
    else:
        player_instance = world.get_player(id)

        if player_instance is None:
            message += "You have no player character. " + emoji.no
            await bot.say(message)
        elif text not in list(world.adventures.keys()):
            message += "I can't find that adventure! " + emoji.no
            await bot.say(message)
        else:
            message += "Got it. " + emoji.yes
            await bot.say(message)

            player_instance.next = text
            await broadcast(player_instance.embark())


@bot.command(pass_context = True)
async def admin_rebuild(ctx):

    id = ctx.message.author.id

    message = "<@" + id + ">: "

    if id not in config.discord_admins:
        message += "**This is an admin-only command** " + emoji.no
    else:
        try:
            world.rebuild_content()
            message += "Data re-build was a success. " + emoji.yes
        except Exception as e:
            message += "Data re-build hit a snag! Check console for details. " + emoji.no
            utils.log_exception(e)

    await bot.say(message)


@bot.command(pass_context = True)
async def admin_now(ctx):
    id = ctx.message.author.id
    message = "<@" + id + ">: "

    if id not in config.discord_admins:
        message += "**This is an admin-only command** " + emoji.no
    else:
        player_instance = world.get_player(id)

        if player_instance is None:
            message += "You have no player character. " + emoji.no
            await bot.say(message)
        else:
            message += "Got it. " + emoji.yes
            await bot.say(message)

            player_instance.scheduled_adventure = utils.now()

    await bot.say(message)


@bot.command(pass_context = True)
async def admin_purge_saves(ctx):

    id = ctx.message.author.id

    message = "<@" + id + ">: "

    if id not in config.discord_admins:
        message += "**This is an admin-only command** " + emoji.no
    else:
        try:
            world.purge_saves()
            message += "Save purge was a success. " + emoji.yes
        except Exception as e:
            message += "Save purge hit a snag! Check console for details. " + emoji.no
            utils.log_exception(e)

    await bot.say(message)



# == METHODS ==
def is_player_online(id):
    server = bot.get_server(config.discord_server)
    member = server.get_member(id)

    if member is None:
        return False

    if member.status is discord.Status.online or member.status is discord.Status.idle:
        return True

    return False


async def check_players_for_adventure():
    # Embarks any player that needs an adventure.
    if len(world.players) == 0:
        return

    for player_instance in list(world.players.values()):
        if player_instance.paused is False and is_player_online(player_instance.id):
            if player_instance.scheduled_adventure is None or player_instance.scheduled_adventure < utils.now():
                message = player_instance.embark()
                await broadcast(message)


async def broadcast(message):
    try:
        await bot.send_message(channel, message)
    except Exception as e:
        utils.log_exception(e)


async def core_loop():
    await bot.wait_until_ready()
    while not bot.is_closed:
        await check_players_for_adventure()
        world.save_persistent_data()
        await asyncio.sleep(update_rate)


bot.loop.create_task(core_loop())