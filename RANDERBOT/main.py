import random
import requests
import nextcord as discord
import pytemperature
import randfacts
from bs4 import BeautifulSoup
import os
import json
from db import add_ping, remove_ping, ping_check, users_check
import calendar
from nextcord.ext.commands import CommandNotFound
from nextcord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="r!", help_command=None)

@client.event
async def on_ready():
    web = "https://RANDERBOT.samkhan4.repl.co"
    activity = discord.Activity(name="r!help",
                                type=discord.ActivityType.watching,
                                description=f"Our Website: {web}")
    await client.change_presence(status=discord.Status.online,
                                 activity=activity)


@client.command()
async def invite(ctx):
    embed = discord.Embed(
        title="Invite Me!",
        description=
        "[Click Here](https://discord.com/api/oauth2/authorize?client_id=898483755231113228&permissions=0&scope=bot)"
    )
    await ctx.send(embed=embed)


@client.command(aliases=['h'])
async def help(ctx):
    helptext = "```"
    for command in client.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    embed = discord.Embed(title="Help Box",description='`r!` prefix',)
    embed.add_field(name="Commands",
                    value=helptext,
                    inline=False)
    await ctx.author.send(embed=embed)
    await ctx.send("```Check Your Direct Messages !```")


def sub(a: int, c: int):
    return a - c


def add(a: int, c: int):
    return a + c


def mult(a: int, c: int):
    return a * c


def div(a: int, c: int):
    return a / c


def rand(a: int, c: int):
    return random.randint(a, c)

@client.command(aliases=['c'])
async def calc(ctx, a: int, b, d: int):
    try:
        if b == "/":
            divison = div(a, d)
            await ctx.send(f"```{divison}```")
    except ZeroDivisionError:
        await ctx.send("`ZeroDivisionError`")
    if b == "x":
        multiply = mult(a, d)
        await ctx.send(f"```{multiply}```")
    elif b == "-":
        subtract = sub(a, d)
        await ctx.send(f"```{subtract}```")
    elif b == "+":
        addition = add(a, d)
        await ctx.send(f"```{addition}```")
    elif b == "#":
        randi = rand(a, d)
        await ctx.send(f"```{randi}```")
    elif b == "":
        await ctx.send('```Arguments are missing```')


