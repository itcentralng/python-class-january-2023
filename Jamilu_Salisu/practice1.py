# users to register

full_name = input("What is your full name? ")
email = input("What is your email? ")
password = input("Choose a 5 character password: ")

# saved users details
if len(password) < 5:
    print("Password should be at least 5 characters")
else:
    print("Registration successful")

users = {"full_name": full_name, "email": email, "password": password}

# users login
login_email = input("Enter your email: ")
login_password = input("Enter your password: ")

if login_email == users["email"] and login_password == users["password"]:
    print("Login successful")
else:
    print("Login failed")
