import math

'''
Final Summary:
Theres a bit more that could be done, for instance implementing the cargo capacity feature to trade, but you can travel to different towns and you can buy and sell 2 commodities and it just works so thats fine with me.
On the whole I especially like the exponetial increase in unit price.
Learnt:
-define methods first ESPECIALLY if they can be reused, use them later as called functions.
-arrays are your friend, whenever possible design for use with a whole array rather than designing functions for each individual entry
	-rather than create dozens of seperate values arrange them as one array, and then call them later. This reduces the number of variables you have to keep in mind. (where appropriate, ie same object)
-to keep the program active, trap it in a while loop.

I like the idea of creating a combat version based on this: basically the plane is split into body parts and pirates shoot in from the sides.
'''




#Values - Towns
#Format: townN = ['Name', Population, 'description', food surplus, goods surplus, position x, position y]
town1 = ['Los Mantos', 1000,'A small fishing village on the eastern coast, a small slum rife with crime', 400, -200, -2,0]
town2 = ['Kallac', 5400, 'the economic center of the region, the city is filled with those who look for a better life, many have failed', -800, 1500,1,1]
town3 = ['Vinas', 400, 'governmental center of the region, refuge of the rich and powerful', -300, -600,+2,-2]

towns = [ town1 , town2 , town3 ] #just realised, current_town variable won't copy onto the original vector.
town_names = [town1[0], town2[0], town3[0]]
current_town = town1 #though actually maybe its fine just for reading, should replace eventually with just town_number
town_number = 0 #you set it to 1 travel options don't match up.
distances = [ [0,4,6] , [4,0,4], [6,4,0] ]

#Values - commodities
'''
price_base = [100,200] #!!!THE BASE PRICE IS CHANGEING?? This is literrally the only line assigning a value to price_base, what the hell is going on.
price = price_base 
'''
price_min = [30,60]
price_max = [400, 500]

#NEW DISCRETE SIZE SYSTEM
goods = [ [12,4] , [40,70] , [2,2] ]
goods_baseline = [ [ 8 , 8] , [ 50,50 ] , [7 , 7] ]
base_prices = [100,200]


#Values Personal
wallet = 5000
cargo_space = int(100)
cargo = [int(10),int(0),int(0)] #total_remaining, food, goods ,...
price = [0,0]

#Action - price calculator
def prices(t):
	for i in range(len(goods[town_number])):
		translation_value = ( ((goods[town_number][i] - t) / goods_baseline[town_number][i]) - 1 )
		if translation_value > 1:
			translation_value = 1
		multiplier = 1 / math.exp(translation_value)
		price[i] = round( base_prices[i] * multiplier, 1)
		#price[i] = round( (2 - ( goods[town_number][i] / ( towns[town_number][1] / 100 ) ) ) * base_prices[i] , 1) #as quantity goes up, prices drop, BUT! they can go negative, so you need to draw out how you want the system to act:    okay bro design it with e^-x on the left and then e^x on the right and cut off max and mins at a value of -1 and 1 within that domain, then define a baseline quantity of goods and then figure out some way to translate, also reverse the function so ie use g(x) where g(x) = -f(x) as f(x) is decreasing at the left when you want it to increase, no . No youre a fucking moron, just use e^-x from -1 to 1 jeez
'''
def local_price(): # ARCHAIC
	price_mod_food = round( ( price_base[0] * (1 - current_town[3]/current_town[1] ) ), 0) # should be an array, with a food loop for each good.
	price_mod_goods = round( ( price_base[1] * (1 - current_town[4]/current_town[1] ) ), 0)
	if price_mod_food > price_min[0]:
		price[0] = price_mod_food
	else:
		price[0] = price_min[0]
	if price_mod_goods > price_min[1]:
		price[1] = price_mod_goods
	else:
		price[1] = price_min[1]
#local_price()
'''

def total_price(k , i):
	total_price = 0
	if k < 0:
		k = -k
		for j in range(k):
			prices(j)
			total_price = total_price - price[i] #for some reason, you buy and sell back you run out of money, which is perfect you just don't have control over it.
	else:
		for j in range(k):
			prices(j)
			total_price = total_price + price[i]
	return total_price

#Gameplay loop
print('There are the following options available: "description" , "trade" , "travel" ,when finished just type "exit game" ')
while True:
	action = input('... ')
	sensible = 0
	if action == 'description':
		print(' Town: ' , current_town[0], ' \n Population: ', current_town[1])	
		print(' \n\'' ,current_town[2], '\'')
		sensible = 1
	if action == 'trade': # uses archaic system
		#local_price()
		prices(0)
		print('Food: ' , price[0] , 'per Crate')
		print('Goods: ' , price[1] , 'per Crate')
		print('Wallet: ' , wallet)
		action1 = input('What would you like to trade... ')
		if action1 == 'food':
			i = 0
			print('1 unit for ' ,  price[i])
			print('5 units for ' , total_price(5, i))
			buy = int(input('How much would you like to trade (negative for sell): '))
			goods[town_number][i] = goods[town_number][i] - buy
			wallet = wallet - total_price(buy,i)
		if action1 == 'goods':
			i = 1
			print('1 unit for ' ,  price[i])
			print('5 units for ' , total_price(5, i))
			buy = int(input('How much would you like to trade (negative for sell): '))
			goods[town_number][i] = goods[town_number][i] - buy
			wallet = wallet - total_price(buy,i)
		sensible = 1
		'''
		transaction_cost = 0 #housekeeping incase the user leave trade interface, better solution would be secondary if loop
		if action1 == 'buy food':
			print('How many?')
			quantity = int(input('...'))
			if cargo[0] - quantity < 0: 
				quantity = cargo[0]
			transaction_cost = quantity * price[0]
			if transaction_cost > wallet:
				quantity = int(wallet / price[0])
				transaction_cost = quantity * price
			print( quantity, 'food crates bought \n for ' , transaction_cost , ' Zredits')
		wallet = wallet - transaction_cost
		print('current balance: ', wallet)
		print(price_base[0])
		'''
	if action == 'travel':
		current_location = town_names[town_number]
		print('Current Location: ', current_location)
		print('Destinations: ')	
		for i in range(len(town_names)):
			if i != town_number:
				print('	' , town_names[i], distances[town_number][i] * 100, 'Kilometers')
		#distances.insert(town_number,0)
		destination = input('Where to?: ')
		if destination == 'Los Mantos':
			current_town = town1
			town_number = 0
		if destination == 'Kallac': #the clever thing would be to put a autodector on the string and assign it to the town_number
			current_town = town2
			town_number = 1
		if destination == 'Vinas':
			current_town = town3
			town_number = 2
		sensible = 1
	if action == 'exit game':
		break
	else:	
		if sensible == 0:
			print('What?')





