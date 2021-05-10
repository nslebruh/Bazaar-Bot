import discord
from discord.ext import commands
from datetime import datetime as dt

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return ctx.author.id == self.bot.user_id
	

	@commands.Cog.listener()
	async def on_message(self, message):
		if self.bot.user == message.author:
			return
		minute = dt.now().minute
		hour = dt.now().hour
		day = dt.now().day
		month = dt.now().month
		year = dt.now().year
		t = f"{minute}:{hour}/{day}/{month}/{year}"
		file = open("messages", "a")
		file.write(f"{message.author} - {message.content} - {t}\n")
		file.close()

	@commands.Cog.listener()
	async def on_member_join(self, ctx):
		role = discord.utils.get(ctx.guild.roles, name = "Member")
		ctx.user.add_roles(role)

def setup(bot):
	bot.add_cog(Events(bot))