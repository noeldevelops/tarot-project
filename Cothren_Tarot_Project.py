#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# CothrenFinalProject
# Programmer: Amber Noel Cothren
# Email: acothren1@cnm.edu
# Purpose: user enters personal info then receives a fortune generated using tarot card data


# In[ ]:


from datetime import datetime
import json
import time
import random


# In[ ]:


# Function Definitions


# In[ ]:


def gatherInfo():
    """Greet the user and take user input for name, birthday.
    Return array with [name (string), birthday (datetime)]."""
    print('\nWelcome weary traveller! Please, tell me about yourself...')
    
    # ask for name
    userName = input('What shall I call you?  ')
   
    validDate = False
    while not validDate:
        # ask for birthdate and catch invalid entries
        try:
            dateEntry = input('Please enter your birthday as mm-dd-yyyy\n')   
            userBirthday = datetime.strptime(dateEntry, "%m-%d-%Y")
            validDate = True
        except Exception as e:
            print("I don't think that's a real date - ", e)
            print("\nPlease try again")
    return [userName, userBirthday]


# In[ ]:


def processData():
    """Open tarot file and return data as dict."""
    try:
        data = open('tarot-interpretations.json')
    except FileNotFoundError as e:
        print('Sorry, I lost the tarot cards! Try again later.')
        return
    else:
        tarotDict = json.load(data)
        return tarotDict


# In[ ]:


def getRandomCard():
    """Return random card from data, type = dict."""
    cardsList = tarotDict['tarot_interpretations']
    # get a random card from deck
    card = random.choice(cardsList)
    return card


# In[ ]:


def formattedFortuneString(card, meanings):
    """Format card name, fortune, meanings and return a reusable printable string."""
    cardString = '{name}.'.format_map(card).upper()
    fortuneString = '\nIn the future...\n' + random.choice(card['fortune_telling']).lower() + '.'
    lightString = 'You must continue ' + meanings[0].lower() + ','
    shadowString = 'And avoid ' + meanings[1].lower() + '.'
    
    # gather the strings in array with stars and return as one string
    strings = ['\n', starString(61), starString(59), starString(61), cardString, fortuneString, lightString, shadowString, starString(58), starString(61), starString(58), '\n']
    fortune = '\n'.join(strings)
    return str(fortune)


# In[ ]:


def lightAndShadowMeanings(card):
    """Return a random light and shadow meaning from the card"""
    # first choose a random number for each (there are multiple options for each in data)
    lightNum = random.randint(0,len(card['meanings']['light'])-1)
    darkNum = random.randint(0,len(card['meanings']['shadow'])-1)
    # then use those numbers to get the meanings
    lightMeaning = card['meanings']['light'][lightNum]
    shadowMeaning = card['meanings']['shadow'][darkNum]
    return [lightMeaning, shadowMeaning]


# In[ ]:


def saveFortuneFile(info, fortune):
    """Write user's info and fortune to a new text file."""
    try:
        with open('fortune.txt', 'w') as f:
            f.write('A fortune for ')
            f.write(info[0].title())
            f.write(', born on ')
            f.write(datetime.strftime(info[1], "%b %d, %Y"))
            f.write(fortune)
            f.write(str(tarotDict.get('description')))
    except Exception as e:
        print('Sorry, we could not save your fortune to a file because ', e)
    else:
        print('\nYour fortune was saved as fortune.txt')
    finally:
        f.close()


# In[ ]:


def starString(length):
    """Return an array of random "star" characters with the given length."""
    stars = []
    options = [' ', ' ', ' ', ' ', ' ', ' ', ' ',  '.', '\u22C6', '\u22C6', '\u2726', '\u00B7', '\u2821', '\u280C']
    while length > 0:
        length -= 1
        stars.append(random.choice(options))
    return ''.join(stars)


# In[ ]:


# Open a while loop to run program
goAgain = 'y'
while goAgain == 'y':

    userInfo = gatherInfo()
    
    print('\nPlease wait while I shuffle the tarot deck and draw you a card...\n')
    time.sleep(2)
    tarotDict = processData()
    userCard = getRandomCard()
    meanings = lightAndShadowMeanings(userCard)
    fortune = formattedFortuneString(userCard, meanings)
    print(fortune)
    
    # ask whether the user wants to save it to a file
    save = input('\nDo you want to save your fortune to a file? y/n -> ')
    if save == 'y':
        saveFortuneFile(userInfo, fortune)

    # ask whether to run program again or close
    goAgain = input('\nDo you want to try again? y/n -> ')


# In[ ]:


# Close out and say goodbye
print(starString(51))
print('Thank you for stopping by.')
print(starString(51))
# print the data description for user's info and to credit author
print('\n\n', tarotDict.get('description'))

