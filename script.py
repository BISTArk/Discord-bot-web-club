print("ok lets GO!!")

import discord
import os
import requests
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(msg):
    
#avoid infinite loop
    if msg.author == client.user:
        return
#ping
    if msg.content == '-ping':
        await msg.channel.send(f"__***PONG***__\nCurrent Ping = {client.latency}")
        return
    
#synonym
    if msg.content.startswith('-syn'):
        query = msg.content.split(" ")[-1]
        print(query)
        res = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{query}')
        if(res.status_code != 200):
            await msg.channel.send("Sorry pal, we couldn't find synonyms for the word you were looking for.")
            return
        synonyms=[]
        no_syn =0
        meanings = res.json()[0]['meanings']
        for pos in meanings:
            defs = pos['definitions']
            for x in defs:
                synonyms.append(x['synonyms'])
        send_msg = f'The Synonyms of {query} are:- \n'
        for x in synonyms:
            for y in x:
                send_msg += y
                send_msg += ", "
                no_syn +=1
        if no_syn>0:
            send_msg += f"\nIn total there are {no_syn} synonyms found"
            await msg.channel.send(send_msg)
        else:
            await msg.channel.send(f"No synonyms found for this word {query}")
        return

#antonyms
    if msg.content.startswith('-ayn'):
        query = msg.content.split(" ")[-1]
        print(query)
        res = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{query}')
        if(res.status_code != 200):
            await msg.channel.send("Sorry pal, we couldn't find antonyms for the word you were looking for.")
            return
        antonyms=[]
        no_ayn =0
        meanings = res.json()[0]['meanings']
        for pos in meanings:
            defs = pos['definitions']
            for x in defs:
                antonyms.append(x['antonyms'])
        send_msg = f'The antonyms of {query} are:- \n'
        for x in antonyms:
            for y in x:
                send_msg += y
                send_msg += ", "
                no_ayn +=1
        if no_ayn>0:
            send_msg += f"\nIn total there are {no_ayn} antonyms found"
            await msg.channel.send(send_msg)
        else:
            await msg.channel.send(f"No antonyms found for this word {query}")
        return

#definition
    if msg.content.startswith('-def'):
        query = msg.content.split(" ")[-1]
        print(query)
        res = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{query}')
        if(res.status_code != 200):
            await msg.channel.send("Sorry pal, we couldn't find definitions for the word you were looking for.")
            return
        definitions=[]
        send_msg = f'The definitions of __***{query}***__ are:- \n'
        no_def =0
        meanings = res.json()[0]['meanings']
        for pos in meanings:
            send_msg += f'\tWhen **{query}** is used as **{pos["partOfSpeech"]}** it is definied as :- \n'
            defs = pos['definitions']
            for x in defs:
                send_msg += f'\t\t{x["definition"]}\n'
                
        await msg.channel.send(send_msg)
        return

client.run(os.getenv('DISCORD_BOT'))