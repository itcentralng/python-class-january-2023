# Customer pick cheap products, shop has a list of items each with its name, price and brand.
# The customer only has 50 naira to spent and is looking to buy up to 5 products.

stocks = [
    {"name": "Milk", "price": 20, "brand": "Peak"},
    {"name": "Bread", "price": 5, "brand": "Dangote"},
    {"name": "Eggs", "price": 20, "brand": "Golden Penny"},
    {"name": "Sugar", "price": 10, "brand": "Dangote"},
    {"name": "Salt", "price": 5, "brand": "Dangote"},
    {"name": "Rice", "price": 3, "brand": "Royal Stallion"},
    {"name": "Beans", "price": 80, "brand": "Golden Penny"},
]

# sort the list of items by price
stocks.sort(key=lambda x: x.get("price"))

for i in stocks:
    spent_limit = 50
    if i.get("price") <= 50:
        spent_limit -= i.get("price")
        print(i)
        print(spent_limit)
        # if spent_limit < 0:
        #     print(i)
        # else:
        #     print("Sorry, you cannot afford any of the products")
