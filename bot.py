import discord
from discord.ext import commands, tasks
import subprocess
from datetime import datetime
import preTools
import funTools
import botTools
from dataBaseManager import *
from dotenv import load_dotenv
import os
import sqlite3


from functools import partial, wraps    
import asyncio
import datetime

load_dotenv()

if False:
    # Remplacez la ligne par 
    # TOKEN_API_DISCORD = "VOTRE_TOKEN_DISCORD"
    NAME_FILE_DATABASE = "data.db"
    TOKEN_API_DISCORD = os.getenv('TOKEN_API_DISCORD')
    TIMING_LOOP_VERIF_ALERT = 13* 60


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

    @tasks.loop()
    async def verif_alert(seconds=TIMING_LOOP_VERIF_ALERT):
        pass #TODO

    base = sqlite3.connect(NAME_FILE_DATABASE)
    createTable(base, 
                Alerts.NAME_BASE.value,
                Alerts.PRIMARY_KEY_SMART_CONTRACT.value[selectData.NAME],
                Alerts.PRIMARY_KEY_SMART_CONTRACT.value[selectData.TYPE],
                {Alerts.PRICE.value[selectData.NAME] : Alerts.PRICE.value[selectData.TYPE]})
    client.run(TOKEN_API_DISCORD)

















#Bot parameters
command_prefix = '/'
description = "you set an alert for "


NAME_FILE_DATABASE = "data.db"
TOKEN_API_DISCORD = os.getenv('TOKEN_API_DISCORD')
TIMING_LOOP_VERIF_ALERT = 13* 60

#Diverse global variable :
CONTRACT_NAME_ETH_BY_CONVENTION = "eth" #it's to make act l'eth like ERC20 in the program, with contract which is its unique id


class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents, sqliteBase):
        super().__init__(command_prefix, description=description, intents=intents)
        self.lock = asyncio.Lock()
        self.timingLoopVerifAlert = TIMING_LOOP_VERIF_ALERT
        self.alerts = {}
        self.index = 0 #to iterate on the wallet addresses
        self.base = sqliteBase
        self.add_commandd("shutdown", MyBot.shutdown)
        self.add_commandd("set", MyBot.set)
        

    def add_commandd(self, name, f):
        self.command(name=name)(wraps(f)(partial(f, self)))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot connected as {self.user.name}')

        #if not exists create table for transactions
        createTable(self.base, 
            Alerts.NAME_BASE.value,
            Alerts.PRIMARY_KEY_SMART_CONTRACT.value[selectData.NAME],
            Alerts.PRIMARY_KEY_SMART_CONTRACT.value[selectData.TYPE],
            {Alerts.PRICE.value[selectData.NAME] : Alerts.PRICE.value[selectData.TYPE]})





        self.alerts = table_to_dict( 
            self.base,
            Alerts.NAME_BASE.value,
            list(Alerts)[1].value[selectData.NAME]
        )


        if not self.notifyAlerts.is_running():
            self.notifyAlerts.start()

    @commands.Cog.listener()
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





    @tasks.loop(seconds=TIMING_LOOP_VERIF_ALERT)
    async def notifyAlerts(self):
        async with self.lock:
            pass #TODO
            




    # @tasks.loop(seconds=TIMING_LOOP_VERIF_ADDRESSES_IN_CHANNEL)
    # async def VerifyNewAddressesOnChannel(self):
    #     async with self.lock:


            
                
            
    async def set(self, ctx):
        message = str(ctx.message.content)
        startAd = message.find("0x")
        contract_address = message[startAd:startAd+ 42]
        price = float(message[message.find("set"):].replace("set","").replace(" ","")) #it converts to float here only for debugging purpose TODO
        newRow(self.base,Alerts.NAME_BASE.value,contract_address,{Alerts.PRICE.value[selectData.NAME] : str(price)})
        self.alerts

    #@commands.command(name='shutdown')
    async def shutdown(self, ctx):
        self.base.close()
        await ctx.send("Bot is shutting down.")
        await self.close()


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    sqliteBase = sqlite3.connect(NAME_FILE_DATABASE)
    bot = MyBot(
        command_prefix=command_prefix, 
        intents=intents,
        sqliteBase=sqliteBase)
    print("VOtre token est " + str(TOKEN_API_DISCORD))
    try:
        bot.run(TOKEN_API_DISCORD)
        
    except Exception as e:
        print('ERROR : BOT SHUTDOWN...')
        sqliteBase.close()


