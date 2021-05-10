import requests
def fetch(url):
		return (lambda u: requests.get(url).json())(url)
bazaardata = fetch("https://api.hypixel.net/skyblock/bazaar?key=2e584d3f-a88d-4d9f-bcf2-01344600de36")
jsoon = open("product.json", "w")
products = []
for i in bazaardata["products"]:
	if i in jsoon["products"]:
		products.append(i)
		print(i)
print(products)
jsoon.write("{")
jsoon.write(f"\t\"products\" : {products}")
jsoon.write("}")
jsoon.close()