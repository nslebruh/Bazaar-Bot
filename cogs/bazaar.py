import discord, urllib.request, json, requests
from discord.ext import commands
from discord.ext.commands import command, errors, cooldown, Cog
from discord.ext.tasks import loop

class Bazaar(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.apikey = "2e584d3f-a88d-4d9f-bcf2-01344600de36"
		with open("product.json") as products:
			products = json.load(products)
		self.products = products["products"]
		npc = open("NpcProducts.json")
		npc = json.load(npc)
		self.npc = npc["NpcPrices"]
		self.craft = npc["NpcCraftMultiply"]

	


	@command(aliases=["bii"])
	async def price(self, ctx, *, item : str):
		def fetch(url):
			return (lambda u: requests.get(url).json())(url)
		item = item.upper().replace(" ", "_")
		if item in self.products:
			bazaardata = fetch("https://api.hypixel.net/skyblock/bazaar?key=" + self.apikey)
			buy_price =  bazaardata["products"][item]["sell_summary"][0]["pricePerUnit"]
			sell_price = bazaardata["products"][item]["buy_summary"][0]["pricePerUnit"]
			sell_to_order_week = bazaardata["products"][item]["quick_status"]["sellMovingWeek"]
			bought_from_order_week = bazaardata["products"][item]["quick_status"]["buyMovingWeek"]
			buy_orders = bazaardata["products"][item]["quick_status"]["buyOrders"]
			sell_orders = bazaardata["products"][item]["quick_status"]["sellOrders"]
			item = item.replace(" ", "_").title()
			embed = discord.Embed(title=item, description = f"Buy order price: {buy_price}\nSell order price: {sell_price}\nBuy orders: {buy_orders}\nSell orders: {sell_orders}\nItems bought per hour: {round(bought_from_order_week / 168)}\nItems sold per hour: {round(sell_to_order_week / 168)}")
			await ctx.send(embed=embed)
		else:
			item = item.replace(" ", "_").title()
			await ctx.send(f"{item} is not an item in the bazaar")
		return
	
	@command()
	async def bnpc(self, ctx, sort = "profit"):
		def fetch(url):
			return (lambda u: requests.get(url).json())(url)

		bazaardata = fetch("https://api.hypixel.net/skyblock/bazaar?key=" + self.apikey)

		itemlist = []

		for i in self.products:
			if i in self.npc.keys():

				price = self.npc[i]
				price = float(price)

				buy = bazaardata["products"][i]["sell_summary"][0]["pricePerUnit"]
				sell_volume = bazaardata["products"][i]["quick_status"]["sellMovingWeek"]

				buy = buy + 0.1

				if buy < price:
					i = i.replace("_", " ").title()
					
					sold_per_minute = round(sell_volume / 10080, 0)
					profit_per_item = round(price-buy, 1)
					cpm = round(sold_per_minute * profit_per_item, 1)
					sold_per_minute = str(sold_per_minute)
					sold_per_minute = sold_per_minute.replace(".0", "")
					itemlist.append([i, price, buy, profit_per_item, cpm, sold_per_minute])

		if sort.lower() == "profit":
			itemlist.sort(key=lambda x: x[3], reverse=True)

		elif sort.lower() == "speed":
			itemlist.sort(key=lambda x: x[5], reverse = True)

		elif sort.lower() == "cpm":
			itemlist.sort(key=lambda x: x[4], reverse=True)

		else:
			await ctx.send(f"{sort} is not a recognised sort for this command\nThe default sort has been applied")

		embed = discord.Embed(title="Items")

		for i in itemlist:
			embed.add_field(name=i[0], value=f"Buy: {i[2]}, Sell: {i[1]}, Profit: {i[3]}\nItems sold per minute: {i[5]}\nCoins per minute: {i[4]}")

		await ctx.send(embed=embed)
		return

	@command(aliases=["cprofit", "craftp", "cp"])
	async def craftprofit(self, ctx):
		def fetch(url):
			return (lambda u: requests.get(url).json())(url)

		bazaardata = fetch("https://api.hypixel.net/skyblock/bazaar?key=" + self.apikey)
		itemlist = []

		for i in self.craft:
			buy = bazaardata["products"][i[0]]["sell_summary"][0]["pricePerUnit"]
			sell = bazaardata["products"][i[1]]["buy_summary"][0]["pricePerUnit"]
			sell_volume  = bazaardata["products"][i[0]]["quick_status"]["sellMovingWeek"]
			buy_volume = bazaardata["products"][i[1]]["quick_status"]["buyMovingWeek"]
			sold_per_minute = round(sell_volume / 10080, 0)
			bought_per_minute = round(buy_volume / 10080, 0)
			if bought_per_minute > 1:
				bought_per_minute = round(buy_volume / 168, 0)

			if buy * i[2] < sell:
				name1 = i[0].replace("_", " ").title()
				name2 = i[1].replace("_", " ").title()
				profit = round(sell - (buy*i[2]), 1)
				itemlist.append([name1, buy, name2, sell, i[2], profit])
		itemlist.sort(key=lambda x: x[5], reverse=True)
		embed = discord.Embed(title="Bazaar Crafting Profits")
		for i in itemlist:
			embed = discord.Embed(title="Bazaar Crafting Profits")
			embed.add_field(name=f"{i[0]} into {i[2]}", value=f"buy: {i[1]}\nSell: {i[3]}\nCraft amount: {i[4]}\nProfit: {i[5]}")

			print(f"{i[0]} into {i[2]}\nbuy: {i[1]}\nSell: {i[3]}\nProfit: {i[5]}\nCraft amount: {i[4]}\n\n")
			await ctx.send(embed=embed) 
		return
	
	@command(aliases=["orders", "op"])
	async def orderprint(self, ctx, order_type, *, item):
		def isstr(variable):
			try:
				variable = str(variable)
				return variable, True
			except:
				return False
		if isstr(order_type):
			if order_type.lower() == "buy" or "sell":
				if isstr(item):
					if item.replace(" ", "_").upper() in self.products:
						item = item.replace(" ", "_").upper()
						def fetch(url):
							return (lambda u: requests.get(url).json())(url)
						bazaardata = fetch("https://api.hypixel.net/skyblock/bazaar?key=" + self.apikey)
						if order_type == "buy":
							order_type = "sell"
						elif order_type == "sell":
							order_type = "buy"
						summary = bazaardata["products"][item][order_type+"_summary"]
						embed = discord.Embed()
						for i in summary:
							ppi = i["pricePerUnit"]
							amount = i["amount"]
							orders = i["orders"]
							item = item.replace("_", " ").title()
							embed.add_field(name=item, value=f"Price:{ppi}\nAmount: {amount}\nOrders: {orders}")
						await ctx.send(embed=embed)
						return
					else:
						await ctx.send(f"{item} is not an item in the bazaar")
				else:
					await ctx.send(f"{item} is not a string")
			else:
				await ctx.send(f"{order_type} is not an accepted order type")
				return
		else:
			await ctx.send(f"{order_type} is not a string type")
			return

		return

def setup(bot):
	bot.add_cog(Bazaar(bot))