
# Q1: Using comments, list all the data types you know with examples

# String
name = "Jamilu Salisu"

# Integer
age = 24

# Float
sallary = 99.99

# Boolean
isHealthy = True

# List
skills_learning = ["Python", "Flask", "Dart", "Flutter", "Clound Computing"]

# Dictionary
intern_profile = {"name": "Jamilu Salisu",
                  "institution": "BUK", "department": "SWE", "level": 300, "duration": "6 months"}

# Tuple
skills = ("PHP", "Javascript", "HTML", "CSS", "Angurlar", "Flutter")

# Set
hobbies = {"Coding", "Watching Anime", "Reading Comics", "Networking"}


# Q2: Read about variable naming convention in python and create examples of each

# (i) variable name must start with a letter or the underscore character
firstname = "Jamilu"
_othername = "Mohammed"

# (ii) variable name cannot start with a number
# 2lastname = "Salisu" # an error will occur

# (iii) variable name can only contain alpha-numeric characters and underscores(A-z, 0-9, and _)
full_name1 = "Jamilu Salisu"

# (iv) variable names are case-sensitive
height = 1.50
Height = 1.60
HEIGHT = 1.75


# Q3: List 5 String methods with an example using print() in each case to print your result

# split the string into a list
print(name.split())

# convert the string to uppercase
print(firstname.upper())

# replace a word in the string
print(name.replace("Jamilu", "Mohammed"))

# format the string
print("I am {} years old and I earn {}$ per month.".format(
    age, sallary))

# count the number of times a word appears in the list
print("I am learning Flutter and Python.".count("am"))
