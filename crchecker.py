import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
import discord

class MyClient(commands.Bot):
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        with open("crdata.txt", "w"):
            pass

    async def on_ready(self):
        channel = self.get_channel("ID here")  # channel's ID
        await self.timer.start(channel)

    @tasks.loop(seconds=600)
    async def timer(self, channel):
        r = requests.get("https://chess-results.com/Transfer.aspx?key5=TS", data={"key5": "TS"})
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find('table', class_='CRs2')
        tds = table.find_all("td")
        with open("crdata.txt", "r") as file:
            links = file.readlines()
        for i in tds:
            tournament = i.find("a")
            if tournament:
                link = tournament["href"]
                name = tournament.text
                r1 = requests.get("https://chess-results.com/" + link)
                soup1 = BeautifulSoup(r1.text, "html.parser")
                td1 = soup1.find_all("td", "CRr")
                real_td = next((int(j.text) for j in td1 if j.text.isdigit() and 1000 <= int(j.text) <= 3000), 0)
                if real_td >= 2400 and link + "\n" not in links:
                    print(name, link, real_td)
                    await channel.send(f"{name} https://chess-results.com/{link} {real_td}\n")
                    with open("crdata.txt", "a") as file:
                        file.write(f"{link}\n")
                else:
                    print("Waiting for new tournaments")

bot = MyClient(command_prefix='!', intents=discord.Intents().all())
bot.run("") #replace with token
