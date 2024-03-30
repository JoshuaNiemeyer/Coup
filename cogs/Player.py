import discord
from discord.ext import commands

class Player(commands.Cog):
    def __init__(self, ctx) -> None:
        self.name = ""
        self.coins = 2
        self.cards = []
        self.isAlive = True
     
    @commands.command()
    async def collect_income(self, ctx):
        self.coins += 1
        await ctx.send(f"{ctx.author.nick} collected income. Total coins: {self.coins}")

    @commands.command()
    async def collect_foreign_aid(self, ctx):
        self.coins += 2
        await ctx.send(f"{self.name} collected income. Total coins: {self.coins}")

    @commands.command()
    async def coup(self, ctx, target : discord.Member):
        if self.coins >= 7:
            self.coins -= 7
            await ctx.send(f"{self.name} initiated a coup against {target}. Total coins: {self.coins}")
        else:
            await ctx.send("You don't have enough coins to initiate a coup.")

async def setup(bot):
    await bot.add_cog(Player(bot))