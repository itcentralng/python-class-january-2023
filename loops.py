# # ForLoop

# numbers = [1, 2, 3]

# # for "a variable" in "what your are iterating over":
#     # what happens every time it loops

# for number in numbers:
#     if number % 2 != 0:
#         print(number)

# for alphabet in "ZAINAB":
#     if alphabet in 'AIOEU':
#         print(alphabet)

# for name in ("Jamil", "Halima", "Late Commer"):
#     if 'Late' not in name:
#         print(name)

# person = {'name':'James Aurthur', 'age':25}

# for item in person:
#     print(person.get(item))

# Class Exercise

# Write a program that helps a customer pick cheap products
# from a certain shop. The shop has a list of items each
# with its name, price and brand. The customer only has
# 50 naira to spend and is looking to buy up to 5 products.

shop = [
    {"name": "Butter", "price": 200, "brand": "Blueband"},
    {"name": "Cake", "price": 10, "brand": "Rahma Stores"},
    {"name": "Bread", "price": 5, "brand": "Rahma Stores"},
    {"name": "Banana", "price": 10, "brand": "Rahma Stores"},
    {"name": "Pepsi", "price": 150, "brand": "Pepsi"},
    {"name": "Coke", "price": 5, "brand": "Coca Cola"},
    {"name": "Pure Water", "price": 20, "brand": "Coca Cola"},
    {"name": "Ice Cream", "price": 200, "brand": "Kanti Plus"},
]

money = 50

purchased = []

for item in shop:
    if item.get('price') <= money:
        purchased.append(item.get('name'))
        money -= item.get('price')
items = "\n".join(purchased)
thanks = "Thank you for shopping with us\n"
reciept = thanks+"Here are your items:\n"+items
print(reciept)

# Write a shopping game where a player will start by
# setting how much they want to spend in our shop with
# maximum spend limit of 5000 naira.
# Players will then be presented with a list of items one
# by one for them to choose from.
# They must not buy more than 5 items.
# If a player spends all their money buy the end of the game
# they win, otherwise they can choose to play again or
# its game over.
