

                                                                                                                     
#@@@@@@   @@@@@@@    @@@@@@    @@@@@@@  @@@@@@@@      @@@@@@   @@@@@@@   @@@@@@@   @@@   @@@@@@@  @@@@@@@   @@@@@@   
#@@@@@@@   @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@     @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@@@@@@  @@@@@@@  @@@@@@@   
#!@@       @@!  @@@  @@!  @@@  !@@       @@!          @@!  @@@  @@!  @@@  @@!  @@@  @@!  !@@         @@!    !@@       
#!@!       !@!  @!@  !@!  @!@  !@!       !@!          !@!  @!@  !@!  @!@  !@!  @!@  !@!  !@!         !@!    !@!       
#!!@@!!    @!@@!@!   @!@!@!@!  !@!       @!!!:!       @!@!@!@!  @!@  !@!  @!@  !@!  !!@  !@!         @!!    !!@@!!    
# !!@!!!   !!@!!!    !!!@!!!!  !!!       !!!!!:       !!!@!!!!  !@!  !!!  !@!  !!!  !!!  !!!         !!!     !!@!!!   
#     !:!  !!:       !!:  !!!  :!!       !!:          !!:  !!!  !!:  !!!  !!:  !!!  !!:  :!!         !!:         !:!  
#    !:!   :!:       :!:  !:!  :!:       :!:          :!:  !:!  :!:  !:!  :!:  !:!  :!:  :!:         :!:        !:!   
#:::: ::    ::       ::   :::   ::: :::   :: ::::     ::   :::   :::: ::   :::: ::   ::   ::: :::     ::    :::: ::   
#:: : :     :         :   : :   :: :: :  : :: ::       :   : :  :: :  :   :: :  :   :     :: :: :     :     :: : :    
# =-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- @Arm_710 -=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# =-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-   2023   -=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=  




import discord
import sqlite3
import random
import json

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

# Connect to the SQLite database
conn = sqlite3.connect('sa24.db')
c = conn.cursor()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!lookup'):
        # Get the name from the command
        name = message.content[8:].lower()

        # Execute a SELECT statement using the entered name
        c.execute("SELECT * FROM people WHERE LOWER(name) = ?", (name,))
        result = c.fetchone()

        # If a result is found, send it to the user
        if result:
            await message.channel.send('>>Subject: ' + result[0])
            await message.channel.send('>>Occupation: ' + result[1])
            await message.channel.send('>>Profile:\n' + result[2])
    
    if message.content.startswith('!random'):
        # Execute a SELECT statement to get the number of rows in the people table
        c.execute("SELECT COUNT(*) FROM people")
        count_result = c.fetchone()
        count = count_result[0]

        # Generate a random number between 1 and the number of rows in the people table
        random_id = random.randint(1, count)

        # Execute a SELECT statement using the generated random number
        c.execute("SELECT * FROM people LIMIT 1 OFFSET ?", (random_id - 1,))
        result = c.fetchone()

        # If a result is found, send it to the user
        if result:
            await message.channel.send('>>Subject: ' + result[0])
            await message.channel.send('>>Occupation: ' + result[1])
            await message.channel.send('>>Profile:\n' + result[2])
            
    if message.content.startswith('!yurro help'):
        # Send the help message to the user
        await message.channel.send('**Commands**\n'
                                   '!lookup [name]: Looks up a person by name\n'
                                   '!random: Gets a random person\n'
                                   '!lookupnft: Will display SA NFT with that number\n'
                                   '!lookuptraits: Will display all traits for that NFT number\n'
                                   '!yurro help: Displays the help message\n')
    
    if message.content.startswith('!lookupnft'):
        # Get the edition number from the command
        edition = message.content[11:]

        if edition.isdigit() and int(edition) in range(1, 5555):
            with open(f"sametar.json", "r") as f:
                data = json.load(f)
            
            nfts = data
            ipfs_link = None
            for nft in nfts:
                if nft["edition"] == int(edition):
                    ipfs_link = nft["image"]
                    break
            
            if ipfs_link:
                await message.channel.send(ipfs_link)
            else:
                await message.channel.send(f"No NFT found for edition {edition}.")
        else:
            await message.channel.send(f"Invalid input. Please enter a number between 1 and 5554.")
    
    if message.content.startswith('!lookuptraits'):
    # Get the edition number from the command
        edition = message.content[14:]

        if edition.isdigit() and int(edition) in range(1, 5555):
            with open(f"sametar.json", "r") as f:
                data = json.load(f)
            
            nfts = data
            attributes = []
            for nft in nfts:
                if nft["edition"] == int(edition):
                    attributes += nft["attributes"]
                    break
            
            if attributes:
                response = f"\n>>Attributes for Edition {edition}<<\n"
                response += "-" * 35 + "\n"
                for attribute in attributes:
                    response += f"- {attribute['trait_type']}: {attribute['value']}\n"
                await message.channel.send(response)
            else:
                await message.channel.send(f"No attributes found for edition {edition}.")
        else:
            await message.channel.send(f"Invalid input. Please enter a number between 1 and 5554.")

# Replace YOUR_BOT_TOKEN with your actual bot token
client.run('BOT_TOKEN_HERE')

# Close the database connection when the bot is shut down
conn.close()
