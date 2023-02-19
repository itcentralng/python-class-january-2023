# ASSIGMENT
"""
Convert the state and capital game into a class blueprint for those kind of games. Make it work well with 
a dictionary or state and capital game.
"""
# class Nigeria:
#     def __init__ (self, state, capital):    
#         self.state = state
#         self.capital = capital
# create a dictionary, key is the state and value is the capital

import random

capital_dic=[
    {"sate":"Abia", "capital":"Umuahia"},
    {"sate":"Adamawa", "capital":"Yola"},
    {"sate":"Akwa Ibom", "capital":"Uyo"},
    {"sate":"Anambra", "capital":"Awka"},
    {"sate":"Bauchi", "capital":"Bauchi"},
    {"sate":"Bayelsa", "capital":"Yenagoa"},
]
    

States=list(capital_dic.keys())
print ('Let\'s learn Nigerian States and Capitals. 10 rounds. Enter exit to quit the game.')
point=0 # this is the score
for i in range(10):
    state=random.choice(States) # randomly select 10 states, how do I avoid duplicate?
    capital = capital_dic[state]
    user_guess = input('what is the capital of %s?'%state )
    if user_guess.lower() == 'exit':  #if a user type in exit, the game exits
        break
    elif user_guess.title() == capital:
        point+=1
        print('Correct! Your score is %d' %point)
    else:
        print('Incorrect. The capital of {} is {}.'.format(state,capital))
print('We are done. Your final score is %d, thank you.' %point)