import discord
from discord.ext import commands
from discord.ext.commands import command, Cog, errors, cooldown

class DeveloperCommands(Cog):
	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		return self.bot == ctx.author

	@command(aliases=["rl"])
	@commands.has_any_role("Admin", "Mod", "Owner", "Developer")
	async def reload(self, ctx, cog):
		extensions = self.bot.extensions
		if cog.lower() == "all":
				for extension in extensions:
					self.bot.unload_extension(cog)
					self.bot.load_extension(cog)
					await ctx.send(f"{cog}.py reloaded")
		if cog in extensions:
			self.bot.unload_extension(cog)  
			self.bot.load_extension(cog)  
			await ctx.send(f"{cog}.py reloaded")  
		else:
			await ctx.send('Unknown Cog')
	
	@command(aliases=["ul"])
	async def unload(self, ctx, cog):
		extensions = self.bot.extensions
		if cog not in extensions:
			await ctx.send("Cog is not loaded!")
			return
		self.bot.unload_extension(cog)
		await ctx.send(f"{cog}.py has successfully been unloaded.")

	@command()
	async def load(self, ctx, cog):
		try:
			self.bot.load_extension(cog)
			await ctx.send(f"{cog} has successfully been loaded.")
		except errors.ExtensionNotFound:
			await ctx.send(f"{cog} does not exist!")
		pass

	@command(aliases=["lc"])
	async def listcogs(self, ctx):
		base_string = "```css\n"
		base_string += "\n".join([str(cog) for cog in self.bot.extensions])
		base_string += "\n```"
		await ctx.send(base_string)

def setup(bot):
	bot.add_cog(DeveloperCommands(bot))