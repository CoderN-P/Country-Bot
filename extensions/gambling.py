from discord.ext import commands
from mongomethods import (
    count,
    reading,
    update,
    update_prestige,
    update_war,
    writing,
    delete_task,
    search_name,
    update_coins,
)

import discord
import random
import asyncio
import datetime


class Gambling(
    commands.Cog, description="Commands that allow you to gamble with Country Bot"
):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief="Gamble with dice against Country Bot for population",
        description="Gamble with dice against Country Bot for population",
    )
    async def dice(self, ctx, amount):
        try:
            amount = int(amount)
        except:
            await ctx.send(":x: That isn't a valid amount")
            return

        if amount <= 0:
            await ctx.send(":x: That isnt a valid amount")
            return

        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        if amount >= a[0][1]:
            await ctx.send(":x: You do not have that much population to bet")

        else:
            user_dice1 = random.randint(1, 6)
            user_dice2 = random.randint(1, 6)
            await ctx.send(f"You rolled {user_dice1} and {user_dice2} :game_die:")
            await asyncio.sleep(1)
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            await ctx.send(f"I rolled {dice1} and {dice2} :game_die:")
            if (dice1 + dice2) < (user_dice1 + user_dice2):
                await ctx.send(":( I lost again! I WILL NEVER WIN! GG, ugh.")
                await ctx.send(
                    "<:angrycbot:863148860616212501> <:angrycbot:863148860616212501> <:angrycbot:863148860616212501>"
                )
                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1] + amount,
                        a[0][2],
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    )
                )
            elif (dice1 + dice2) == (user_dice1 + user_dice2):
                await ctx.send(
                    "<:Thinkingcbot:863151583294521344> Its a draw. so no one won"
                )
                await ctx.send(
                    "<:sadcbot:863150212989845514> <:sadcbot:863150212989845514> <:sadcbot:863150212989845514>"
                )

            else:
                await ctx.send("YES. I WON!!!! WOHOOOOOO :partying_face:")
                await ctx.send(
                    "<:laughcbot:863151389042933800> <:laughcbot:863151389042933800> <:laughcbot:863151389042933800>"
                )
                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1] - amount,
                        a[0][2],
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    )
                )

    @commands.command(
        brief="Flip a coin with Country Bot, to win population (or loose some)",
        description="Flip a coin with Country Bot, to win population (or loose some)",
    )
    async def coinflip(self, ctx, choice, *amount):
        h_t = random.choice(["h", "t"])
        a = await reading(ctx.author.id, ctx)
        if a is None:
            return

        if choice.lower() not in ["heads", "tails"]:
            embed = discord.Embed(
                title="huh",
                description=":x: That is not a valid option. Specify either `heads` or `tails`",
            )
            await ctx.channel.send(embed=embed)
            return

        if len(amount) == 0:
            if a[0][1] <= 0:
                embed = discord.Embed(
                    title="Hey!",
                    description=":x: You don't have enough people to do this command",
                )
                await ctx.channel.send(embed=embed)
                return

            if h_t == "h":
                confirmed = "heads"

            else:
                confirmed = "tails"

            if confirmed == choice:
                embed = discord.Embed(
                    title="Woohooooo!!!",
                    description=":tada: Your guess was correct!! You won `1` population!!!",
                )

                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1] + 1,
                        a[0][2],
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    )
                )

                await ctx.channel.send(embed=embed)

            else:
                embed = discord.Embed(
                    title=":(",
                    description=":slight_frown: Your guess was incorrect. You lost `1` population",
                )

                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1] - 1,
                        a[0][2],
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    )
                )

                await ctx.channel.send(embed=embed)

        else:

            try:
                amount = int(amount[0])
            except:
                embed = discord.Embed(
                    title="Error", description=":x: You have entered an invalid amount!"
                )
                await ctx.send(embed=embed)
                return

            if amount < 1:
                await ctx.send(":x: You can't bet with this amount smh")
                return

            if a[0][1] <= int(amount):
                embed = discord.Embed(
                    title="Hey!",
                    description=":x: You don't have that much population to bet",
                )
                await ctx.send(embed=embed)
                return

            if h_t == "h":
                confirmed = "heads"

            else:
                confirmed = "tails"

            if confirmed == choice:
                embed = discord.Embed(
                    title="Woohooooo!!!",
                    description=f":tada: Your guess was correct!! You won `{amount}` population!!!",
                )

                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1] + int(amount),
                        a[0][2],
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    )
                )

                await ctx.channel.send(embed=embed)

            else:
                embed = discord.Embed(
                    title=":(",
                    description=f":slight_frown: Your guess was incorrect. You lost `{amount}` population",
                )

                await update(
                    (
                        ctx.author.id,
                        a[0][0],
                        a[0][1] - amount,
                        a[0][2],
                        a[0][3],
                        a[0][4],
                        a[0][10],
                    )
                )

                await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Gambling(bot))
