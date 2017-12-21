import bot
import config
import utils

utils.log('Starting up bot!')
bot.bot.run(config.discord_token)