@client.command(aliases=['sm'])
async def slowmode(ctx, time: int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send("`This Command Requires [Manage Messages Permission]`")
        return
    if (ctx.author.guild_permissions.manage_messages):
        if time == 0:
            await ctx.send("```SlowMode is Off```")
        elif time > 21600:
            await ctx.send('```You cannot set slowmode above 6 hours```')
        else:
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.send(f"```Slowmode Set To {time} Seconds!```")


@client.command()
@commands.guild_only()
async def purge(ctx, a: int):
   if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send("```This Command Requires [Manage Messages Permission]```")
        return
   if (ctx.author.guild_permissions.manage_messages):
     await ctx.channel.purge(limit=a)
     await ctx.send(f"```Successfully Purged {a} Messages```")



@client.command()
async def ping(ctx):
    await ctx.send(f'```Pong! In {round(client.latency * 1000)}ms```')


@client.command()
async def month(ctx, a: int, b: int):
    calen = calendar.month(a, b, 3, 1)
    embed = discord.Embed(title="Calendar", description=f"{calen}")
    await ctx.send(embed=embed)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quotes = json_data[0]['q'] + "-" + json_data[0]['a']
    return (quotes)


@client.command()
async def quote(ctx):
    quote = get_quote()
    embed = discord.Embed()
    embed.title = "Rander Quotes"
    embed.description = quote
    embed.set_footer(text="Requested By {} ".format(ctx.message.author.name))
    await ctx.channel.send(embed=embed)


@client.command()
async def web(ctx):
    embed = discord.Embed()
    embed.title = "Rander Bot Page"
    embed.description = "[Our Website](https://randerbot.samkhan4.repl.co/)"
    embed.set_footer(text="Requested By {} ".format(ctx.message.author.name))
    await ctx.send(embed=embed)


@client.command()
async def fact(ctx):
  facts = randfacts.get_fact(True)
  embed = discord.Embed()
  embed.title = "Rander Facts"
  embed.description = facts
  embed.set_footer(text="Requested By {} ".format(ctx.message.author.name))
  await ctx.send(embed=embed)

@client.command(aliases=['weth'])
async def weather(ctx,cityname):
 
 headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
 
 
 def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?channel=nrow5&client=firefox-b-d&q=weather+of+{cityname}', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    global location
    location = soup.select('#wob_loc')[0].getText().strip()
    global tiime
    tiime = soup.select('#wob_dts')[0].getText().strip()
    global info
    info = soup.select('#wob_dc')[0].getText().strip()
    global weatherz
    weatherz = int(soup.select('#wob_tm')[0].getText().strip())
    global imageofweatherz
    imageofweather = soup.select('#wob_tci')[0].attrs['src']
    imageofweatherz = 'https://'+imageofweather[2:]
    print(imageofweatherz)
  
 city = cityname
 city = city+" weather"
 weather(city)
 e = discord.Embed(title=f"Weather Of {location}",color = discord.Color.green())
 e.set_thumbnail(url=f"{imageofweatherz}")
 e.add_field(name=f"Time:",value=f"`{tiime}`",inline=False)
 e.add_field(name=f"Status:",value=f"`{info}`",inline=False)
 e.add_field(name=f"Temperature:",value=f"`{pytemperature.f2c(weatherz)} °C`",inline=False)
 e.set_footer(text="Requested By {} ".format(ctx.message.author.name))
 await ctx.send(embed=e)


@client.command()
async def info(ctx,item):
 searchitem = item
 def imageget(itemz):
    res = requests.get(f'https://www.google.com/search?q={itemz}_image&client=firefox-b-d&channel=nrow5&sxsrf=AOaemvIUCv4OMQlWyeUKmBfTXWiRrYgXkA:1642743132241&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj8j-qGj8L1AhV0wjgGHQmHBsoQ_AUoA3oECAIQBQ')
    soup = BeautifulSoup(res.text, 'html.parser')
    global imagelink
    imagelink = soup.select('.yWs4tf')[0]['src']
 imageget(searchitem)
 headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
 res = requests.get(f'https://en.wikipedia.org/w/index.php?search={item}&title=Special:Search&profile=advanced&fulltext=1&ns0=1',headers=headers)
 soupe = BeautifulSoup(res.text, 'html.parser')
 global heading
 try:
     heading = soupe.select('.searchresult')[0].getText()
     global heading2 
     heading2 = soupe.select('.searchresult')[1].getText()
     global heading3
     heading3 = soupe.select('.searchresult')[2]  .getText()
     global heading4
     heading4 = soupe.select('.searchresult')[3].getText()
     global heading5
     heading5 = soupe.select('.searchresult')[4].getText()
     global link
     link = soupe.select('.mw-search-result-heading')[0].contents[0]['href']
     global hoding
     hoding = soupe.select('.mw-search-result-heading')[0].contents[0]['title']
     global hoding2
     hoding2 = soupe.select ('.mw-search-result-heading')[1].contents[0]['title']
     global hoding3
     hoding3 = soupe.select('.mw-search-result-heading')[2].contents[0]['title']
     global hoding4
     hoding4 = soupe.select('.mw-search-result-heading')[3].contents[0]['title']
     global hoding5
     hoding5 = soupe.select('.mw-search-result-heading')[4].contents[0]['title']
     embed = discord.Embed(title=f"Info for {item.capitalize()}",color = discord.Color.green())
     embed2 = discord.Embed(title=f"Extra Info For {item.capitalize()}",color = discord.Color.green())
     embed.set_thumbnail(
            url=f"{imagelink}"
        )
     embed.add_field(name=hoding,value=heading,inline=False)
     embed2.add_field(name=hoding2.capitalize(),value=heading2,inline=False)
     embed2.add_field(name=hoding3.capitalize(),value=heading3,inline=False)
     embed2.add_field(name=hoding4.capitalize(),value=heading4,inline=False)
     embed.set_footer(text="Requested By {}\nReact Below To Get Realed Items".format(ctx.message.author.name))
     embed2.set_footer(text="Requested By {}".format(ctx.message.author.name))
     embed2.add_field(name=hoding5.capitalize(),value=heading5,inline=False)
     embed.add_field(name="Get More Info",value=f'[Get Full Info](https://en.wikipedia.org/{link})',inline=False)
     wikinfo = await ctx.send(embed=embed)
     await wikinfo.add_reaction('➕')
     def check_reaction(reaction, reaction_user):
       return reaction.emoji == "➕" and reaction_user == ctx.author and reaction.message == wikinfo
     while True:
       try:
          reaction, user = await client.wait_for("reaction_add", timeout=10, check=check_reaction)
          await ctx.send(embed=embed2)
          break
       except:
          pass

 except IndexError:
     embod = discord.Embed(title=f"No Info Found for {item.capitalize()}",color = discord.Color.red())
     await ctx.send(embed=embod)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        embed = discord.Embed(title="Oops !",color = discord.Color.red())
        embed.add_field(name="Command Not Found !",value ="Try Running **r!help** For Available Commands")
        await ctx.send(embed=embed)
    if isinstance(error,commands.MissingRequiredArgument):
       embed = discord.Embed(title="Oops !",color = discord.Color.red())
       embed.add_field(name="This Command Requires 1 Postional Arguement. ",value ="Try Running **r!help** For Detailed Information")
       await ctx.send(embed=embed)
    if isinstance(error,commands.BotMissingPermissions):
        embed = discord.Embed(title="Oops !",color = discord.Color.red())
        embed.add_field(name="I Don't Have Permisson To Execute Following Command. ",value ="Try Running **r!help** For Other Commands")
        await ctx.send(embed=embed)
    raise error

@client.command()
async def addbump(ctx):
 if ctx.guild.id == 813660012001624124:
  serverID = ctx.message.guild.id
  authorID = ctx.author.id
  name = ctx.message.author.name
  vfy = ping_check()
  if authorID in vfy:
    await ctx.send('User Already Exsist !')
  else:
    add_ping(serverID,authorID,name)
    await ctx.send('User Added To Bump Ping Successfully !')
 else:
   await ctx.send('`Command is Not Made For This Server !`')
@client.command()
async def removebump(ctx):
 if ctx.guild.id == 813660012001624124:
  authorID = ctx.author.id
  vfy = ping_check()
  if authorID in vfy:
    remove_ping(authorID)
    await ctx.send('Deleted Ping Successfully')
  else:
    await ctx.send('No User Exsist !')
 else:
   await ctx.send('`Command Is Not Made For This Server`')

@client.event
async def on_message(message):
 if message.guild.id == 813660012001624124:
  if message.author.id == 765598792535244820:
   try:
    embeds = message.embeds[0]
   except:
     pass
   message_to_vfy = '!d bump'
   if message_to_vfy in embeds.description:
    ussrs = ping_check()
    if not ussrs:
      pass
    else:
     for usr in ussrs:
      await message.channel.send(f"<@{usr}>")
     await message.channel.send('`Please Run /bump to Bump Server`')
   else:
     pass
  else:
    await client.process_commands(message)
 else:
     await client.process_commands(message)

@client.command()
async def bumplist(ctx):
 if ctx.guild.id == 813660012001624124:
  embed = discord.Embed(title="Rander Bump Users",color = discord.Color.green())
  bump_users = users_check(ctx.guild.id)
  count = 1
  if not bump_users:
    embed.add_field(name = 'Users Not Found',value="No users Found!")
    return
  else:
    for users in bump_users:
     embed.add_field(name=f"{count}.{users}", value=">>>", inline=False)
     count+=1
    await ctx.send(embed=embed)
 else:
   await ctx.send('`Command Is Not Made For This Server`')

keep_alive()
client.run(os.getenv('BOTKEY'))
