# # halima_is_arround = True

# # if halima_is_arround:
# #     print("Everyone gets 10K")

# print("welcome our awesome social media")

# name = input("What is your name? ")
# email = input("What is your email? ")
# password = input("Choose a 5 character password: ")

# if len(password) < 5:
#     password = input("Password must be at least 5 characters: ")

# database = {"name":name, "email":email, "password":password}

# email = input("Enter email: ")
# password = input("Enter password: ")

# if email == database.get("email"):
#     if password == database.get('password'):
#         print("Welcome {}".format(database.get("name")))


numbers = [1,2,3]

if 5 not in numbers:
    print("5 not found, adding...")
    numbers.append(5)
    print(numbers)

if 5 in numbers:
    print("5 Found, removing....")
    numbers.remove(5)
    print(numbers)

if len(numbers) >= 3:
    print(numbers[0])
