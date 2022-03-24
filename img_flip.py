import requests
import os
import discord
import bs4

from flask import Flask
from threading import Thread

app=Flask("")

@app.route("/")
def index():
    return "<h1>Bot is running</h1>"

Thread(target=app.run,args=("0.0.0.0",8080)).start()

TOKEN = os.environ['DISCORD_TOKEN']
username = os.environ['username1']
password = os.environ['password1']


def find_meme(name):
    c=[]
    #scrape imgflip.com 
    url = f'https://imgflip.com/search?q={name}'
    response = requests.request('get',url)
    soup = bs4.BeautifulSoup(response.text,'html.parser')
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/meme/'):
            b = a['href'].split('/')
            if b[2].isdigit():
                c.append(b[2])
    print(c[0])
    return c[0]

def caption_meme(id, textarray):
    captionurl = 'https://api.imgflip.com/caption_image'
    params = {
        'username': username,
        'password': password,
        'template_id': id,
    }
    for i in range(len(textarray)):
        params[f"text{i}"] = textarray[i]
    response = requests.request('POST', captionurl, params=params).json()
    print(response)
    return response['data']['url']


def storeids():
    url = 'https://api.imgflip.com/get_memes'
    response = requests.request('get', url).json()
    memedic = {}
    for i in range(100):
        memedic[response["data"]["memes"][i]
                ["name"].lower()] = response["data"]["memes"][i]["id"]
    return memedic


memedicglobal = storeids()

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!imgflip help":
      await message.channel.send("Usage- !imgflip /{template name}/{text-top}/{text-bottom}")
      
    if message.content.startswith('!imgflip'):
        input = message.content.split('/')[1:]
        print(input)
        if input[0] in memedicglobal:
            id = memedicglobal[input[0]]
        else:
            id = find_meme(input[0])
        print(id)
        await message.channel.send(caption_meme(id, input[1:]))


client.run(TOKEN)
