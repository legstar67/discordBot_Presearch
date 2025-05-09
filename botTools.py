import discord
import subprocess
from datetime import datetime

# Send discord message even if it's longer than 2000 char (limit by discord)
async def sd_msg(channel, content):
    max_length = 2000 - len("``````") #limit of discord
    if len(content) <= max_length:
        await channel.send(f'```{content}```')
    else:
        sizeContent = len(content)
        nbChunks = sizeContent//max_length if sizeContent//max_length == sizeContent/max_length else sizeContent//max_length + 1
        for i in range(nbChunks):
            await channel.send(f'```{content[(i)*max_length:min(sizeContent,(i+1)*max_length)]}```')


# Determine if an element of strTab is in content
def contains(content,strTab):
    for w in strTab:
        if w in content:
            return True
    return False


