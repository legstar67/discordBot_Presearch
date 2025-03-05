import discord
import subprocess
from datetime import datetime
import preTools
import funTools
import botTools
from dotenv import load_dotenv
import os


load_dotenv()

# Remplacez la ligne par 
# TOKEN_API_DISCORD = "VOTRE_TOKEN_DISCORD"
TOKEN_API_DISCORD = os.getenv('TOKEN_API_DISCORD')


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if False:
        print()
    # if message.author == client.user:
    #     return

    # if message.content.startswith('!cmd '):
    #     command = message.content[5:]
    #     try:
    #         if "docker logs -f" in command:
    #             await handle_docker_logs(message, command)
    #         else:
    #             result = subprocess.check_output(command, shell=True, text=True)
    #             if result.strip():
    #                 await send_long_message(message.channel, result)
    #             else:
    #                 await message.channel.send('Command executed successfully, but no output was returned.')
    #     except subprocess.CalledProcessError as e:
    #         await message.channel.send(f'Error: {e}')
            
    #MONITORING
    elif "!cmd debug node" in message.content:
        await preTools.handle_docker_logs(message, "docker logs -f presearch-node")

    elif message.content == "!cmd temp":
        result = subprocess.check_output("vcgencmd measure_temp", shell=True, text=True)
        await preTools.send_long_message(message.channel, result)


    #END MONITORING
    
    #TOOL
    elif botTools.contains(message.content,["prepa ","prépa ","Prepa ","Prépa "]):
        dateExamBeginning = datetime(2025, 4,22,8,0,0)
        dif = dateExamBeginning - datetime.today()
        await message.channel.send(f"Bonjour ! \nIl te reste exactement avant ton premier concours : \n\n{dif.days} jours  {dif.seconds//3600} heures  {(dif.seconds%3600) //60 } minutes  {dif.seconds%60 } secondes \n\n**Le futur de ta vie est entre tes mains** :)")




    #END TOOL




    ##TROLL : ------
    elif botTools.contains(message.content,["lepen","Lepen","LEPEN","droite","Droite","DROITE"]):
        await message.channel.send('https://tenor.com/view/le-pen-gif-23754327')
    elif botTools.contains(message.content,["melenchon","Melenchon","mélenchon","Mélenchon","gauche","Gauche","GAUCHE"]):
        await message.channel.send('https://tenor.com/view/jean-luc-m%C3%A9lenchon-politique-macron-bfm-bourdin-gif-14227525')

    ##END TROLL : -----

test = on_message


client.run(TOKEN_API_DISCORD)


