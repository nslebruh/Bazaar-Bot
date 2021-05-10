import discord, json
from discord.ext import commands
from discord.ext.commands import command, Cog, errors, cooldown

class Maths(Cog):
	def __init__(self, bot):
		self.bot = bot
		with open("operations.json") as ops:
			self.ops = json.load(ops)
	
	@command()
	async def math(self, ctx, operation:str, *, numbers):
		if operation.lower() not in self.ops:
			await ctx.send(f"{operation} is not an accepted operation")
		numbers = numbers.split()
		for i in numbers:
			try:
				i *= 1
			except:
				await ctx.send(f"{i} is not a number")
				return
		
		pass
	@command(aliases=["exec"])
	async def execute(self, ctx, *, executable):
		try:
			print(executable)
			eval(executable)
		except Exception:
			await ctx.send(Exception)
			print(Exception)
		return
def setup(bot):
	bot.add_cog(Maths(bot))