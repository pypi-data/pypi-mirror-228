import discord
from CharmCord.CharmErrorHandling import CharmCordErrors
from CharmCord.all_functions import newline_char


async def sendEmbed(args: str, Context):
    """
    Ex. $sendEmbed[Channel ID;Title;Message;Color?;image?;Footer?]
    Send an Embed
    """
    from CharmCord.Classes.CharmCord import bots

    args = args.replace(newline_char, "\n")
    split = args.split(";")
    try:
        channel_id = split[0]
        title = split[1]
        message = split[2]
        color = split[3]
        image = split[4]
        footer = split[5]
        channel = await bots.fetch_channel(int(channel_id))
        embed = eval(
            f"discord.Embed(title=title, description=message, color=discord.Color.{color.lower()}())"
        )
        embed.set_footer(text=footer)
        embed.set_image(url=image)

        if isinstance(Context, discord.Interaction):
            try:
                await Context.response.send_message(embed=embed)
                message = await Context.original_response()
                return message.id
            except:
                await Context.followup.send(embed=embed)
                message = await Context.original_response()
                return message.id
        message = await channel.send(embed=embed)
    except discord.ClientException:
        raise SyntaxError("Can't send empty message!")
    except IndexError:
        raise SyntaxError("Not enough arguments in $sendEmbed")
    except SyntaxError:
        channel_id = split[0]
        title = split[1]
        message = split[2]
        image = split[4]
        footer = split[5]
        channel = await bots.fetch_channel(int(channel_id))
        embed = eval("discord.Embed(title=title, description=message)")
        embed.set_footer(text=footer)
        embed.set_image(url=image)
        if isinstance(Context, discord.Interaction):
            try:
                await Context.response.send_message(embed=embed)
                message = await Context.original_response()
                return message.id
            except:
                await Context.followup.send(embed=embed)
                message = await Context.original_response()
                return message.id
        message = await channel.send(embed=embed)
    return message.id
