import random
# Function is a reusable block of code

"""
Write a state a capital game users are prompted with a name of a
state for which to provide the capital.

The game runs on an endless loop untill all the states have been
used or the user chooses to 'quit'.

The whole game should start when a function is called. For example
stateAndCapital() ==> game
"""

Nigeria = [ 
    {"sate":"Abia", "capital":"Umuahia"},
    {"sate":"Adamawa", "capital":"Yola"},
    {"sate":"Akwa Ibom", "capital":"Uyo"},
    {"sate":"Anambra", "capital":"Awka"},
    {"sate":"Bauchi", "capital":"Bauchi"},
    {"sate":"Bayelsa", "capital":"Yenagoa"},
]
state = []
    state = random.choice(states)
        if state not in states:
            states.append(state)
        response = input("What is the capital of {}? ".format(state.get('name')))
        if response == 'end':
    else:
        if state.get('capital') == response:
            print("That's correct.")
        else:
            print("Wrong, the capital of {} is {}".format(state.get('name')))

    used_states = []
    while playing:
        state = random.choice(states)
        if state not in used_states:
            used_states.append(state)
        response = input("What is the capital of {}? ".format(state.get('name'), state.get('capital')))
    if len(state) == len(states):
        playing = False


        # if response == 'quit':
        #     playing = False
        # else:
        #     if state.get('capital') == response:
        #         print("That's correct!")
        #     else:
        #         print("Oops! wrong, the capital of {} is {}".format(state.get('name'), state.get('capital')))
        # if len(used_states) == len(states):
        #     playing = False 


# for state in Nigeria:
#     # state = random.choice(Nigeria)
#     print(state)
# for capital in Nigeria:
#     capital = random.choice(Nigeria)
#     response = input("state: {} capital: {} What is your state? ".format(state.get('state'),
#     capital.get('capital')))
        # if response == 'capital':
#     else:
# print('welcome to our capital ', capital)


# state = input('what is your state ')
# capital = input('what is your capital ')
# else:
#     print('wrong state')
#     else:
#         print('wrong capital')



shopping = ("sausage", "indomie", "milk")
print(shopping[0])
print(shopping[1])
print(shopping[2])