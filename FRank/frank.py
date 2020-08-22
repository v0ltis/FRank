# coding: utf-8
import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import random
from img import generator as CardGen
import traceback
import requests
import shutil
import re
import datetime
import json
file = open("levels.json","r").read()
exec(f"data = {file}")
file = open("sentences.json","r").read()
LevelUpMsg = json.loads(file)
file =  open("roles.json","r").read()
exec(f"roles = {file}")
frank = commands.Bot(command_prefix = '^')
wait = []
mentions = discord.AllowedMentions(everyone=False, users=False, roles=False)
class CustomMessage():
    def __init__(self,userName,userDiscrim,userId,userMention,guildName,guildId,guildMemberCount,\
    channelId,channelName,channelMention,second,minute,hour,intDay,intMonth,year,\
    userLevel,oldUserLevel,userRank,userRanked,strDay,strMonth):
        # user
        self.userName = userName
        self.userDiscrim = userDiscrim
        self.userId = userId
        self.userMention = userMention
        # guild :
        self.guildName = guildName
        self.guildId = guildId
        self.guildMemberCount = guildMemberCount
        # channel:
        self.channelId =channelId
        self.channelName =channelName
        self.channelMention =channelMention
        # hour :
        self.second =second
        self.minute =minute
        self.hour =hour
        self.intDay =intDay
        self.intMonth =intMonth
        self.year =year
        # XP
        self.userLevel =userLevel
        self.oldUserLevel = oldUserLevel
        self.userRank =userRank
        self.userRanked =userRanked
        self.strDay=strDay
        self.strMonth = strMonth

    def __repr__(self):
        return None

    def __str__(self):
        return None


@tasks.loop(seconds=15)
async def save():
    global data, LevelUpMsg,roles
    file = open("levels.json","w")
    file.write(str(data))
    json.dump(LevelUpMsg, open("sentences.json","w"))
    file = open("roles.json","w")
    file.write(str(roles))


async def GenClass(user,channel):
    global CustomMessage, data
    levels = data[channel.guild.id]
    guild = channel.guild
    NVal = []
    for x in levels:
        NVal.append([x, levels[x]["level"], levels[x]["xp"]])
    def CShort(e):
        return int(e[1] * 10000000000) + int(e[2])
    NVal.sort(key=CShort,reverse=True)
    pos = 0
    for x in NVal:
        pos +=1
        if x[0] == user.id:
            break
    date = datetime.datetime.now()
    jour = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"][int(date.strftime("%w"))]
    mois = ["janvier","fevrier","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"][int(date.strftime("%m"))-1]
    return CustomMessage(user.name,user.discriminator,user.id,user.mention,guild.name,guild.id,guild.member_count,\
    channel.id,channel.name,channel.mention,date.strftime("%S"),date.strftime("%M"),date.strftime("%H"),date.strftime("%d"),date.strftime("%m"),date.strftime("%Y"),\
    levels[user.id]["level"]+1,levels[user.id]["level"],pos,len(NVal),jour,mois)

async def reset(user=None,guild=None):
    global data
    if user == None:
        data[guild] = {}
    else:
        user = int(user)
        del data[guild][user]
        data[guild][user] = {}
        data[guild][user]["xp"] = 0
        data[guild][user]["level"] = 1
async def update_data(user,guild):
    global data
    if not user in data[guild]:
        data[guild][user] = {}
        data[guild][user]["xp"] = 0
        data[guild][user]["level"] = 1

async def add_experience(user,guild):
    if not user.id in wait:
        global data
        if int(datetime.datetime.today().weekday()) == 6:
            data[guild][user.id]["xp"] += random.randint(10,30)
        else:
            data[guild][user.id]["xp"] += random.randint(5,15)
        wait.append(user.id)
        await asyncio.sleep(30)
        wait.remove(user.id)
async def addLevel(user,guild):
    global data
    await update_data(user,guild)
    data[guild][user]["level"] += 1
    return data[guild][user]["level"]



