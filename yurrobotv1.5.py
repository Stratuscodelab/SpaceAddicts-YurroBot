

                                                                                                                     
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
import urllib
import io
import datetime
import psutil
import time

from discord.ext import commands

start_time = datetime.datetime.utcnow()

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)


# Connect to the SQLite database
conn = sqlite3.connect('rtsash8.db')
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
        c.execute("SELECT * FROM spaceaddicts WHERE LOWER(name) = ? UNION SELECT * FROM shop WHERE LOWER(name) = ?", (name, name,))

        #c.execute("SELECT * FROM spaceaddicts WHERE LOWER(name) = ?", (name,))
        result = c.fetchone()

        # If a result is found, send it to the user
        if result:
            # Get the image from the URL
            image_url = result[3]
            with urllib.request.urlopen(image_url) as url:
                image_data = url.read()
            image_file = io.BytesIO(image_data)

            # Create the message with the image
            message_content = '>>Subject: ' + result[0] + '\n'
            message_content += '>>Title: ' + result[1] + '\n'
            message_content += '>>Description:\n' + result[2] + '\n'
            message = await message.channel.send(message_content, file=discord.File(image_file, 'image.jpg'))
      
      
    if message.content.startswith('!lookupron'):
        # Get the name from the command
        name = message.content[11:].lower()

        # Execute a SELECT statement using the entered name
        c.execute("SELECT * FROM ront WHERE LOWER(name) = ?", (name,))
        result = c.fetchone()

        # If a result is found, send it to the user
        if result:
            # Get the image from the URL
            image_url = result[3]
            with urllib.request.urlopen(image_url) as url:
                image_data = url.read()
            image_file = io.BytesIO(image_data)

            # Create the message with the image
            message_content = '>>Subject: ' + result[0] + '\n'
            message_content += '>>Occupation: ' + result[1] + '\n'
            message_content += '>>Profile:\n' + result[2] + '\n'
            message = await message.channel.send(message_content, file=discord.File(image_file, 'image.jpg'))


    if message.content == '!random':
        # Execute a SELECT statement to get the number of rows in the people table
        c.execute("SELECT COUNT(*) FROM spaceaddicts")
        count_result = c.fetchone()
        count = count_result[0]

        # Generate a random number between 1 and the number of rows in the people table
        random_id = random.randint(1, count)

        # Execute a SELECT statement using the generated random number
        c.execute("SELECT * FROM spaceaddicts LIMIT 1 OFFSET ?", (random_id - 1,))
        result = c.fetchone()

        if result:
            # Get the image from the URL
            image_url = result[3]
            with urllib.request.urlopen(image_url) as url:
                image_data = url.read()
            image_file = io.BytesIO(image_data)

            # Create the message with the image
            message_content = '>>Subject: ' + result[0] + '\n'
            message_content += '>>Occupation: ' + result[1] + '\n'
            message_content += '>>Profile:\n' + result[2] + '\n'
            message = await message.channel.send(message_content, file=discord.File(image_file, 'image.jpg'))
            
        
    if message.content == '!randomron':
        # Execute a SELECT statement to get the number of rows in the people table
        c.execute("SELECT COUNT(*) FROM ront")
        count_result = c.fetchone()
        count = count_result[0]

        # Generate a random number between 1 and the number of rows in the people table
        random_id = random.randint(1, count)

        # Execute a SELECT statement using the generated random number
        c.execute("SELECT * FROM ront LIMIT 1 OFFSET ?", (random_id - 1,))
        result = c.fetchone()

        if result:
            # Get the image from the URL
            image_url = result[3]
            with urllib.request.urlopen(image_url) as url:
                image_data = url.read()
            image_file = io.BytesIO(image_data)

            # Create the message with the image
            message_content = '>>Subject: ' + result[0] + '\n'
            message_content += '>>Occupation: ' + result[1] + '\n'
            message_content += '>>Profile:\n' + result[2] + '\n'
            message = await message.channel.send(message_content, file=discord.File(image_file, 'image.jpg'))
            
    
    if message.content.lower().startswith('!yurro help'):
        # Send the help message to the user
        await message.channel.send('**Commands:**\n'
                                '`!lookup [name]`: Look up a Space Addict character by name or Shop Item\n'
                                '`!yurroall`: Will DM you all the characters in Space Addicts\n'
                               '`!random`: Get a random Space Addict character\n'
                               '`!randomron`: Get a random Ron Tacklebox character\n'
                               '`!lookupnft`: Will show a Space Addict NFT image only\n'
                               '`!lookupron`: Will show a Ron Tacklebox collection\n'
                               '`!lookuptraits`: Display all traits for an Space Addict NFT\n'
                               '`!lookupnftfull`: Display all traits and image for a Space Addict NFT\n'
                               '`!yurrostats`: Display server information and channel stats\n'
                               '`!yurro help`: Display this help message\n\n'
                               '**Example Usage:**\n'
                               '`!lookup Viper`\n'
                               '`!lookupnft 123`\n'
                               '`!lookupnftfull 456`')
    
    
    if message.content.startswith('!lookupnft'):
        # Get the edition number from the command
        edition = message.content[11:]

        if edition.isdigit() and int(edition) in range(1, 5556):
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
    
    
    if message.content.startswith('!lookuptraits'):
    # Get the edition number from the command
        edition = message.content[14:]

        if edition.isdigit() and int(edition) in range(1, 5556):
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
            await message.channel.send(f"Invalid input. Please enter a number between 1 and 5555.")
            
            
    if message.content.startswith('!lookupnftfull'):
    # Get the edition number from the command
        edition = message.content[15:]

        if edition.isdigit() and int(edition) in range(1, 5556):
            with open(f"sametar.json", "r") as f:
                data = json.load(f)

            nfts = data
            nft_data = None
            for nft in nfts:
                if nft["edition"] == int(edition):
                    nft_data = nft
                    break

            if nft_data:
                response = f"\n>>Attributes for Edition {edition}<<\n"
                response += "-" * 35 + "\n"
                for attribute in nft_data["attributes"]:
                    response += f"- {attribute['trait_type']}: {attribute['value']}\n"
                response += f"\n"
                response += f"{nft_data['image']}"
                await message.channel.send(response)
            else:
                await message.channel.send(f"No NFT found for edition {edition}.")
        else:
            await message.channel.send(f"Invalid input. Please enter a number between 1 and 5555.")
    
    
    if message.content.startswith('!yurrostats'):
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent
        c.execute("SELECT COUNT(*) FROM spaceaddicts")
        num_records = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM ront")
        num_records2 = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM shop")
        num_records3 = c.fetchone()[0]
        total_users = len(set(client.get_all_members()))
        total_channels = len(list(client.get_all_channels()))
        uptime = datetime.datetime.utcnow() - start_time

        # Get network interface statistics
        net_io_counters = psutil.net_io_counters()
        bytes_sent = net_io_counters.bytes_sent
        bytes_recv = net_io_counters.bytes_recv

        # Calculate network speed
        time.sleep(1)  # Wait for 1 second to get a more accurate measurement
        net_io_counters = psutil.net_io_counters()
        bytes_sent_diff = net_io_counters.bytes_sent - bytes_sent
        bytes_recv_diff = net_io_counters.bytes_recv - bytes_recv
        net_speed = f"Download Speed: {bytes_recv_diff / 1024:.2f} KB/s, Upload Speed: {bytes_sent_diff / 1024:.2f} KB/s"

        # Calculate days, hours, minutes and seconds
        uptime_days = uptime.days
        uptime_hours = uptime.seconds // 3600
        uptime_minutes = (uptime.seconds // 60) % 60
        uptime_seconds = uptime.seconds % 60

        # Format uptime as "Days:Hours:Minutes:Seconds"
        uptime_str = f"{uptime_days} Days, {uptime_hours:02d}:{uptime_minutes:02d}:{uptime_seconds:02d}"
        
        #version number 
        
        version_num = "1.5"

        server_stats = f"**Server Stats**:\nCPU usage: {cpu_usage}%\nMemory usage: {mem_usage}%\nNumber of SA Database Records: {num_records}\nNumber of Ron Tacklebox Database Records: {num_records2}\nNumber of Shop Database Records: {num_records3}\n"
        bot_stats = f"**Bot Stats**:\nTotal users: {total_users}\nTotal channels: {total_channels}\nBot Uptime: {uptime_str}\n{net_speed}\nYurrobot Version: {version_num}"

        await message.channel.send(server_stats + bot_stats)
        
    
    if message.content.startswith('!yurroall'):
        # Execute a SELECT statement to retrieve all names from the database
        c.execute("SELECT name, 'Space Addicts' as source FROM spaceaddicts UNION SELECT name, 'Ron Tacklebox' as source FROM ront UNION SELECT name, 'Shop' as source FROM shop")
        results = c.fetchall()

        # If results are found, create a list of names and send it to the user via DM
        if results:
            formatted_results = {}
            for name, source in results:
                if source not in formatted_results:
                    formatted_results[source] = []
                formatted_results[source].append(name)
            dm_message = ''
            for source, names in formatted_results.items():
                dm_message += f'\n{source.upper()}:\n' + '\n'.join(names) + '\n'
            chunks = [dm_message[i:i+2000] for i in range(0, len(dm_message), 2000)] # split the message into chunks of 2000 characters
            for chunk in chunks:
                await message.author.send(chunk)
        else:
            await message.channel.send('There are no names in the databases.')







# Replace YOUR_BOT_TOKEN with your actual bot token
client.run('token here')

# Close the database connection when the bot is shut down
conn.close()
