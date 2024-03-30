import discord
from discord.ext import commands
import random
import json

cardList = ['Assasin', 'Assasin', 'Assasin', 'Contessa', 'Contessa', 'Contessa',  'Duke', 'Duke', 'Duke',  'Captain', 'Captain','Captain', 'Ambassador', 'Ambassador', 'Ambassador']

class Player(commands.Cog):
    def __init__(self, ctx) -> None:
        self.name = ""
        self.coins = 2
        self.cards = []
        self.isAlive = True

    
    @commands.command()
    async def join_game(self, ctx):

        #name of person calling the command
        self.name = ctx.author.nick 
        #randomly assign 3 cards from the deck
        self.cards = random.sample(cardList, 3)

        #remove the first instance of a card
        for card in self.cards:
            cardList.remove(card)

        #open the player.json file
        with open('./data/players.json', 'r+') as f:

      

            # Load existing data
            players = json.load(f)

            #ensure that player hasn't already joined 
            for player in players:
                if player['username'] == self.name:
                     await ctx.send(f"{self.name} has already been added to the game.")
                     return
            
            # Add new objects
            new_player = [
                {"username": self.name, "coins": self.coins, "cards": self.cards}
            ]
            
            # Extend existing data with new objects
            players.extend(new_player)
            
            # Go to the beginning of the file
            f.seek(0)
            
            # Write updated data to file
            json.dump(players, f, indent=4)
            
            # Truncate any remaining data
            f.truncate()

        await ctx.send(f"{self.name} has been added to the Coup game.")

    
     
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