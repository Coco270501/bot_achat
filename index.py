# import requests
import cloudscraper
from bs4 import BeautifulSoup
import discord
import time
from discord.ext import commands, tasks

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    },
)
# Initialise le client Discord
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    permanent_task.start()

async def doingbackmarket(response, lien):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        values_to_find = ["grades-0", "grades-1", "grades-2"]
        elements = soup.find_all(attrs={"data-qa": values_to_find})

        if elements:
            for element in elements:
                prix = element.find(class_=["text-primary-light body-2-light text-center","body-2-light text-center"]).text
                etat = element.find('span').text
                if('État correct' not in etat):
                    await send_discord_bot(prix=prix, etat=etat,lien=lien)

async def doingcertideal(response, lien):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find('div', {'id': 'product-state-switch'})
        categories = elements.find_all('div', {'class': 'product-feature-switch-item'})
        if categories:
            for categorie in categories:
                item = categorie.find('a')
                prix = item.find('p',{'class':'product-switch-price'}).text
                etat = item.find('p', {'class':'product-switch-state'}).text
                print(prix)
                print(etat)
                if('Correct' not in etat):
                    if('Très bon état' not in etat):
                        await send_discord_bot(prix=prix, etat=etat,lien=lien)
                    
@tasks.loop(seconds=3600)
async def permanent_task():
    urlbackmarketargent = "https://www.backmarket.fr/fr-fr/p/iphone-13-pro-max-128-go-argent-debloque-tout-operateur/d1dc3338-2bb0-40ab-b74f-e76788ea02d4#l=11";
    responsebackmarketargent = scraper.get(urlbackmarketargent)
    await doingbackmarket(response=responsebackmarketargent,lien=urlbackmarketargent)
    
    time.sleep(30)

    urlbackmarketbleu = "https://www.backmarket.fr/fr-fr/p/iphone-13-pro-max-128-go-bleu-alpin-debloque-tout-operateur/5becd0a2-df06-4ca8-8d3b-b0bb11697fbf#l=11&scroll=false";
    responsebackmarketbleu = scraper.get(urlbackmarketbleu)
    await doingbackmarket(response=responsebackmarketbleu,lien=urlbackmarketbleu)

    urlcertidealtargent = "https://offre-free.certideal.com/iphone-13-pro-max-reconditionne/iphone-13-pro-max-128-go-argent-8873"
    responsecertidealtargent = scraper.get(urlcertidealtargent)
    await doingcertideal(response=responsecertidealtargent,lien=urlcertidealtargent)
    
@bot.event
async def send_discord_bot(prix,etat,lien):
    channel = bot.get_channel(1169972690698899488)
    embed = discord.Embed(
        title="iphone 13 pro max",
        color=0x00ff00  
    )
    embed.add_field(name="Prix", value=prix, inline=True)
    embed.add_field(name="Etat", value=etat, inline=True)
    embed.add_field(name="Lien", value=lien, inline=False)
    await channel.send(embed=embed)

bot.run("MTE1OTIxMDM1ODQxMDU5NjQ5Mg.GiBDzU.zjx-kjcJPl8okmdeVE5itbcjWkpy7cDGRY0zbE")