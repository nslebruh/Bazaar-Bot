import discord
from discord.ext import commands
class AdminCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def cog_check(self, ctx):
		return ctx.author.id == self.bot.user.id

def setup(bot):
	bot.add_cog(AdminCommands(bot))


