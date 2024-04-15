import discord
import asyncio


from discord.ext import commands
import random


import json



cardList = ['Assassin', 'Contessa',  'Duke',  'Captain', 'Ambassador']



class Player(commands.Cog):


    def __init__(self, ctx) -> None:


        self.name = ""


        self.coins = 2


        self.cards = []


        self.isAlive = True
    
    @commands.command()
    async def join_game(self, ctx):



        #name of person calling the command


        self.name = ctx.author.display_name 


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


                {"username": self.name, "coins": self.coins, "cards": self.cards, "isAlive": True}


            ]
            


            # Extend existing data with new objects


            players.extend(new_player)
            


            # Go to the beginning of the file


            f.seek(0)
            


            # Write updated data to file


            json.dump(players, f, indent=4)
            


            # Truncate any remaining data


            f.truncate()



        #dm cards to player


        await ctx.author.send(self.cards)



        await ctx.send(f"{self.name} has been added to the Coup game.")

    @commands.command()
    async def collect_income(self, ctx):


        # Open the JSON file to increment points


        with open('./data/players.json', 'r+') as f:


            # Load existing data


            players = json.load(f)
            


            # Increment points of the first object
         


            found = False


            for player in players:


                if player['username'] == ctx.author.display_name:


                     found = True


                     if(player['isAlive'] == False):


                        await send('Dead player cannot collect income.')


                        return


                     player['coins'] += 1


                     self.coins = player['coins']



            if(found == False):


                await ctx.send(f'{ctx.author.display_name} has not joined the game.')
            


            # Go to the beginning of the file


            f.seek(0)
            


            # Write updated data to file


            json.dump(players, f, indent=4)
            


            # Truncate any remaining data


            f.truncate()



        await ctx.send(f"{ctx.author.display_name} collected income. Total coins: {self.coins}")

    def isValidCard(self, inputCard):
        found = False
        for card in cardList:
            if(inputCard ==  card):
                found = True

        return found
    
    @commands.command()
    async def collect_foreign_aid(self, ctx):


        # Open the JSON file to increment points
    

        with open('./data/players.json', 'r+') as f:
                # Load existing data
                players = json.load(f)
                # Increment points of the first object
                found = False
                for player in players:
                    if player['username'] == ctx.author.display_name:
                        found = True
                        if(player['isAlive'] == False):
                            await ctx.send('Dead player cannot collect income.')
                            return
                        player['coins'] += 2

                        def check(reaction, user):
                            return str(reaction.emoji) == '👍'

                        message =  await ctx.send(f'{ctx.author.display_name} has recieved 2 coins in foreign aid.')
                        try:
                            reaction, user = await commands.wait_for('reaction_add', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            await channel.send('👎')
                        else:
                            await channel.send('👍')

                        await ctx.send(f"{ctx.author.display_name}'s Total Coins: {player['coins']}")
                if(found == False):
                    await ctx.send(f'{ctx.author.display_name} has not joined the game.')
                


                # Go to the beginning of the file


                f.seek(0)
                


                # Write updated data to file


                json.dump(players, f, indent=4)
                


                # Truncate any remaining data


                f.truncate()



        await ctx.send(f"{ctx.author.display_name} collected income. Total coins: {self.coins}")

    @commands.command()
    async def challenge(self, ctx, target: discord.Member, challengeCard):
        if(self.isValidCard(challengeCard) == False):
            await ctx.send(f'{challengeCard} is not a valid card option.')
            return

        with open('./data/players.json', 'r+') as f:


                # Load existing data
                players = json.load(f)
        
                playerFound = False

                for player in players:
                    if player['username'] == target.display_name:
                        playerFound = True

                        cardFound = False
                        for card in player['cards']:
                            if(card == challengeCard):
                                cardFound = True
                        
                        if(cardFound):
                            for challenger in players:
                                if(challenger['username'] == ctx.author.display_name):
                                    randomCard = random.choice(challenger['cards'])
                                    challenger['cards'].remove(randomCard)
                                    await ctx.send(f"{ctx.author.dispay_name}'s suspicion that {target.display_name} doesn't have a {challengeCard} was wrong.")
                                    await ctx.send(f'Therefore, {randomCard} has been removed from {ctx.author.display_name}')
                        else:
                            randomCard = random.choice(player['cards'])
                            player['cards'].remove(randomCard)
                            await ctx.send(f"{ctx.author.dispay_name}'s suspicion that {target.display_name} doesn't have a {challengeCard} was correct.")
                            await ctx.send(f'Therefore, {randomCard} has been removed from {target.display_name}')
                              

                if(playerFound == False):

                    await ctx.send(f'{target.display_name} has not joined the game.')


                f.seek(0)
                


                # Write updated data to file

                json.dump(players, f, indent=4)
                


                # Truncate any remaining data

                f.truncate()

    @commands.command()
    async def coup(self, ctx, target : discord.Member):
        with open('./data/players.json', 'r+') as f:
            players = json.load(f)
            found = False
            for player in players:
                if player['username'] == ctx.author.display_name:
                    found = True
                    if(player['isAlive'] == False):
                        await send('Dead player cannot coup.')
                        return
                    if player['coins'] >= 7:
                        await ctx.send(f"{ctx.author.display_name} initiated a coup against {target.display_name}. Total coins: {self.coins}")
                        player['coins'] -= 7
                        self.coins = player['coins']
                        await ctx.send(f"{ctx.author.display_name} now has {player['coins']} coins.")
                    else:
                        await ctx.send("You don't have enough coins to initiate a coup.")
                if player['username'] == target.display_name:
                    player['cards'].pop(0)
                    await ctx.send(f"{target.display_name} has lost one of their player cards.")
                    await target.send(player['cards'])

            if(found == False):
                await ctx.send(f'{ctx.author.display_name} has not joined the game.')
            
            # Go to the beginning of the file
            f.seek(0)
            
            # Write updated data to file
            json.dump(players, f, indent=4)
            
            # Truncate any remaining data
            f.truncate()
        # if self.coins >= 7:
        #     self.coins -= 7
        #     await ctx.send(f"{self.name} initiated a coup against {target}. Total coins: {self.coins}")
        # else:
        #     await ctx.send("You don't have enough coins to initiate a coup.")







        #Duke
        @commands.command()
        async def collect_tax(self, ctx):
            

            # Open the JSON file to increment points
            with open('./data/players.json', 'r+') as f:


                    # Load existing data


                    players = json.load(f)
                    


                    # Increment points of the first object
                


                    found = False


                    for player in players:


                        if player['username'] == ctx.author.display_name:


                            found = True


                            if(player['isAlive'] == False):


                                await send('Dead player cannot collect income.')


                                return


                            player['coins'] += 3


                            self.coins = player['coins']



                    if(found == False):


                        await ctx.send(f'{ctx.author.display_name} has not joined the game.')
                    


                    # Go to the beginning of the file


                    f.seek(0)
                    


                    # Write updated data to file


                    json.dump(players, f, indent=4)
                    


                    # Truncate any remaining data


                    f.truncate()



            await ctx.send(f"{ctx.author.display_name} collected income. Total coins: {self.coins}")

    @commands.command()
    async def steal(self, ctx, target: discord.Member):

        if ctx.author == target:
            await ctx.send("You can't steal from yourself.")
            return

        with open('./data/players.json', 'r+') as f:

            players = json.load(f)

            stolen_coins = 0

            for player in players:

                if player['username'] == target.display_name:

                    if player['coins'] >= 1:
                        stolen_coins = min(2, player['coins'])
                        player['coins'] -= stolen_coins
                    else:
                        await ctx.send(f"{target.display_name} does not have any coins to steal.")
                        return
                    
                if player['username'] == ctx.author.display_name:
                    player['coins'] += stolen_coins
                    self.coins = player['coins']
            
            f.seek(0)

            json.dump(players, f, indent = 4)

            f.truncate()
        
        await ctx.send(f"{self.name} stole {stolen_coins} coin(s) from {target.display_name}. ")

    @commands.command()
    async def tax(self, ctx):
        with open('./data/players.json', 'r+') as f:
            players = json.load(f)

            for player in players:
                if player['username'] == ctx.author.display_name:
                    player['coins'] += 3
                    self.coins = player['coins']
            
            f.seek(0)

            json.dump(players, f, indent = 4)

            f.truncate()
        
        await ctx.send(f"{ctx.author.display_name} collected tax. Total Coins: {self.coins}.")

    @commands.command()        
    async def assassinate(self, ctx, target : discord.Member):
        with open('./data/players.json', 'r+') as f:
            players = json.load(f)
            found = False
            targetFound = False
            await self.challenge(ctx, target, players)
            for player in players:
                if player['username'] == ctx.author.display_name:
                    found = True
                    if player['isAlive'] == False:
                        await ctx.send('Dead players cannot assassinate.')
                        return
                    if player['coins'] < 3:
                        await ctx.send("You do not have enough coins to assassinate!")
                    else:
                        player['coins'] -= 3
                        self.coins = player['coins']
                        await ctx.send("Assassination has been successful!")

                if player['username'] == target.display_name:
                    targetFound = True
                    if player['isAlive'] == False:
                        await ctx.send(f'{target.display_name} is dead and cannot be assassinated!')
                        return
                    if len(player['cards']) == 2:
                        msg = await ctx.send(f'Choose which of your two player cards to lose.')
                        await msg.add_reaction('1️⃣')
                        await msg.add_reaction('2️⃣')

                        def check(reaction, user):
                            return user == target and str(reaction.emoji) in ['1️⃣', '2️⃣']
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout = 60.0, check = check)
                        except asyncio.TimeoutError:
                            await ctx.send(f'No response from {target.display_name}')
                        else: 
                            if str(reaction.emoji) == '1️⃣':
                                player['cards'].pop(0)
                                await target.send(player['cards'])
                                await ctx.send(f"{target.display_name} has lost one of their player cards.")
                            elif str(reaction.emoji) == '2️⃣':
                                player['cards'].pop(1)
                                await target.send(player['cards'])
                                await ctx.send(f"{target.display_name} has lost one of their player cards.")

            if found == False:
                await ctx.send(f'{ctx.author.display_name} has not joined the game.')
            if targetFound == False:
                await ctx.send(f'{target.display_name} has not joined the game.')
            
            # Go to the beginning of the file
            f.seek(0)
            
            # Write updated data to file
            json.dump(players, f, indent=4)
            
            # Truncate any remaining data
            f.truncate()

    @commands.command()
    async def exchange(self, ctx):
        with open('./data/players.json', 'r+') as f:
            players = json.load(f)

            for player in players:
                if player['username'] == ctx.author.display_name:
                    player['cards']



async def setup(bot):


    await bot.add_cog(Player(bot))