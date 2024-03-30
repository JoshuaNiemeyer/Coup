import random
import settings
import discord 
from discord.ext import commands
from cogs.Player import Player
    
logger = settings.logging.getLogger("bot")



"""
class Slapper(commands.Converter):
    use_nicknames : bool 
    
    def __init__(self, *, use_nicknames) -> None:
        self.use_nicknames = use_nicknames
        
    async def convert(self, ctx, argument):
        someone = random.choice(ctx.guild.members)
        print(ctx.guild.name)
        print(ctx.guild.owner)
        nickname = ctx.author
        if self.use_nicknames:
            nickname = ctx.author.nick
            
        return f"{nickname} slaps {someone} with {argument}"
"""
    
def run():
    intents = discord.Intents.all()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event 
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        await bot.load_extension("cogs.Player")
        
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()