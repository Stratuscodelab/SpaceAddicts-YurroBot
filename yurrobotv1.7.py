

                                                                                                                     
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
import io
import datetime
import psutil
import time
from discord.embeds import Embed
import requests

from PIL import Image
from discord.ext import commands
start_time = datetime.datetime.utcnow()

intents = discord.Intents.all()


client = discord.Client(command_prefix='!', intents=intents)


# Connect to the SQLite database
conn = sqlite3.connect('yourdbhere.db')
c = conn.cursor()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    
    
    
    if message.content.startswith('!lookupron'):
    # Get the name from the command
        name = message.content[11:].lower()

    # Execute a SELECT statement using the entered name
        c.execute("SELECT * FROM ront WHERE LOWER(name) = ?", (name,))
        exact_result = c.fetchone()

    # If an exact result is found, send it to the user
        if exact_result:
            # Get the image from the local file system
            image_path = exact_result[3]
            with open(image_path, 'rb') as f:
                image_file = discord.File(f)

            # Create the embed
            embed = discord.Embed(
                title=exact_result[0],
                description=exact_result[2],
                color=discord.Color.teal()
            )
            with Image.open(image_path) as img:
                img.thumbnail((300, 300))
                with io.BytesIO() as output:
                    img.save(output, format="JPEG")
                    image_data = output.getvalue()
            embed.set_image(url="attachment://thumbnail.png")
            embed.set_thumbnail(url="attachment://logoclear.png")
            embed.add_field(name="Title", value=exact_result[1], inline=False)
            embed.set_footer(text="Learn more here: Spaceaddicts.io")

            # Send the message and the image files to the user
            await message.channel.send(embed=embed, 
                                    files=[discord.File(io.BytesIO(image_data), filename='thumbnail.png'),
                                            discord.File("logoclear.png", filename='logoclear.png')])
        else:
            # Execute a SELECT statement using LIKE to search for similar items
            c.execute("SELECT * FROM ront WHERE LOWER(name) LIKE ?", (f'%{name}%',))
            results = c.fetchall()
            if len(results) > 0:
                message_content = "Did you mean:\n"
                for result in results:
                    message_content += f"- {result[0]}\n"
                message_content += "Here's what I found for you:"
                await message.channel.send(message_content)
                # Send the results to the user
                for result in results:
                    # Get the image from the local file system
                    image_path = result[3]
                    with open(image_path, 'rb') as f:
                        image_file = discord.File(f)

                    # Create the embed
                    embed = discord.Embed(
                        title=result[0],
                        description=result[2],
                        color=discord.Color.teal()
                    )
                    with Image.open(image_path) as img:
                        img.thumbnail((300, 300))
                        with io.BytesIO() as output:
                            img.save(output, format="JPEG")
                            image_data = output.getvalue()
                    embed.set_image(url="attachment://thumbnail.png")
                    embed.set_thumbnail(url="attachment://logoclear.png")
                    embed.add_field(name="Title", value=result[1], inline=False)
                    embed.set_footer(text="Learn more here: Spaceaddicts.io")

                # Send the message and the image files to the user
                await message.channel.send(embed=embed, 
                                    files=[discord.File(io.BytesIO(image_data), filename='thumbnail.png'),
                                            discord.File("logoclear.png", filename='logoclear.png')])
            else:
                await message.channel.send("Item not found.")

    
    
    if message.content.startswith('!shop'):
        # Get the name from the command
        name = message.content[6:].lower()

        # Execute a SELECT statement using the entered name
        c.execute("SELECT * FROM shop WHERE LOWER(name) LIKE ?", ('%' + name + '%',))

        # Fetch the results
        results = c.fetchall()

        # If a result is found, send the image URL to the user
        if results:
            if len(results) == 1:
                # If only one result is found, send its image URL
                image_url = results[0][2]
                message_content = f"Here's the URL for {results[0][0]}: {image_url}"
                await message.channel.send(message_content)
            else:
                # If multiple results are found, suggest them to the user
                message_content = "Multiple items found. Did you mean:\n"
                for result in results:
                    message_content += f"- {result[0]}\n"
                message_content += "Type !shop followed by the item name to get the URL for the desired item."
                await message.channel.send(message_content)
        else:
            # Execute a SELECT statement using LIKE to search for similar items
            c.execute("SELECT * FROM shop WHERE LOWER(name) LIKE ?", (f'%{name}%',))
            results = c.fetchall()
            if len(results) > 0:
                message_content = "Item not found. Did you mean:\n"
                for result in results:
                    message_content += f"- {result[0]}\n"
                message_content += "Type !shop followed by the item name to get the URL for the desired item."
                await message.channel.send(message_content)
            else:
                await message.channel.send("No item found.")

    
    
    if message.content.startswith('!lookup'):
        # Get the name from the command
        name = message.content[8:].lower()

        # Execute a SELECT statement using the entered name
        c.execute("SELECT *, 'spaceaddicts' as tablename FROM spaceaddicts WHERE LOWER(name) = ? ", (name,))
        result = c.fetchone()

        # If a result is found, send it to the user
        if result:
            # Check which table the data came from
            table_name = result[4]

            # Get the image from the local file system
            image_path = result[3]
            with open(image_path, 'rb') as f:
                image_file = discord.File(f)

            # Create the embed
            embed = discord.Embed(
                title=result[0],
                description=result[2],
                color=discord.Color.teal()
            )
            with Image.open(image_path) as img:
                img = img.convert('RGB') # convert the image mode to RGB
                img.thumbnail((300, 300))
                with io.BytesIO() as output:
                    img.save(output, format="JPEG")
                    image_data = output.getvalue()
            embed.set_image(url="attachment://thumbnail.png")
            embed.set_thumbnail(url="attachment://logoclear.png")
            embed.add_field(name="Title", value=result[1], inline=False)
            embed.set_footer(text=f"Learn more here: Spaceaddicts.io")

            # Send the message and the image files to the user
            await message.channel.send(embed=embed, 
                                    files=[discord.File(io.BytesIO(image_data), filename='thumbnail.png'),
                                            discord.File("logoclear.png", filename='logoclear.png')])
        else:
            # Execute a SELECT statement using LIKE to search for similar items
            c.execute("SELECT *, 'spaceaddicts' as tablename FROM spaceaddicts WHERE LOWER(name) LIKE ? ", ('%'+name+'%',))
            results = c.fetchall()

            # If multiple results are found, suggest them to the user
            if results:
                message_content = "Multiple items found..."
                for r in results:
                    message_content += f"\n- {r[0]} ({r[4]})"
                message_content += "\nPlease refine your search."
                await message.channel.send(message_content)
            else:
                pass




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

        # If a result is found, send it to the user
        if result:
            # Get the image from the local file system
            image_path = result[3]
            with open(image_path, 'rb') as f:
                image_file = discord.File(f)

            # Create the embed
            embed = discord.Embed(
                title=result[0],
                description=result[2],
                color=discord.Color.teal()
            )
            with Image.open(image_path) as img:
                img.thumbnail((300, 300))
                with io.BytesIO() as output:
                    img.save(output, format="JPEG")
                    image_data = output.getvalue()
            embed.set_image(url="attachment://thumbnail.png")
            embed.set_thumbnail(url="attachment://logoclear.png")
            embed.add_field(name="Title", value=result[1], inline=False)
            embed.set_footer(text="Learn more here: Spaceaddicts.io")

            # Send the message and the image files to the user
            await message.channel.send(embed=embed, 
                                    files=[discord.File(io.BytesIO(image_data), filename='thumbnail.png'),
                                            discord.File("logoclear.png", filename='logoclear.png')])
            
        
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

        # If a result is found, send it to the user
        if result:
            # Get the image from the local file system
            image_path = result[3]
            with open(image_path, 'rb') as f:
                image_file = discord.File(f)

            # Create the embed
            embed = discord.Embed(
                title=result[0],
                description=result[2],
                color=discord.Color.teal()
            )
            with Image.open(image_path) as img:
                img.thumbnail((300, 300))
                with io.BytesIO() as output:
                    img.save(output, format="JPEG")
                    image_data = output.getvalue()
            embed.set_image(url="attachment://thumbnail.png")
            embed.set_thumbnail(url="attachment://logoclear.png")
            embed.add_field(name="Title", value=result[1], inline=False)
            embed.set_footer(text="Learn more here: Spaceaddicts.io")

            # Send the message and the image files to the user
            await message.channel.send(embed=embed, 
                                    files=[discord.File(io.BytesIO(image_data), filename='thumbnail.png'),
                                            discord.File("logoclear.png", filename='logoclear.png')])
            
    
    if message.content.lower().startswith('!yurro help'):
        embed = discord.Embed(title="Yurrobot Help", description="Here are the available commands:", color=0x00ff00)
        embed.set_thumbnail(url="attachment://logoclear.png")
        embed.add_field(name="!lookup [name]", value="Look up a Space Addict character by name", inline=False)
        embed.add_field(name="!shop [name]", value="Look up an item in the online Space Addicts Shop.", inline=False)
        embed.add_field(name="!random", value="Get a random Space Addict character", inline=False)
        embed.add_field(name="!randomron", value="Get a random Ron Tacklebox character", inline=False)
        embed.add_field(name="!lookupnft [number]", value="Will show all information on that NFT", inline=False)
        embed.add_field(name="!lookupron [name]", value="Will show a Ron Tacklebox collection", inline=False)
        embed.add_field(name="!yurroall", value="Will DM you all the characters in Space Addicts", inline=False)
        embed.add_field(name="!yurrostats", value="Display server information and channel stats", inline=False)
        embed.add_field(name="!links", value="Display all Official links", inline=False)
        embed.add_field(name="!yurro help", value="Display this help message", inline=False)
        embed.add_field(name="Example Usage:", value="`!lookup Viper`\n`!lookupnft 123`\n`!lookupron Finnius`", inline=False)
        await message.channel.send(embed=embed, 
                                    files=[discord.File("logoclear.png", filename='logoclear.png')])

            
            

    if message.content.startswith('!lookupnft'):
        # Get the edition number from the command
        edition = message.content[11:]

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
                embed = Embed(title=f"Attributes for Edition {edition}", description="", color=0x00ff00)
                embed.set_thumbnail(url="attachment://logoclear.png")
                for attribute in nft_data["attributes"]:
                    embed.add_field(name=attribute['trait_type'], value=attribute['value'], inline=False)
                embed.set_image(url=nft_data['image'])
                await message.channel.send(embed=embed, 
                                    files=[discord.File("logoclear.png", filename='logoclear.png')])
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
        version_num = "1.7"

        # Initialize server_stats and bot_stats
        server_stats = ""
        bot_stats = ""

        if True:
            server_stats = f"\nCPU usage: {cpu_usage}%\nMemory usage: {mem_usage}%\nNumber of SA Database Records: {num_records}\nNumber of Ron Tacklebox Database Records: {num_records2}\nNumber of Shop Database Records: {num_records3}\n"
            bot_stats = f"\nTotal users: {total_users}\nTotal channels: {total_channels}\nBot Uptime: {uptime_str}\n{net_speed}\nYurrobot Version: {version_num}"

        # Create embed
        embed = discord.Embed(title="Server and Bot Stats", color=0x00ff00)
        embed.set_thumbnail(url="attachment://logoclear.png")
        embed.add_field(name="Server Stats", value=server_stats, inline=False)
        embed.add_field(name="Bot Stats", value=bot_stats, inline=False)
        await message.channel.send(embed=embed, 
                                    files=[discord.File("logoclear.png", filename='logoclear.png')])


    if message.content.lower().startswith('!links'):
        embed = discord.Embed(title=":pizza: :pizza: Space Addicts Links :pizza: :pizza:", color=0x00ff00)
        embed.set_thumbnail(url="attachment://logoclear.png")
        embed.add_field(name="COMIC BOOK PASS", value="https://app.manifold.xyz/c/GoldenArc", inline=False)
        embed.add_field(name="Official Twitter", value="https://twitter.com/SpaceAddictsNFT", inline=False)
        embed.add_field(name="Asteroid Belt Radio", value="https://twitter.com/Asteroid_Radio", inline=False)
        embed.add_field(name="Asteroid Belt Radio Youtube", value="https://youtube.com/@AsteroidBeltRadio", inline=False)
        embed.add_field(name="Website", value="https://www.spaceaddicts.io/", inline=False)
        embed.add_field(name="OpenSea", value="https://opensea.io/collection/space-addicts", inline=False)
        embed.add_field(name="Ron’s Tacklebox", value="https://opensea.io/collection/ronstacklebox", inline=False)
        embed.add_field(name="Ron’s Tacklebox V2 (PFP’s)", value="https://opensea.io/collection/ron-s-tacklebox-v2", inline=False)
        embed.add_field(name="High Quality Addicts", value="https://ipfs.io/ipfs/QmY3ygkfH16vSxsSRBxMtsVnBagraiCUfddzGU5yb7bdsL/4192.png (simply replace the token ID)", inline=False)
        await message.channel.send(embed=embed, 
                                    files=[discord.File("logoclear.png", filename='logoclear.png')])
        
        
    
    if message.content.startswith('!yurroall'):
        # Execute a SELECT statement to retrieve all names from the database
        c.execute("SELECT name, 'Space Addicts' as source FROM spaceaddicts UNION SELECT name, 'Ron Tacklebox' as source FROM ront UNION SELECT name, 'Shop' as source FROM shop")
        results = c.fetchall()

        # If results are found, create a list of names and send it to the user via DM
        if results:
            # Format the results into a dictionary, where the key is the source and the value is a list of names from that source
            formatted_results = {}
            for name, source in results:
                if source not in formatted_results:
                    formatted_results[source] = []
                formatted_results[source].append(name)
            
            # Create a DM message with the formatted results
            dm_message = ''
            for source, names in formatted_results.items():
                dm_message += f'\n{source.upper()}:\n' + '\n'.join(names) + '\n'

            # Split the message into chunks of 2000 characters and send each chunk via DM
            chunks = [dm_message[i:i+2000] for i in range(0, len(dm_message), 2000)]
            for chunk in chunks:
                embed = discord.Embed(title='Names in Databases', description=chunk, color=0x00ff00)
                await message.author.send(embed=embed)
        else:
            # If no results are found, send a message in the channel indicating that there are no names in the databases
            embed = discord.Embed(title='Names in Databases', description='There are no names in the databases.', color=0xff0000)
            await message.channel.send(embed=embed)


    if message.content.lower().startswith('!about'):
        embed = discord.Embed(title="The World: 🪐", description="The Year: Who cares.... IT'S OUTER SPACE. It's... kinda hard to live.", color=0xffcc00)
        embed.set_thumbnail(url="attachment://logoclear.png")
        embed.add_field(name="The (Space Addicts) :reg: Fight to Survive", value="With sparse resources and an empty stomach, the (Space Addicts) fight to survive. There are no planets left in the solar system. The only safe place is on your battleships, and maybe an asteroid city (if you're lucky).\n\nLet's not forget your empty stomach. PIZZA:ShrimpDelight: is the only thing that keeps us alive! It's really the only blueprint we could find... Then we all decided that Pizza Rocks! Why make anything else...", inline=False)
        embed.add_field(name="5 Pizza Factions Fight for Supremacy", value="5 PIZZA FACTIONS:badbones: :cipher: :kingpizza: :sals: :sokan: fight for pizza supremacy while the rest of the Galaxy lives and works. If you can find a steady job, keep it. If you can find a good crew, bare arms with them. Constant battles rage on in and out of every day and night cycle. It's pretty normal at this point.", inline=False)
        embed.add_field(name="The Only Problem: Low Fuel Cells!", value="Fuel Cells power everything. You have to fight to get your hands on one. If you can produce them, well you're asking for a bruis'n! The whole galaxy is hungry for Pizza, Fuel Cells, and all out War...no big deal right?", inline=False)
        embed.add_field(name="Choose Your Character Wisely", value="Be careful out there. Choose your Character wisely. Pack the right heat. Grab the best slice.:Onionsupreme: :ShrimpDelight: :TropicalThunder: :pizza~1: Join the fight and fight to survive.:sword:", inline=False)
        await message.channel.send(embed=embed, 
                                    files=[discord.File("logoclear.png", filename='logoclear.png')])

       
       
    if message.content.lower().startswith('!space'):
            response = requests.get("https://api.nasa.gov/planetary/apod?api_key=apitokenhere")
            data = response.json()
            embed = discord.Embed(title="NASA's Astronomy Picture of the Day", description=data['title'], color=0x000000)
            embed.set_image(url=data['url'])
            embed.set_footer(text="Image credits: NASA")
            if 'explanation' in data:
                embed.description = data['explanation']
            else:
                embed.description = "No explanation provided."
            await message.channel.send(embed=embed)



    if message.content.startswith('!destroy'):
        # Check if the command was invoked by the bot owner
        if message.author.id == 666666666666666666:  # Replace with your user ID
            for i in range(10):
                with open('cipher.jpg', 'rb') as f:
                    # Create a discord.File object from the image
                    file = discord.File(f)
            
                    # Send the image
                    await message.channel.send(file=file)
                    # Pause for 2 seconds
                    time.sleep(2)
        else:
            await message.channel.send("You don't have permission to use that command!")










# Replace YOUR_BOT_TOKEN with your actual bot token
client.run('your token here ')

# Close the database connection when the bot is shut down
conn.close()
