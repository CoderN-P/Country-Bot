from mongomethods import *

from fuzzywuzzy import fuzz
import country_converter as coco

from emojiflags.lookup import lookup

import datetime
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
import unicodedata
import asyncio
from dinteractions_Paginator import Paginator


from countryinfo import CountryInfo
import time

from discord import Color
import random
from discord_slash import cog_ext
from main import guild_ids
from typing import Union
import discord

from discord.ext import commands

dic2 = {
    "Mayor": 1,
    "State Senator": 2,
    "Governor": 3,
    "Senator": 4,
    "Vice President": 5,
    "President": 6,
}


dic = {
    1: "Mom's basement",
    2: "Apartment (with roomate)",
    3: "Home Office",
    5: "Mansion",
    10: "Space Base",
}

hunt_animals = {
    "Boar": [":boar:", 1000],
    "Deer": [":deer:", 400],
    "Crocodile": [":crocodile:", 750],
}


quiz_country_list = list(CountryInfo().all().keys())


class EconomyCommands2(
    commands.Cog,
    name="Economy Commands (slash)",
    description="Commands that let you have your own little economy system",
):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Tax your citiens for coins.")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def tax(self, ctx):
        await ctx.defer(hidden=True)
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        if a[0][11] > 1000000000:
            embed = discord.Embed(
                title="Hey!",
                description="You can't tax more. You have emptied the money supply!",
            )
            await ctx.send(embed=embed)
            return

        prestige = a[0][5] + 1

        tax1 = round(((a[0][1] ** 0.5) / 50) * prestige)

        tax1 *= dic2[a[0][3]]

        await ctx.send(
            embed=discord.Embed(
                title="Tax",
                description=f"You got {tax1} :coin: from taxing your population",
            )
        )

        await update_coins((ctx.author.id, tax1 + a[0][11]))

    @tax.error
    async def tax_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                title="Hey!",
                description=f"""You can't collect taxes now! Try again in `{error.retry_after:.2f}`s.""",
            )
            await ctx.send(embed=em)

    @cog_ext.cog_slash(description="Shows global leaderboards for coins and prestige")
    async def leaderboard(self, ctx, type: str = None):
        await ctx.defer(hidden=True)
        if not type:

            data = await find_lb()

            for i in data:
                i["_id"] = await self.bot.fetch_user(int(i["_id"]))

            string = """"""
            for x, i in enumerate(data, start=1):
                prestige = i["data"]["prestige"]
                name = str(i["_id"]).strip("`")
                name2 = str(i["data"]["name"]).strip("`")
                string = (
                    string
                    + f"**{x}.** {name}: `{name2}`| `Prestige Level {prestige}`\n"
                )

            embed = discord.Embed(
                title="Global Leaderboard (prestige)", description=string
            )
            await ctx.send(embed=embed)

        else:

            if type == "coins":
                data = await find_lb2()

                for i in data:
                    i["_id"] = await self.bot.fetch_user(int(i["_id"]))

                string = """"""
                for x, i in enumerate(data, start=1):
                    prestige = i["data"]["coins"]
                    name = str(i["_id"]).strip("`")
                    name2 = str(i["data"]["name"]).strip("`")
                    string = (
                        string + f"**{x}.** {name}: `{name2}`| `{prestige}` :coin:\n"
                    )

                embed = discord.Embed(
                    title="Global Leaderboard (coins)", description=string
                )
                await ctx.send(embed=embed)

            else:
                await ctx.send(":x: uhhhhhh thats not not an option")

    @leaderboard.error
    async def lb_error(self, ctx, error):
        raise error

    @cog_ext.cog_slash(description="Hunt for items (they go to your inventory)")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def hunt(self, ctx):
        await ctx.defer(hidden=True)
        a = await find_inventory(ctx.author.id, ctx)
        if a is None:
            return

        lst = list(hunt_animals.keys())
        lst.append(" ")
        animal = random.choice(lst)

        if animal == " ":
            embed = discord.Embed(
                title="Hunting", description="While hunting you found nothing :C"
            )
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Hunting",
                description=f"While hunting you found an {hunt_animals[animal][0]} {animal} worth {hunt_animals[animal][1]}",
            )
            await ctx.send(embed=embed)

            if f"{hunt_animals[animal][0]} {animal}" not in a.keys():
                a[f"{hunt_animals[animal][0]} {animal}"] = {
                    "amount": 1,
                    "value": hunt_animals[animal][1],
                }

            else:
                a[f"{hunt_animals[animal][0]} {animal}"] = {
                    "amount": a[f"{hunt_animals[animal][0]} {animal}"]["amount"] + 1,
                    "value": a[f"{hunt_animals[animal][0]} {animal}"]["value"]
                    + hunt_animals[animal][1],
                }

            await update_inventory((ctx.author.id, a))

    @hunt.error
    async def hunt_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                title="Hey!",
                description=f"""You can't hunt right now! Try again in `{error.retry_after:.2f}`s.""",
            )
            await ctx.send(embed=em)

    @cog_ext.cog_slash(description="Sell items in your inventory")
    async def sell(self, ctx, item: str, amount: int = None):
        await ctx.defer(hidden=True)
        ab = await reading(ctx.author.id, ctx)
        if ab is None:
            return
        a = await find_inventory(ctx.author.id)

        if not amount:
            item1 = None
            for i in a.keys():
                if item.lower() in i:
                    item1 = i

            if item1 is None:
                await ctx.send(":x: You don't own that!")

            else:
                value = a[item1]["value"]
                if a[item1]["amount"] == 1:
                    del a[item1]
                    await update_inventory((ctx.author.id, a))

                    await ctx.send(
                        embed=discord.Embed(title="Success", description=f"Sold {item}")
                    )

                    await update_coins((ctx.author.id, ab[0][11] + value))

                else:
                    value = a[item1]["value"] / a[item1]["amount"]
                    a[item1] = {
                        "amount": a[item1]["amount"] - 1,
                        "value": a[item1]["value"] - value,
                    }

                    await update_inventory((ctx.author.id, a))

                    await ctx.send(
                        embed=discord.Embed(
                            title="Success", description=f"Sold {item1}"
                        )
                    )

                    await update_coins((ctx.author.id, ab[0][11] + value))

        else:
            if amount <= 0:
                await ctx.send(":x: That is not a valid amount")
                return

            item1 = None
            for i in a.keys():
                if item.lower() in i:
                    item1 = i

            if item1 is None:
                await ctx.send(":x: You don't own that!")
                return

            amount1 = a[item1]["amount"]

            if amount1 < amount:
                await ctx.send(":x: You don't have that much of this item")
                return

            value = a[item1]["value"] / a[item1]["amount"] * amount
            if a[item1]["amount"] - amount == 0:
                del a[item1]
            else:
                a[item1]["amount"] = a[item1]["amount"] - amount

            await update_inventory((ctx.author.id, a))

            await ctx.send(
                embed=discord.Embed(title="Success", description=f"Sold {item1}")
            )

            await update_coins((ctx.author.id, ab[0][11] + value))

    @cog_ext.cog_slash(description="View your inventory")
    async def inventory(self, ctx):
        await ctx.defer(hidden=True)
        a = await find_inventory(ctx.author.id, ctx)
        if a is None:
            return

        string = """"""
        for x, i in enumerate(a.items()):
            amount = i[1]["amount"]
            value = i[1]["value"]
            string = (
                string + f"**{x + 1}.** {i[0]} | Amount: {amount} : Worth: {value}\n"
            )

        if len(a) == 0:
            string = ":x: You don't have anything in your inventory. Buy things from the shop with coins!"

        embed = discord.Embed(title="Inventory", description=string)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Start your country!")
    async def start(self, ctx):
        await ctx.defer(hidden=True)
        try:
            embed = discord.Embed(
                title="Hooray",
                description="""We are very excited for you to start your own country :tada:
      In the chat type the **name** of your soon to be country""",
                color=Color.teal(),
            )

            await ctx.send(embed=embed)
            the_channel, the_author = ctx.channel, ctx.author

            def check(m):
                return m.channel == the_channel and m.author == the_author

            msg = await self.bot.wait_for("message", check=check, timeout=100)

            await writing(
                (
                    ctx.author.id,
                    msg.content,
                    0,
                    1,
                    "Mayor",
                    1,
                    0,
                    50000000,
                    0,
                    0,
                    0,
                    0,
                    0,
                )
            )

            await ctx.send("Hooray, Country Created!!!!")
        except:
            embed = discord.Embed(
                title="Sorry", description=""":x: You already have a country."""
            )

            await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description="Check information about your country, or another person's country."
    )
    async def profile(self, ctx, member: discord.Member = None):
        await ctx.defer(hidden=True)
        if member is None:
            member = ctx.author

        try:
            a = await reading(member.id)
            name = a[0][0]
            username = member.name
            discriminator = member.discriminator

            username = username.replace(" ", "%20")

            amount12 = 36 + len(str(member.id))
            url = f"https://cbotdiscord.npcool.repl.co/{member.id}/{str(member.avatar_url)[amount12:][:-15]}/{str(username)}/{str(discriminator)}"
            embed = discord.Embed(
                title=f"""General Information""",
                description=f"""Name: [`{name}`]({url})
                Population: `{"{:,}".format(a[0][1])}`
                      Multiplier: `{"{:,}".format(a[0][2])}`
                      Job: `{a[0][3]}`
                      Work Ethic: `{a[0][4]}`
                      Work Commands Issued: 
                      `{a[0][10]}`
                      Coins: {a[0][11]} :coin:
                      """,
            )

            embed2 = discord.Embed(
                title="War",
                description=f"""Wars Played: `{a[0][7]}`
                      Wars Won: `{a[0][8]}`
                      Wars Lost: `{a[0][9]}`
                      """,
            )

            embed3 = discord.Embed(
                title="Prestige",
                description=f"""Prestige Level: `{a[0][5]}`
                      Prestige Requirement `{a[0][6]}` population""",
            )

            embed4 = discord.Embed(
                title="Office", description=f"Your office is: `{dic[a[0][4]]}`"
            )

            embed.set_thumbnail(url=member.avatar_url)
            embed2.set_thumbnail(url=member.avatar_url)
            embed3.set_thumbnail(url=member.avatar_url)
            embed4.set_thumbnail(url=member.avatar_url)

            if dic[a[0][4]] == "Mom's basement":
                embed4.set_image(
                    url="http://www.storefrontlife.com/wp-content/uploads/2013/01/Basement.jpg"
                )
            elif dic[a[0][4]] == "Apartment (with roomate)":
                embed4.set_image(
                    url="https://res.cloudinary.com/hemcfvrk2/image/upload/c_lfill,g_xy_center,x_1516,y_615,w_1200,h_700,q_auto:eco,fl_lossy,f_auto/v1485383879/uhzs2wektoh0mb5rkual.jpg"
                )

            elif dic[a[0][4]] == "Mansion":
                embed4.set_image(
                    url="https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2013/08/26/100987825-121017_EJ_stone_mansion_0014r.600x400.jpg?v=1395082652"
                )

            elif dic[a[0][4]] == "Home Office":
                embed4.set_image(
                    url="https://cdn1.epicgames.com/ue/product/Screenshot/01B-1920x1080-6fd10f5c37639159b1d7a57a869aa3ed.png?resize=1&w=1600"
                )

            elif dic[a[0][4]] == "Space Base":
                embed4.set_image(
                    url="https://cdna.artstation.com/p/assets/images/images/000/630/350/large/jarek-kalwa-space-base.jpg?1429173581"
                )

            embed.set_footer(text=f"Tax your citizens with `/tax` to earn coins!")

            pages = [embed, embed2, embed3, embed4]
            await Paginator(bot=self.bot, ctx=ctx, pages=pages, timeout=100)

        except KeyError:
            embed = discord.Embed(
                title="Hey!",
                description=f":x: You or the person you are viewing do not have a country! Create one with `/start`",
            )
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Shows you items you can purchase for your country")
    async def shop(self, ctx):
        await ctx.defer(hidden=True)
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        status = "NOT OWNED"
        status2 = "NOT OWNED"
        status3 = "NOT OWNED"
        status4 = "NOT OWNED"

        if dic[a[0][4]] == "Apartment (with roomate)":
            status = "OWNED"

        if dic[a[0][4]] == "Home Office":
            status = "OWNED"
            status2 = "OWNED"

        if dic[a[0][4]] == "Mansion":
            status = "OWNED"
            status2 = "OWNED"
            status3 = "OWNED"

        if dic[a[0][4]] == "Space Base":
            status = "OWNED"
            status2 = "OWNED"
            status3 = "OWNED"
            status4 = "OWNED"

        embed = discord.Embed(
            title="Store",
            description=f"""**1. Multiplier Boost `1` :zap: ID = 1**
    To buy this item type: `/buy 1 <amount>`
    Cost: 500 :coin:
    Increases your multiplier by 1
    
    **2. Apartment (with roomate) ID = `2` Status: [{status}]**
    To buy this item type: `/buy 2`

    Cost:  1000 :coin:
    
    Your work ethic becomes 2 
    
    
    3. **Home Office :homes:  ID = `3` Status: [{status2}]**
    To buy this item type: `/buy 3`

    Cost: 10,000 :coin:
    
    Your work ethic becomes 3 
    
    
    4. **Mansion :homes:  ID = `4` Status: [{status3}]**
    To buy this item type: `/buy 4`

    Cost: 50,000 :coin:
    
    Your work ethic becomes 5 
    
    5. **Space Base :crescent_moon:  ID = 5 Status: [{status4}]**
    To buy this item type: `/buy 5`

    Cost: 100,000 :coin:
    
    Your work ethic becomes 10 
    
    
    
    """,
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Work and earn population for your country!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def work(self, ctx):
        await ctx.defer(hidden=True)
        chance = random.randint(1, 10)
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        if a[0][1] > 30000000000000000000000000000000000:
            embed = discord.Embed(
                title="Woah!",
                description="You have the max amount of population even possible! You better prestige!",
            )
            await ctx.send(embed=embed)
            return
        if a[0][1] >= 100 and a[0][3] == "Mayor":
            embed = discord.Embed(
                title="Promotion!!!!",
                description="Congratulations!!, You have been promoted to `State Senator`",
            )
            await ctx.send(embed=embed)
            await update(
                (
                    ctx.author.id,
                    a[0][0],
                    a[0][1],
                    a[0][2],
                    "State Senator",
                    a[0][4],
                    a[0][10],
                )
            )
            a = await reading(ctx.author.id)

        elif a[0][1] >= 10000 and a[0][3] == "State Senator":
            embed = discord.Embed(
                title="Promotion!!!!",
                description="Congratulations!!, You have been promoted to `Governor`",
            )
            await ctx.send(embed=embed)
            await update(
                (
                    ctx.author.id,
                    a[0][0],
                    a[0][1],
                    a[0][2],
                    "Governor",
                    a[0][4],
                    a[0][10],
                )
            )
            a = await reading(ctx.author.id)

        elif a[0][1] >= 50000 and a[0][3] == "Governor":
            embed = discord.Embed(
                title="Promotion!!!!",
                description="Congratulations!!, You have been promoted to `Senator`",
            )
            await ctx.send(embed=embed)
            await update(
                (ctx.author.id, a[0][0], a[0][1], a[0][2], "Senator", a[0][4], a[0][10])
            )
            a = await reading(ctx.author.id)

        elif a[0][1] >= 200000 and a[0][3] == "Senator":
            embed = discord.Embed(
                title="Promotion!!!!",
                description="Congratulations!!, You have been promoted to `Vice President`",
            )

            await ctx.send(embed=embed)
            await update(
                (
                    ctx.author.id,
                    a[0][0],
                    a[0][1],
                    a[0][2],
                    "Vice President",
                    a[0][4],
                    a[0][10],
                )
            )
            a = await reading(ctx.author.id)

        elif a[0][1] >= 2500000 and a[0][3] == "Vice President":
            embed = discord.Embed(
                title="Promotion!!!!",
                description=f"Congratulations!!, You have been promoted to `President` You are now the leader of {a[0][0]}",
            )
            await ctx.send(embed=embed)
            await update(
                (
                    ctx.author.id,
                    a[0][0],
                    a[0][1],
                    a[0][2],
                    "President",
                    a[0][4],
                    a[0][10],
                )
            )
            a = await reading(ctx.author.id)

        try:
            if a[0][3] == "Mayor":
                amount1 = random.randint(0, 5)
                amount1 = amount1 * a[0][4]
                if float(a[0][2]).is_integer():
                    embed = discord.Embed(
                        title="Boost Time!!!!! :zap:",
                        description=f"""Your work will be multiplied by `{str(a[0][2])}`""",
                    )
                    await ctx.send(embed=embed)
                    amount1 = amount1 * a[0][2]

                amount = amount1 + int(a[0][1])
                multi = float("{:.1f}".format(a[0][2] + (a[0][5] + 1) / 10))
                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        amount,
                        multi,
                        "Mayor",
                        a[0][4],
                        a[0][10] + 1,
                    )
                )

                embed = discord.Embed(
                    title="Work Work Work!!!!!",
                    description=f"""During your work shift, you got `{amount1}` more people into your country!!""",
                )

                await ctx.send(embed=embed)
                if chance == 5:
                    a = await reading(ctx.author.id)
                    await update(
                        (
                            ctx.author.id,
                            a[0][0],
                            a[0][1],
                            a[0][2] + 1,
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )
                    embed_chance = discord.Embed(
                        title="Hooray",
                        description="While working you found 1 multiplier boost :zap:",
                    )
                    await ctx.send(embed=embed_chance)

            elif a[0][3] == "State Senator":
                amount1 = random.randint(50, 100)
                amount1 = amount1 * a[0][4]
                if float(a[0][2]).is_integer():
                    embed = discord.Embed(
                        title="Boost Time!!!!! :zap:",
                        description=f"""Your work will be multiplied by `{str(a[0][2])}`""",
                    )
                    await ctx.send(embed=embed)
                    amount1 = amount1 * a[0][2]

                amount = amount1 + int(a[0][1])
                multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1) / 10)))
                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        amount,
                        multi,
                        "State Senator",
                        a[0][4],
                        a[0][10] + 1,
                    )
                )

                embed = discord.Embed(
                    title="Work Work Work!!!!!",
                    description=f"""During your work shift, you got `{amount1}` more people into your country!!""",
                )

                await ctx.send(embed=embed)
                if chance == 5:
                    a = await reading(ctx.author.id)
                    await update(
                        (
                            ctx.author.id,
                            a[0][0],
                            a[0][1],
                            a[0][2] + 1,
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )
                    embed_chance = discord.Embed(
                        title="Hooray",
                        description="While working you found 1 multiplier boost :zap:",
                    )
                    await ctx.send(embed=embed_chance)

            elif a[0][3] == "Governor":
                amount1 = random.randint(100, 500)
                amount1 = amount1 * a[0][4]
                if float(a[0][2]).is_integer():
                    embed = discord.Embed(
                        title="Boost Time!!!!! :zap:",
                        description=f"""Your work will be multiplied by `{str(a[0][2])}`""",
                    )
                    await ctx.send(embed=embed)
                    amount1 = amount1 * a[0][2]

                amount = amount1 + int(a[0][1])
                multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1) / 10)))
                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        amount,
                        multi,
                        "Governor",
                        a[0][4],
                        a[0][10] + 1,
                    )
                )

                embed = discord.Embed(
                    title="Work Work Work!!!!!",
                    description=f"""During your work shift, you got `{amount1}` more people into your country!!""",
                )

                await ctx.send(embed=embed)
                if chance == 5:
                    a = await reading(ctx.author.id)
                    await update(
                        (
                            ctx.author.id,
                            a[0][0],
                            a[0][1],
                            a[0][2] + 1,
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )
                    embed_chance = discord.Embed(
                        title="Hooray",
                        description="While working you found 1 multiplier boost :zap:",
                    )
                    await ctx.send(embed=embed_chance)

            elif a[0][3] == "Senator":
                amount1 = random.randint(1000, 5000)
                amount1 = amount1 * a[0][4]

                if float(a[0][2]).is_integer():
                    embed = discord.Embed(
                        title="Boost Time :zap:!!!!!",
                        description=f"""Your work will be multiplied by `{str(a[0][2])}`""",
                    )
                    await ctx.send(embed=embed)
                    amount1 = amount1 * a[0][2]
                amount = amount1 + int(a[0][1])
                multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1) / 10)))
                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        amount,
                        multi,
                        "Senator",
                        a[0][4],
                        a[0][10] + 1,
                    )
                )

                embed = discord.Embed(
                    title="Work Work Work :zap:!!!!!",
                    description=f"""During your work shift, you got `{amount1}` more people into your country!!""",
                )

                await ctx.send(embed=embed)
                if chance == 5:
                    a = await reading(ctx.author.id)
                    await update(
                        (
                            ctx.author.id,
                            a[0][0],
                            a[0][1],
                            a[0][2] + 1,
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )
                    embed_chance = discord.Embed(
                        title="Hooray",
                        description="While working you found 1 multiplier boost :zap:",
                    )
                    await ctx.send(embed=embed_chance)

            elif a[0][3] == "Vice President":
                amount1 = random.randint(10000, 50000)
                amount1 = amount1 * a[0][4]
                if float(a[0][2]).is_integer():
                    embed = discord.Embed(
                        title="Boost Time :zap:!!!!!",
                        description=f"""Your work will be multiplied by `{str(a[0][2])}`""",
                    )
                    await ctx.send(embed=embed)
                    amount1 = amount1 * a[0][2]

                amount = amount1 + int(a[0][1])
                multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1) / 10)))
                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        amount,
                        multi,
                        "Vice President",
                        a[0][4],
                        a[0][10] + 1,
                    )
                )

                embed = discord.Embed(
                    title="Work Work Work!!!!!",
                    description=f"""During your work shift, you got `{amount1}` more people into your country!!""",
                )

                await ctx.send(embed=embed)
                if chance == 5:
                    a = await reading(ctx.author.id)
                    await update(
                        (
                            ctx.author.id,
                            a[0][0],
                            a[0][1],
                            a[0][2] + 1,
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )
                    embed_chance = discord.Embed(
                        title="Hooray",
                        description="While working you found 1 multiplier boost :zap:",
                    )
                    await ctx.send(embed=embed_chance)

            elif a[0][3] == "President":
                amount1 = random.randint(50000, 100000)
                amount1 = amount1 * a[0][4]
                if float(a[0][2]).is_integer():
                    embed = discord.Embed(
                        title="Boost Time!!!!! :zap:",
                        description=f"""Your work will be multiplied by `{str(a[0][2])}`""",
                    )
                    await ctx.send(embed=embed)
                    amount1 = amount1 * a[0][2]
                amount = amount1 + int(a[0][1])
                multi = float("{:.1f}".format(a[0][2] + ((a[0][5] + 1) / 10)))
                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        amount,
                        multi,
                        "President",
                        a[0][4],
                        a[0][10] + 1,
                    )
                )

                embed = discord.Embed(
                    title="Work Work Work!!!!!",
                    description=f"""During your work shift, you got `{amount1}` more people into your country!!""",
                )

                await ctx.send(embed=embed)
                if chance == 5:
                    a = await reading(ctx.author.id)
                    await update(
                        (
                            ctx.author.id,
                            a[0][0],
                            a[0][1],
                            a[0][2] + 1,
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )
                    embed_chance = discord.Embed(
                        title="Hooray",
                        description="While working you found 1 multiplier boost :zap:",
                    )
                    await ctx.send(embed=embed_chance)

        except OverflowError:
            await ctx.send(
                " :x: You have WAY too much population. You better prestige or you won't be able to work!"
            )

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                title="Too tired",
                description=f"""You are too tired to work again. You can work in `{error.retry_after:.2f}`s.""",
            )
            await ctx.send(embed=em)

        else:
            raise error

    @cog_ext.cog_slash(
        description="Your population and multiplier will be reset, but you earn more coins, multiplier and population."
    )
    async def prestige(self, ctx):
        await ctx.defer(hidden=True)
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        if a[0][1] > a[0][6]:
            embed = discord.Embed(
                title="Hooray!!",
                description="You have met the requirements to prestige!! Do you want to prestige `y` | `n`",
            )
            await ctx.send(embed=embed)

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=100)

                if msg.content.lower() == "n":
                    embed = discord.Embed(
                        title="ok", description=":x: Prestige cancelled"
                    )
                    await ctx.send(embed=embed)

                elif msg.content.lower() == "y":
                    await update_prestige(
                        (
                            ctx.author.id,
                            a[0][0],
                            0,
                            1,
                            "Mayor",
                            1,
                            a[0][5] + 1,
                            (a[0][6] + 50000000),
                        )
                    )
                    embed = discord.Embed(
                        title="Congratulations", description=":tada: You prestiged!!"
                    )
                    await ctx.send(embed=embed)

                else:
                    await ctx.send("That isnt a valid option!")
            except asyncio.TimeoutError:
                await ctx.send("Time ran out :C")

        else:
            embed = discord.Embed(
                title="Oh No",
                description=""":x: you haven't met the requirements to prestige. You can see the requirements on your profile! (under the prestige section)""",
            )
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Deletes your country :((")
    async def quit(self, ctx):
        await ctx.defer(hidden=True)
        embed = discord.Embed(
            title="quit",
            description=":x: Are you really sure you want to quit your country. You will lose all your data (`y`,`n`)",
        )
        await ctx.send(embed=embed)
        thechannel = ctx.channel
        theauthor = ctx.author

        def check(m):
            return (
                m.content == "y"
                or m.content == "n"
                and m.channel == thechannel
                and m.author == theauthor
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=100)
        except asyncio.TimeoutError:
            await ctx.send(":x: You did not answer in time")
            return
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return
        if msg.content == "y":
            await delete_task(ctx.author.id)
            prefix = ctx.prefix
            embed = discord.Embed(
                title="Country deleted",
                description=f"Your country is gone, and you can't become the leader :cry:. But don't worry :D. You can start a new one with `{prefix}start`",
            )
            await ctx.send(embed=embed)
        elif msg.content == "n":
            embed = discord.Embed(
                title="Phew", description=f"Your country is not deleted :DD"
            )
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description="Buy items for your country! Check out the items for sale with the shop command!"
    )
    async def buy(self, ctx, id: int, amount: int = None):
        await ctx.defer(hidden=True)
        id = str(id)
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        if amount:

            if id == "1":
                if a[0][11] - (500 * int(amount)) < 0:
                    embed = discord.Embed(
                        title="Oh no",
                        description=""":x: You don't have enough coins!""",
                    )
                    await ctx.send(embed=embed)
                    return

                if a[0][2] > 10000000:
                    embed = discord.Embed(
                        title="Stop!", description="You can't buy anymore multiplier!!"
                    )
                    await ctx.send(embed=embed)
                    return

                if int(amount) <= 0:
                    await ctx.send(":x: You can't buy this amount of multiplier smh")
                    return
                if (int(amount)) + a[0][2] > 10000000:
                    embed = discord.Embed(
                        title="Stop!", description="You can't buy anymore multiplier!!"
                    )
                    await ctx.send(embed=embed)
                    return

                await update(
                    (
                        ctx.message.author.id,
                        a[0][0],
                        a[0][1],
                        a[0][2] + (1 * int(amount)),
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    )
                )

                await update_coins((ctx.author.id, a[0][11] - (500 * int(amount))))

                embed = discord.Embed(
                    title="Congratulations",
                    description=f"You have bought {amount} Multiplier Boosts",
                )
                await ctx.send(embed=embed)

        else:

            if id == "1":
                embed = discord.Embed(
                    title="Error", description=":x: How much multiplier are you buying!"
                )
                await ctx.send(embed=embed)

            elif id == "2":
                if a[0][4] >= 2:
                    embed = discord.Embed(
                        title="Hey", description=":x: You already own this!!!"
                    )
                    await ctx.send(embed=embed)
                    return
                if (a[0][11] - 1000) < 0:
                    embed = discord.Embed(
                        title="Oh no",
                        description=""":x: You don't have enough coins!""",
                    )
                    await ctx.send(embed=embed)
                    return

                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1],
                        a[0][2],
                        a[0][3],
                        (a[0][4] + 1),
                        a[0][10],
                    )
                )

                await update_coins((ctx.author.id, a[0][11] - 1000))

                embed = discord.Embed(
                    title="Congratulations",
                    description=f"You have bought the Apartment (with roomate)",
                )
                await ctx.send(embed=embed)

            elif id == "3":
                if a[0][4] >= 3:
                    embed = discord.Embed(
                        title="Hey", description=":x: You already own this!!!"
                    )
                    await ctx.send(embed=embed)
                    return
                if a[0][4] < 2:
                    embed = discord.Embed(
                        title="Hey",
                        description=":x: You need to buy the apartment first!!!",
                    )
                    await ctx.send(embed=embed)
                    return
                if (a[0][11] - 10000) < 0:
                    embed = discord.Embed(
                        title="Oh no",
                        description=""":x: You don't have enough coins!""",
                    )
                    await ctx.send(embed=embed)
                    return

                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1],
                        a[0][2],
                        a[0][3],
                        (a[0][4] + 1),
                        a[0][10],
                    )
                )

                await update_coins((ctx.author.id, a[0][11] - 10000))

                embed = discord.Embed(
                    title="Congratulations",
                    description=f"You have bought the Home Office",
                )
                await ctx.send(embed=embed)

            elif id == "4":
                if a[0][4] >= 5:
                    embed = discord.Embed(
                        title="Hey", description=":x: You already own this!!!"
                    )
                    await ctx.send(embed=embed)
                    return
                if a[0][4] < 3:
                    embed = discord.Embed(
                        title="Hey",
                        description=":x: You need to buy the Home Office first!!!",
                    )
                    await ctx.send(embed=embed)
                    return
                if (a[0][11] - 50000) < 0:
                    embed = discord.Embed(
                        title="Oh no",
                        description=""":x: You don't have enough coins!""",
                    )
                    await ctx.send(embed=embed)
                    return

                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1],
                        a[0][2],
                        a[0][3],
                        (a[0][4] + 2),
                        a[0][10],
                    )
                )

                await update_coins((ctx.author.id, a[0][11] - 50000))

                embed = discord.Embed(
                    title="Congratulations", description=f"You have bought the Mansion"
                )
                await ctx.send(embed=embed)

            elif id == "5":
                if a[0][4] >= 10:
                    embed = discord.Embed(
                        title="Hey", description=":x: You already own this!!!"
                    )
                    await ctx.send(embed=embed)
                    return
                if a[0][4] < 5:
                    embed = discord.Embed(
                        title="Hey",
                        description=":x: You need to buy the Mansion first!!!",
                    )
                    await ctx.send(embed=embed)
                    return
                if (a[0][11] - 100000) < 0:
                    embed = discord.Embed(
                        title="Oh no",
                        description=""":x: You don't have enough coins!""",
                    )
                    await ctx.send(embed=embed)
                    return

                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1],
                        a[0][2],
                        a[0][3],
                        (a[0][4] + 5),
                        a[0][10],
                    )
                )

                await update_coins((ctx.author.id, a[0][11] - 100000))

                embed = discord.Embed(
                    title="Congratulations",
                    description=f"You have bought the Space Base",
                )
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="ummmm",
                    description="This ID doesn't exist. Check out the shop command to see all the available IDs",
                )
                await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description='Gift some population to other people! Specify "half" or "full" or an integer as the amount!'
    )
    async def gift(self, ctx, user: discord.User, amount: str):
        await ctx.defer(hidden=True)
        try:
            a = await reading(user.id)

        except:
            embed = discord.Embed(
                title="Whoops", description=":x: This person doesnt have a country!!"
            )
            await ctx.send(embed=embed)
            return

        if str(user.id) == str(ctx.author.id):
            embed = discord.Embed(
                title="Hey!", description=":x: You can't give gifts to yourself!"
            )
            await ctx.send(embed=embed)
            return

        b = await reading(ctx.author.id, ctx)
        if b is None:
            return

        try:
            amount = amount.strip(",")
            if amount.isnumeric():
                if int(amount) > b[0][1]:
                    embed = discord.Embed(
                        title="Hey!", description=":x: You don't have that many people!"
                    )
                    await ctx.send(embed=embed)

                else:
                    await update(
                        (
                            ctx.author.id,
                            b[0][0],
                            b[0][1] - int(amount),
                            b[0][2],
                            b[0][3],
                            b[0][4],
                            b[0][10],
                        )
                    )

                    await update(
                        (
                            user,
                            a[0][0],
                            a[0][1] + int(amount),
                            a[0][2],
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )

                    await ctx.send(
                        embed=discord.Embed(
                            title="Success!",
                            description=f"Succesfully transefered {amount} people to {user}'s country!",
                        )
                    )

            else:

                if amount.lower() == "half":
                    await update(
                        (
                            ctx.author.id,
                            b[0][0],
                            int(b[0][1] / 2),
                            b[0][2],
                            b[0][3],
                            b[0][4],
                            b[0][10],
                        )
                    )

                    await update(
                        (
                            user,
                            a[0][0],
                            a[0][1] + int(b[0][1] / 2),
                            a[0][2],
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )

                    await ctx.send(
                        embed=discord.Embed(
                            title="Success!",
                            description=f"Succesfully transefered {int(b[0][1]/2)} people to {user}'s country!",
                        )
                    )

                elif amount.lower() == "all":
                    await update(
                        (ctx.author.id, b[0][0], 0, b[0][2], b[0][3], b[0][4], b[0][10])
                    )

                    await update(
                        (
                            user,
                            a[0][0],
                            a[0][1] + b[0][1],
                            a[0][2],
                            a[0][3],
                            a[0][4],
                            a[0][10],
                        )
                    )

                    await ctx.send(
                        embed=discord.Embed(
                            title="Success!",
                            description=f"Succesfully transefered {int(b[0][1])} people to {user}'s country!",
                        )
                    )

                else:
                    embed = discord.Embed(
                        title="Hey!", description=":x: That is not a valid amount!"
                    )
                    await ctx.send(embed=embed)
        except OverflowError:
            await ctx.send(":x: You can't gift that much at a time")

    @cog_ext.cog_slash(description="Change your country name!")
    async def change(self, ctx, *, name: str):
        await ctx.defer(hidden=True)
        arg = name
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        if len(arg) > 50:
            embed = discord.Embed(
                title="Hey!", description=":x: The name can only be up to 50 characters"
            )
            await ctx.send(embed=embed)
            return

        arg = arg.replace("'", "`")
        await update((ctx.author.id, arg, a[0][1], a[0][2], a[0][3], a[0][4], a[0][10]))
        embed = discord.Embed(
            title="Success",
            description=f"Country name Has been succesfully changed to {arg}",
        )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(description="Get your daily allowance of population...")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        await ctx.defer(hidden=True)
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        await update(
            (
                ctx.author.id,
                a[0][0],
                a[0][1] + int((100 * (((a[0][1] ** 0.5) / 100)) * (a[0][5] + 1))),
                a[0][2],
                a[0][3],
                a[0][4],
                a[0][10],
            )
        )

        embed = discord.Embed(
            title="Daily",
            description=f"`{int((100 * ((a[0][1]**0.5)/100)) * (a[0][5] +1))}` more people joined your country!! Your new population is `{a[0][1] + int((100 * ((a[0][1]**0.5)/100)) * (a[0][5] +1))}`",
        )

        await ctx.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time1 = error.retry_after
            em = discord.Embed(
                title="Slow it down!",
                description=f"""Try again after `{datetime.timedelta(seconds = time1)}`.""",
            )
            await ctx.send(embed=em)

    @cog_ext.cog_context_menu(name="View country profile", target=ContextMenuType.USER)
    async def view_country_profile(self, ctx: MenuContext):
        await ctx.defer(hidden=True)
        member = ctx.target_author
        try:
            a = await reading(member.id)
            name = a[0][0]
            username = member.name
            discriminator = member.discriminator

            username = username.replace(" ", "%20")

            amount12 = 36 + len(str(member.id))
            url = f"https://cbotdiscord.npcool.repl.co/{member.id}/{str(member.avatar_url)[amount12:][:-15]}/{str(username)}/{str(discriminator)}"
            embed = discord.Embed(
                title=f"""{name}""",
                url=url,
                description=f"""Population: `{"{:,}".format(a[0][1])}`
                      Multiplier: `{"{:,}".format(a[0][2])}`
                      Job: `{a[0][3]}`
                      Work Ethic: `{a[0][4]}`
                      Office: `{dic[a[0][4]]}`
                      Work Commands Issued: 
                      `{a[0][10]}`
                      Coins: {a[0][11]} :coin:
                      """,
            )

            embed.add_field(
                name="War",
                value=f"""Wars Played: `{a[0][7]}`
                      Wars Won: `{a[0][8]}`
                      Wars Lost: `{a[0][9]}`
                      """,
            )

            embed.add_field(
                name="Prestige",
                value=f"""Prestige Level: `{a[0][5]}`
                      Prestige Requirement `{a[0][6]}` population""",
            )

            embed.set_thumbnail(url=member.avatar_url)

            if dic[a[0][4]] == "Mom's basement":
                embed.set_image(
                    url="http://www.storefrontlife.com/wp-content/uploads/2013/01/Basement.jpg"
                )
            elif dic[a[0][4]] == "Apartment (with roomate)":
                embed.set_image(
                    url="https://res.cloudinary.com/hemcfvrk2/image/upload/c_lfill,g_xy_center,x_1516,y_615,w_1200,h_700,q_auto:eco,fl_lossy,f_auto/v1485383879/uhzs2wektoh0mb5rkual.jpg"
                )

            elif dic[a[0][4]] == "Mansion":
                embed.set_image(
                    url="https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2013/08/26/100987825-121017_EJ_stone_mansion_0014r.600x400.jpg?v=1395082652"
                )

            elif dic[a[0][4]] == "Home Office":
                embed.set_image(
                    url="https://cdn1.epicgames.com/ue/product/Screenshot/01B-1920x1080-6fd10f5c37639159b1d7a57a869aa3ed.png?resize=1&w=1600"
                )

            elif dic[a[0][4]] == "Space Base":
                embed.set_image(
                    url="https://cdna.artstation.com/p/assets/images/images/000/630/350/large/jarek-kalwa-space-base.jpg?1429173581"
                )

            embed.set_footer(text=f"Tax your citizens with `/tax` to earn coins!")

            await ctx.send(embed=embed)

        except KeyError:
            embed = discord.Embed(
                title="Hey!",
                description=f":x: You or the person you are viewing do not have a country! Create one with `/start`",
            )
            await ctx.send(embed=embed)


class Games2(
    commands.Cog, description="Cool games that test your geography skills (slash)"
):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(description="Wage war on your friends!")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def war(self, ctx, user: discord.Member):
        await ctx.defer(hidden=True)
        b = user.id

        opponent = user

        if int(b) == int(ctx.author.id):
            embed = discord.Embed(
                title="Stop!", description=":x: You can't wage war on yourself!"
            )
            await ctx.send(embed=embed)
            return

        user1 = await reading(ctx.author.id, ctx)
        if user1 is None:
            return
        try:
            user2 = await reading(b)
        except:
            embed = discord.Embed(
                title="Sorry",
                description=f""":x: This user doesn't have a country yet""",
            )

            await ctx.send(embed=embed)
            return

        if user1[0][1] == 0 or user2[0][1] == 0:
            await ctx.send(
                ":x: Hey! One of you has only 0 population! You can't go to war like that smh"
            )
            return

        await ctx.send(
            f"<@!{b}>, you have 20 seconds to accept <@!{ctx.author.id}> request to war. Type `accept` in the chat to accept, or type `deny` in the chat to end the conflict"
        )

        def check(m):
            return (
                m.channel == ctx.channel
                and m.author == opponent
                and m.content.lower() == "accept"
                or m.content.lower() == "deny"
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=20)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="Whoops",
                description=":x: Time ran out. The war preperations took too long. No war",
            )
            await ctx.send(embed=embed)
            return

        if msg.content.lower() == "accept":
            embed = discord.Embed(
                title="Accepted",
                description=f"<@!{ctx.message.author.id}> your opponent accepted!!",
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Phew", description="Crisis averted. There is no war"
            )
            await ctx.send(embed=embed)
            return

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.message.author

        n = True
        a = 0
        while n:
            if a == 4:
                await ctx.send("You tried this too many times, quitting game..")
                return
            await ctx.send(
                f"<@!{ctx.message.author.id}> how many troops do you want to deploy, type `quit` to end"
            )
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send("Time ran out. No war :(")
                return

            try:
                num = float(msg.content)

                if num <= 0:
                    await ctx.send("You can't go to war with less than 0 people smh")
                    a += 1
                    continue

                else:
                    pass

            except:
                if msg.content.lower().startswith("quit"):
                    await ctx.send(":x: Game quit")
                    return
                await ctx.send("That is not a valid amount!!")
                a += 1
                continue

            if num.is_integer():
                if int(msg.content) < user1[0][1]:
                    await ctx.send(f"{msg.content} people deployed")
                    user1_troops = int(msg.content)
                    break
                else:
                    await ctx.send(
                        f":x: <@!{ctx.message.author.id}> you dont have enough people!!!!"
                    )
                    a += 1
                    continue
            else:
                await ctx.send(f"{msg.content} is not a valid amount")
                a += 1
                continue

        def check(m):
            return m.channel == ctx.channel and m.author == opponent

        a = 0
        while n:
            if a == 4:
                await ctx.send("You tried this too many times! quitting game...")
                return
            await ctx.send(
                f"{user} how many troops do you want to deploy, type `quit` to end"
            )
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send("Time ran out. No war :(")
                return
            try:
                num = float(msg.content)

                if num <= 0:
                    await ctx.send("You can't go to war with less than 0 people smh")
                    a = a + 1
                    continue
            except:
                if msg.content.lower() == "quit":
                    await ctx.send(":x: Game Quit")
                    return
                await ctx.send("That is not a valid amount!!")
                a = a + 1
                continue

            if num.is_integer():
                if int(msg.content) < user2[0][1]:
                    await ctx.send(f"{msg.content} people deployed")
                    user2_troops = int(msg.content)
                    break
                else:
                    await ctx.send(f":x: {user} you dont have enough people!!!!")
                    a = a + 1
                    continue
            else:
                await ctx.send(f"{msg.content} is not a valid amount")
                a = a + 1
                continue

        random_country = random.choice(quiz_country_list)
        country_capital1 = CountryInfo(random_country)
        country_capital = country_capital1.capital()

        if not country_capital:
            random_country = random.choice(quiz_country_list)
            country_capital1 = CountryInfo(random_country)
            country_capital = country_capital1.capital()

        country_capital = (
            unicodedata.normalize("NFKD", country_capital)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )

        # try:

        result4 = coco.convert(names=random_country, to="ISO2")

        await ctx.send(
            f"What is the capital of....... `{random_country.title()}` {lookup(result4)}"
        )

        # except:
        # await ctx.channel.send(f"What is the capital of....... `{random_country}`")

        def check(m):

            return (
                m.content.lower() == country_capital.lower()
                and m.channel == ctx.channel
                and int(m.author.id) in [int(b), int(ctx.author.id)]
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30)

        except asyncio.TimeoutError:
            await ctx.send("Time ran out. Draw!!!")
            return

        if msg.author == ctx.author:
            await ctx.channel.send(
                f"<@!{ctx.author.id}> you gave the answer first. You won the war!!! :crown:"
            )
            await update_war(
                (
                    ctx.author.id,
                    user1[0][0],
                    user1[0][1] + user2_troops,
                    user1[0][2],
                    user1[0][3],
                    user1[0][4],
                    user1[0][5],
                    user1[0][6],
                    user1[0][7] + 1,
                    user1[0][8] + 1,
                    user1[0][9],
                )
            )

            await update_war(
                (
                    b,
                    user2[0][0],
                    user2[0][1] - user2_troops,
                    user2[0][2],
                    user2[0][3],
                    user2[0][4],
                    user2[0][5],
                    user2[0][6],
                    user2[0][7] + 1,
                    user2[0][8],
                    user2[0][9] + 1,
                )
            )

        else:
            await ctx.channel.send(
                f"{user} you gave the answer first. You won the war!!! :crown:"
            )
            await update_war(
                (
                    ctx.author.id,
                    user1[0][0],
                    user1[0][1] - user1_troops,
                    user1[0][2],
                    user1[0][3],
                    user1[0][4],
                    user1[0][5],
                    user1[0][6],
                    user1[0][7] + 1,
                    user1[0][8],
                    user1[0][9] + 1,
                )
            )

            await update_war(
                (
                    b,
                    user2[0][0],
                    user2[0][1] + user1_troops,
                    user2[0][2],
                    user2[0][3],
                    user2[0][4],
                    user2[0][5],
                    user2[0][6],
                    user2[0][7] + 1,
                    user2[0][8] + 1,
                    user2[0][9],
                )
            )

    @war.error
    async def war_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                title="Hey!",
                description=f"""You can't wage war right now! Try again in `{error.retry_after:.2f}`s.""",
            )
            await ctx.send(embed=em)

    @cog_ext.cog_subcommand(
        base="guess",
        description="Guess the capitals of countries. This game lasts for 10 minutes.",
        name="capital",
    )
    async def guess_capital(self, ctx):
        await ctx.defer(hidden=True)
        the_author = ctx.author
        channel = ctx.channel

        await ctx.send("How long should the time limit be (**in seconds**)")

        def check1(m):
            return (
                m.content.isdigit()
                and m.author == the_author
                and m.channel == channel
                and int(m.content) <= 300
            )

        msg1 = await self.bot.wait_for("message", check=check1)

        length = int(msg1.content)

        correct_ans = {}

        count = 0

        start = time.monotonic()
        while time.monotonic() - start < 600:
            random_country = random.choice(quiz_country_list)
            try:
                country_capital1 = CountryInfo(random_country)

                country_capital = country_capital1.capital()
            except:
                random_country = random.choice(quiz_country_list)
                country_capital1 = CountryInfo(random_country)

                country_capital = country_capital1.capital()

            if not country_capital:
                try:
                    random_country = random.choice(quiz_country_list)
                    country_capital1 = CountryInfo(random_country)

                    country_capital = country_capital1.capital()
                except:
                    random_country = random.choice(quiz_country_list)
                    country_capital1 = CountryInfo(random_country)

                    country_capital = country_capital1.capital()

            country_capital = (
                unicodedata.normalize("NFKD", country_capital)
                .encode("ascii", "ignore")
                .decode("utf-8")
            )

            # try:

            result4 = coco.convert(names=random_country, to="ISO2")

            await ctx.send(
                f"What is the capital of....... `{random_country.title()}` {lookup(result4)}"
            )

            # except:
            # await ctx.channel.send(f"What is the capital of....... `{random_country}`")

            def check(m):
                return (
                    fuzz.ratio(country_capital.lower(), m.content.lower()) > 85
                    or m.content.lower() == "quit"
                    and m.channel == channel
                )

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=length)

                if msg.content == "quit":
                    await ctx.send("Game Over")
                    return

                if msg.author.id not in correct_ans:
                    correct_ans[msg.author.id] = 1
                    count += 1

                else:
                    correct_ans[msg.author.id] += 1
                    count += 1

                await ctx.send(
                    f"That is the correct answer!!! 🏆 Good Job <@{msg.author.id}>"
                )

            except asyncio.TimeoutError:
                try:
                    await ctx.send(
                        f"""Time has run out!! ***Game Over***. Total score: `{count}` 
  The highest scorer in this match was <@{max(correct_ans, key=lambda key: correct_ans[key])}> with a score of `{correct_ans[msg.author.id]}` GG"""
                    )
                    return
                except:
                    await ctx.send("No one scored in this match. :cry: Total score `0`")
                    return

        await ctx.send("10 mintues have passed! The game is over! Good job everyone!")

    @cog_ext.cog_subcommand(
        base="guess",
        name="country",
        description="Guess countries from their capitals. This game lasts for 10 minutes.",
    )
    async def reverse(self, ctx):
        await ctx.defer(hidden=True)
        the_author = ctx.author
        channel = ctx.channel

        await ctx.send("How long should the time limit be (**in seconds**)")

        def check1(m):
            return (
                m.content.isdigit()
                and m.author == the_author
                and m.channel == channel
                and int(m.content) <= 300
            )

        msg1 = await self.bot.wait_for("message", check=check1)

        length = int(msg1.content)
        count = 0

        correct_ans = {}

        start = time.monotonic()

        while time.monotonic() - start < 600:
            try:
                random_country = random.choice(quiz_country_list)

                country_capital1 = CountryInfo(random_country)

                country_capital = country_capital1.capital()
            except:
                random_country = random.choice(quiz_country_list)

                country_capital1 = CountryInfo(random_country)

                country_capital = country_capital1.capital()

            result4 = coco.convert(names=random_country, to="ISO2")

            await ctx.send(
                f"What Country has `{country_capital.title()}` as its capital. Here is a hint: {lookup(result4)}"
            )

            def check(m):
                return (
                    m.content.lower() == "quit"
                    or fuzz.ratio(random_country.lower(), m.content.lower()) > 82
                    and m.channel == channel
                )

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=length)

                if msg.content.lower() == "quit":
                    await ctx.send("Game quit")
                    return

                if msg.author.id not in correct_ans:
                    correct_ans[msg.author.id] = 1
                    count += 1

                else:
                    correct_ans[msg.author.id] += 1
                    count += 1

                await ctx.send(
                    f"That is the correct answer!!! 🏆 Good Job <@{msg.author.id}>"
                )

            except asyncio.TimeoutError:
                try:
                    await ctx.send(
                        f"""Time has run out!! ***Game Over***. Total score: `{count}` 
    The highest scorer in this match was <@{max(correct_ans, key=lambda key: correct_ans[key])}> with a score of `{correct_ans[msg.author.id]}` GG"""
                    )
                    return
                except:
                    await ctx.send("No one scored in this match. :cry: Total score `0`")
                    return
        await ctx.send("10 minutes have passed! Good job everyone!!")


def setup(bot):
    bot.add_cog(EconomyCommands2(bot))
    bot.add_cog(Games2(bot))
