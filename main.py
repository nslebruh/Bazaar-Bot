import os, discord
from keep_alive import keep_alive
from discord.ext import commands

bot = commands.Bot(
	command_prefix=".",  
	case_insensitive=True  
)

bot.author_id = 305589763866624001  

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name="Deez Nuts™", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
	print(f"Logged in as {bot.user}")


extensions = [
	'cogs.dev_commands',
    "cogs.admin_commands",
	"cogs.events",
	"cogs.bazaar",
	"cogs.mod_commands"

	]

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)  
		print(f"{extension}.py loaded")

keep_alive()  
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  