async def level_up(user,channel):
    global data,roles,lvlUpMsg
    experience = data[channel.guild.id][user.id]["xp"]
    level = data[channel.guild.id][user.id]["level"]
    needxp = round((((level ** 2) + 50 + (level*10)) * 2.5))

    if needxp <= experience:
        try:
            lvlUpMsg = LevelUpMsg[str(channel.guild.id)]
            cls = await GenClass(user,channel)
            await channel.send(lvlUpMsg.format(cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls))
        except:
            try:
                await channel.send(":tada: Bravo {}, tu es passé niveau {} :tada: !".format(user.mention,level+1))
            except:
                pass
        finally:
            try:
                role = None
                max = 0
                while role == None:
                    await asyncio.sleep(0.2)
                    role = channel.guild.get_role(int(roles[str(channel.guild.id)][str(level+1)]))
                    max +=1
                    if max == 10:
                        raise Exception("erreur")
                await user.add_roles(role,reason="Level-up !")
            except:
                pass
            data[channel.guild.id][user.id]["xp"] = (int(data[channel.guild.id][user.id]["xp"]) - int(needxp))
            data[channel.guild.id][user.id]["level"] += 1

@frank.event
async def on_ready():
    await frank.change_presence(activity=discord.Streaming(name="de l'xp",type=discord.ActivityType.watching,url="https://www.twitch.tv/discord"),status=discord.Status.dnd)
    print("En ligne !")
    await save.start()


