import asyncio
import random

import discord

from bot_utils.mongomethods import reading, update

words = ["come here!", "more people!", "🙂", "hello!"]


class BackgroundTasks:

    def __init__(self, bot):
        self.bot = bot

    async def presence(self):
        while True:
            await self.bot.change_presence(activity=discord.Game(name=".help"))
            await asyncio.sleep(10)
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening,
                                          name="@Country Bot prefix"))
            await asyncio.sleep(10)
            await self.bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.bot.guilds)} guilds and {sum(guild.member_count for guild in self.bot.guilds)} users!",
            ))
            await asyncio.sleep(10)

    # setting the status of the bot and sending a message if the guild is not in db

    async def refugee_drops(self):
        channel = await self.bot.fetch_channel(836624980359643176)

        while True:
            word = random.choice(words)
            amount = random.randint(100, 1000)

            message = await channel.send(embed=discord.Embed(
                title="Refugees",
                description=f"{amount} refugees have showed up. Who will be the first person to bring them in! Say `{word}` to bring them in!!",
            ))

            def check(m):
                return m.content == word and m.channel == channel

            n = True
            while n:
                try:
                    msg = await self.bot.wait_for("message",
                                                  check=check,
                                                  timeout=30)

                    try:
                        a = await reading(msg.author.id)
                    except:
                        embed = discord.Embed(
                            title="Sorry",
                            description=f":x: You don't have a country. Type `.start` to start one",
                        )
                        await msg.channel.send(embed=embed)
                        n = True

                    await update((
                        msg.author.id,
                        a[0][0],
                        a[0][1] + amount,
                        a[0][2],
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    ))
                    await msg.reply(embed=discord.Embed(
                        title="Hooray",
                        description=f"{amount} more people added to your country!",
                    ))

                    break

                except asyncio.TimeoutError:
                    await message.delete()
                    break

            await asyncio.sleep(300)
