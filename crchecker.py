import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
import discord

class MyClient(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        file=open("crdata.txt", "w")
        file.close()

    async def on_ready(self):
        channel = bot.get_channel()  # replace with channel ID that you want to send to
        await self.timer.start(channel)

    @tasks.loop(seconds=600)
    async def timer(self, channel):
        r=requests.get("https://chess-results.com/Transfer.aspx?key5=TS", data={"key5":"TS"})
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        table = soup.findAll('table', class_='CRs2')[0]
        
        tds=table.findAll("td")
        
        
        for i in tds:
            tournament=i.find("a")
            if str(tournament)!="None":
                file=open("crdata.txt", "r")
                links=file.readlines()
                file.close()
                link=tournament["href"]
                name=tournament.text
                r1=requests.get("https://chess-results.com/"+link)
                soup1=BeautifulSoup(r1.text, "html.parser")
                td1=soup1.findAll("td", "CRr")
                real_td=0
                for j in td1:
                    text=j.text
                    if text.isdigit():
                        if int(text)>=1000 and 3000>=int(text):
                            real_td=int(text)
                if real_td>=1500: #any rating you need
                    if not (link+"\n" in links):
                        print(name,link,real_td)
                        await channel.send(name+" "+"https://chess-results.com/"+link+" "+str(real_td)+"\n")
                        file=open("crdata.txt", "a")
                        file.write(link+"\n")
                        file.close()
                    else:
                        pass
                        print("Waiting for new tournaments")

bot = MyClient(command_prefix='!', intents=discord.Intents().all())
bot.run("")  # replace with bot token
