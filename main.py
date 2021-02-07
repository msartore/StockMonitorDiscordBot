from discord.ext import commands
from replit import db
import os
import cryptocompare
import asyncio

client = commands.Bot(command_prefix=".")

def updateStatus(stockN, statusUpdate):
  if stockN in db.keys():
    if statusUpdate == 'stop':
      db[stockN]='stop'
      return True
    elif statusUpdate == 'del':
      del db[stockN]
      return True
    else:
      return False

def addToDB(stockN):
  db[stockN] = 'run'
  return True

def checkStatus(stockN):
  if stockN in db.keys():
    if db[stockN] == 'stop':
      return True
    else:
      return False


async def thS(arg, ctx, timer):  
  while True:
    price = cryptocompare.get_price(arg)[arg]['EUR']
    if arg == 'BTC':
      if price > float(25734.34):
        await ctx.send("Update "+arg+" value in euro: "+str(price))
      else:
        await ctx.send("@everyone Buy "+arg+"!, value in euro: "+str(price))
    else:
      await ctx.send("Update "+arg+" value in euro: "+str(price))
    await asyncio.sleep(int(timer))
    if checkStatus(arg):
      if updateStatus(arg, 'del'):
        await ctx.send(arg+" Stopped!")
      break

@client.event
async def on_ready():
    print("Bot started!")

@client.command()
async def stopUS(ctx, stockN):
  if updateStatus(stockN, 'stop'):
    await ctx.send("Stopping "+stockN+" updates..")    
  else: 
    await ctx.send("Error, "+stockN+" is not running!")
    
@client.command()
async def runningStocks(ctx):
  tmp = ""
  for items in db.keys():
    tmp += " " + items
  if tmp!="":
    await ctx.send("Running stocks: "+tmp)
  else:
    await ctx.send("no running stocks!")

@client.command()
async def updateStock(ctx, arg, timer):
  if addToDB(arg):
    asyncio.get_event_loop().create_task(thS(arg, ctx, timer))
  else:
    await ctx.send("Error, something went wrong!")

@client.command()
async def credits(ctx):
  await ctx.send("Bot made by Massimiliano Sartore")
 
db.clear()
client.run(os.getenv('TOKEN'))