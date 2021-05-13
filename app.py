import discord
import re
import asyncio
import math
import dao
from discord.ext import commands
from os import environ

BOT_TOKEN = environ.get("BOT_TOKEN")
SUPPORT_USER_ID = environ.get("SUPPORT_USER_ID")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=">", intents=intents)


@bot.command()
async def copped(ctx, shoe_copped, copped_by: discord.Member, copped_for: discord.Member):
    entry_id = dao.insert_new_copdoc_entry(shoe_copped, str(copped_by.id), str(copped_for.id))
    await ctx.message.delete()
    await ctx.send(
        "\n**{}**"
        "\nCopped by - {}"
        "\nSent to - {} "
        "\nEntry ID - {}".format(shoe_copped, copped_by.mention, copped_for.mention, entry_id))


@bot.command()
async def delete(ctx, entry_id):
    dao.delete_copdoc_entry(entry_id)
    channel = ctx.message.channel
    async for message in channel.history():
        if re.search(r"\bEntry ID - %s\b" % entry_id, message.content):
            await message.delete()
    await ctx.message.delete()
    message = await ctx.send("Removed cop-doc entry {}".format(entry_id))
    await asyncio.sleep(3)
    await message.delete()


@bot.command()
async def copboard(ctx):
    formatted_cop_board = get_formatted_cop_board(ctx.guild, dao.get_helper_leader_board())
    await ctx.message.delete()
    await ctx.send(formatted_cop_board)


@bot.command()
async def copstats(ctx, member: discord.Member):
    await ctx.message.delete()
    await ctx.send(format_member_stats(member))


def get_formatted_cop_board(guild, cop_board):
    cop_board_string = "**Cop Doc Leader Board**\n\n"
    for entry in cop_board:
        user_mention = guild.get_member(int(entry[0]))
        if user_mention is not None:
            cop_board_string += user_mention.mention + ' - ' + str(entry[1]) + " cop(s)\n"
    return cop_board_string


def get_helpee_helper_ratio(helper_count, helpee_count):
    ratio_string = "0:0"
    if helper_count == 0 and helpee_count != 0:
        ratio_string = "0:" + str(helpee_count)

    if helpee_count == 0 and helper_count != 0:
        ratio_string = str(helper_count) + ":0"

    if helper_count != 0 and helpee_count != 0:
        numbers = [helper_count, helpee_count]
        denominator = math.gcd(helper_count, helpee_count)
        ratio = [i / denominator for i in numbers]
        ratio_string = ':'.join(str(int(i)) for i in ratio)

    return ratio_string


def format_member_stats(member):
    helper_count = dao.get_member_count_by_query_type(member.id, dao.HELPER_COUNT_QUERY)
    helpee_count = dao.get_member_count_by_query_type(member.id, dao.HELPEE_COUNT_QUERY)

    if helpee_count == 0 and helper_count == 0:
        return "No cop stats found for {}. Think this is wrong? Contact {}."\
            .format(member.mention, SUPPORT_USER_ID)

    formatted_member_stats = "**Cop Stats**" \
        "\nMember - {}\nCops sent - {}\nCops received - {}\nRatio - {}\n\nSee a problem? Contact {}."\
        .format(member.mention, str(helper_count), str(helpee_count),
                get_helpee_helper_ratio(helper_count, helpee_count), SUPPORT_USER_ID)
    return formatted_member_stats


bot.run(BOT_TOKEN)