@frank.event
async def on_message(message):
    global data, mentions, roles
    try:
        levels = data[message.guild.id]
    except:
        data[message.guild.id] = {}
        levels = data[message.guild.id]
    if not message.author.bot and str(message.channel.type).lower() != "private":
        if message.content == "<@738341837395197952>" or message.content == "<@!738341837395197952>":
            try:
                username = message.author
                NVal = []
                for x in levels:
                    NVal.append([x,levels[x]["level"],levels[x]["xp"]])
                def CShort(e):
                    return int(e[1]*10000000000) + int(e[2])
                NVal.sort(key=CShort,reverse=True)
                pos = 0
                for x in NVal:
                    pos +=1
                    if x[0] == username.id:
                        break
                avatarUrl = username.avatar_url_as(format="png",static_format="png",size=1024)
                r = requests.get(avatarUrl, stream=True)
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, open('Avatar.png', 'wb'))
                level = levels[username.id]["level"]
                nextlvl = round((((level ** 2) + 50 + (level*10)) * 2.5))
                xp = levels[username.id]["xp"]
                color =  username.color.to_rgb()
                CardGen.card(username.name,color,int(xp),int(nextlvl),int(level),len(levels),pos,message.guild.id)
                await message.channel.send(file=discord.File('level.png'))
            except:
                await message.channel.send("Tu n'as pas encore gagné d'xp. Envoie quelques messages et réessaie plus tard !")
        elif message.content.lower() == "<@738341837395197952> top" or message.content.lower() == "<@!738341837395197952> top":
            try:
                NVal = []
                for x in levels:
                    NVal.append([x, levels[x]["level"], levels[x]["xp"]])
                def CShort(e):
                    return int(e[1] * 10000000000) + int(e[2])
                pos = 0
                for x in NVal:
                    pos +=1
                    if x[0] == message.author.id:
                        break
                if pos != 0:
                    await message.channel.send(allowed_mentions=mentions,content=f"Voici le top 5 du serveur:\n🥇 <@{NVal[0][0]}> : Niveau {NVal[0][1]},\n🥈 <@{NVal[1][0]}> : Niveau {NVal[1][1]},\n🥉 <@{NVal[2][0]}> : Niveau {NVal[2][1]},\n4e place: <@{NVal[3][0]}> : Niveau {NVal[3][1]},\n5e place: <@{NVal[4][0]}> : Niveau {NVal[4][1]}.\n\nTu es à la {pos}e place.")
                else:
                    await message.channel.send(allowed_mentions=mentions,content=f"Voici le top 5 du serveur:\n🥇 <@{NVal[0][0]}> : Niveau {NVal[0][1]},\n🥈 <@{NVal[1][0]}> : Niveau {NVal[1][1]},\n🥉 <@{NVal[2][0]}> : Niveau {NVal[2][1]},\n4e place: <@{NVal[3][0]}> : Niveau {NVal[3][1]},\n5e place: <@{NVal[4][0]}> : Niveau {NVal[4][1]}.")
            except:
                await message.channel.send("Il n'y a pas assez de membre pour faire un classement. réessayez plus tard !")
        elif (message.content == "<@!738341837395197952> resetAll" or message.content == "<@738341837395197952> resetAll") and message.author.guild_permissions.administrator:
            try:
                await reset(guild=message.guild.id)
                await message.channel.send("Les données ont bien été réinitialisées")
            except:
                await message.channel.send("Une erreure est survenue, désolé.")

        elif (message.content.startswith("<@!738341837395197952> del ") or message.content.startswith("<@738341837395197952> del ") ) and message.author.guild_permissions.administrator:
            try:
                await reset(guild = message.guild.id,user=message.content.replace(" del","").replace("<","").replace(">","").replace("@","").replace("!","").replace("738341837395197952",""))
                await message.channel.send("Les données de l'utilisateur bien été réinitialisées")
            except:
                await message.channel.send("Une erreure est survenue, désolé.")

        elif (message.content.startswith("<@!738341837395197952> addLevel") or message.content.startswith("<@738341837395197952> addLevel") ) and message.author.guild_permissions.administrator:
            try:
                x = await addLevel(guild = message.guild.id,user=int(message.content.replace(" addLevel","").replace("<","").replace(">","").replace("@","").replace("!","").replace("738341837395197952","")))
                await message.channel.send(f"L'utilisateur est désormais niveau {x}")
            except:
                await message.channel.send("Une erreure est survenue, désolé.")
        elif message.content.startswith("<@!738341837395197952> help") or message.content.startswith("<@738341837395197952> help"):
            help = discord.Embed(color=0xb42cfc)
            help.add_field(name="@FRank help",value="Affiche l'aide",inline=False)
            help.add_field(name="@FRank",value="Affiche vos statistiques",inline=False)
            help.add_field(name="@FRank [@mention/id]",value="Affiche les statistiques d'une autre persone",inline=False)
            help.add_field(name="@FRank top",value="Affiche les 5 personnes les plus hautes dans le classement du serveur",inline=False)
            help.add_field(name="@FRank resetAll*",value="Réinitalise **tous** les stats du serveur",inline=False)
            help.add_field(name="@FRank del [@mention/id]*",value="Réinitalise l'xp d'une personne",inline=False)
            help.add_field(name="@FRank addLevel [@mention/id]*",value="Ajoute 1 niveau à une personne.",inline=False)
            help.add_field(name="@FRank setMessage [message]*",value="Modifie le message de changement de niveau.",inline=False)
            help.add_field(name="@FRank addRole [niveau] [mention/id du role]*",value="Ajoute un role-level.",inline=False)
            help.add_field(name="@FRank delRole [niveau]*",value="Supprime un role-level.",inline=False)
            help.add_field(name="@FRank card*",value="Modifie la carte du serveur !\nPensez à bien avoir uplaod une image avec votre message",inline=False)
            help.add_field(name="Ajoutez FRank à votre serveur !",value="[en cliquant ici](https://discord.com/oauth2/authorize?client_id=738341837395197952&scope=bot&permissions=268749888)",inline=False)
            help.set_footer(text="* Nécésite la permission \"Administrateur\" sur le serveur",icon_url="https://cdn.discordapp.com/avatars/738341837395197952/e66f2b432f737429ab3e40c01a6ff7c9.png?size=256")
            await message.channel.send(embed=help)

        elif (message.content.startswith("<@!738341837395197952> setMessage") or message.content.startswith("<@738341837395197952> setMessage") ) and message.author.guild_permissions.administrator:
            content = re.sub(r'<@!?738341837395197952> setMessage', '', message.content)
            try:
                if len(content) >= 1000:
                    await message.channel.send("Désolé, votre message est trop long !\nVeuillez faire un message de moins de __1000__ caractères !")
                elif  content == "" or content.isspace():
                    raise Exception("Message trop court")
                else:
                    try:
                        cls = await GenClass(message.author,message.channel)
                        x = content.format(cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls,cls)
                        LevelUpMsg[str(message.guild.id)] = content
                        await message.channel.send("message défini avec succès ! Voici un apperçu du message :\n\n" + str(x))
                    except:
                        await message.channel.send("Votre message ne semble pas valide.\nVeuillez verifier que vos arguments se trouvent bien dans cette liste: https://github.com/v0ltis/FRank/blob/master/README.md")
            except:
                await message.channel.send("Votre message ne semble pas valide.\nVeuullez verifier que vos arguments se trouvent bien dans cette liste: https://github.com/v0ltis/FRank/blob/master/README.md")

        elif ( message.content.startswith("<@738341837395197952> addRole") or message.content.startswith("<@!738341837395197952> addRole") ) and message.author.guild_permissions.administrator:
            try:
                content = message.content.replace("738341837395197952","").replace("addRole","").replace(">","").replace("<","").replace("!","").replace("@","").replace("&","")
                level = int(re.sub(r'[0-9]{18}', '', content))
                id = int(content.replace(str(level),""))
                if level > 999:
                    await message.channel.send("Désolé, vous ne pouvez pas ajouter de roles au-delà du niveau 999.")
                else:
                    role=None
                    max = 0
                    while role == None:
                        role = message.guild.get_role(int(id))
                        max +=1
                        if max == 10:
                            0/0
                        await asyncio.sleep(0.2)
                    try:
                        if len(roles[str(message.guild.id)] <= 4):
                            roles[str(message.guild.id)][str(level)] = id
                        else:
                            try:
                                await message.channel.send("Désolé, vous ne pouvez ajouter que 5 roles par serveur, vous devez en supprimer avant d'en rajouter d'autres !")
                            except:
                                pass
                    except:
                        roles[str(message.guild.id)] = {}
                        roles[str(message.guild.id)][str(level)] = id
                        await message.channel.send("Le role a été ajouté avec succès !")
            except:
                await message.channel.send("Une erreur est survenue.\nVerifiez avoir donné un role valide, et bien avoir précisé un niveau, inferieur à 1000\nVoici la syntaxe: ``@FRank addRole niveau role(id/mention)``.")

        elif (message.content.startswith("<@738341837395197952> delRole") or message.content.startswith("<@!738341837395197952> delRole")) and message.author.guild_permissions.administrator:
            try:
                content = int(re.sub(r'<@!?738341837395197952> delRole', '', message.content))
                del roles[str(message.guild.id)][str(content)]
                await message.channel.send("Le role a été supprimé avec succès !")
            except:
                await message.channel.send("Une erreur est survenue")

        elif (message.content.startswith("<@738341837395197952> card") or message.content.startswith("<@!738341837395197952> card")) and message.author.guild_permissions.administrator:
            if message.attachments ==  []:
                await message.channel.send("Veuillez uploader une image avec votre message")
            elif message.attachments[0].size >=  500000:
                await message.channel.send("Votre image est trop lourde, elle doit faire moins de 500 Ko .")
            else:
                await message.attachments[0].save(f'img/{message.guild.id}.png')
                await message.channel.send("Votre image a été sauvegardée avec succès !")
        elif message.content.startswith("<@738341837395197952>") or message.content.startswith("<@!738341837395197952>"):
            try:
                user = int(message.content.replace("<","").replace("@","").replace(">","").replace("!","").replace("738341837395197952",""))
                username = None
                max = 0
                while username == None:
                    username = message.guild.get_member(user)
                    max +=1
                    if max == 10:
                        raise "erreur"
                    await asyncio.sleep(0.2)
                NVal = []
                for x in levels:
                    NVal.append([x, levels[x]["level"], levels[x]["xp"]])
                def CShort(e):
                    return int(e[1] * 10000000000) + int(e[2])
                NVal.sort(key=CShort, reverse=True)
                pos = 0
                for x in NVal:
                    pos +=1
                    if x[0] == user:
                        break
                avatarUrl = username.avatar_url_as(format="png",static_format="png",size=1024)
                r = requests.get(avatarUrl, stream=True)
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, open('Avatar.png', 'wb'))
                level = levels[user]["level"]
                nextlvl = round((((level ** 2) + 50 + (level*10)) * 2.5))
                xp = levels[user]["xp"]
                color =  username.color.to_rgb()
                CardGen.card(username.name,color,int(xp),int(nextlvl),int(level),len(levels),pos,message.guild.id)
                await message.channel.send(file=discord.File('level.png'))
            except:
                await message.channel.send("Désolé, je n'ai pas trouvé cet utilisateur")

        else:
            await update_data(message.author.id,message.guild.id)
            await level_up(message.author,message.channel)
            await add_experience(message.author,message.guild.id)





frank.run("TOKEN")
