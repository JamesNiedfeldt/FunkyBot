#==== Description ====
"""
Contains all necessary functions for searching up Magic: the Gathering cards
"""

#==== Imports ====
import requests
from funktions import helpers as h

#==== Fetch a card from Scryfall ====
def fetchCard(query,headers):
    name = "https://api.scryfall.com/cards/named"
    search = "https://api.scryfall.com/cards/search"
    random = "https://api.scryfall.com/cards/random"
    
    try:
        #Random card requested
        if query.upper().startswith("RANDOM"):
            response = requests.get(url = random, params = {'q':__parseRandom(query)}, headers = headers)
            results = response.json()

        else:
            #Find by name first
            response = requests.get(url = name, params = {'fuzzy':query}, headers = headers)
            results = response.json()

            if results['object'] == "error":
                #Try a search if not found by name
                response = requests.get(url = search, params = {'q':query}, headers = headers)
                results = response.json()

        #If found multiple cards, take the first
        if results['object'] == "list":
            return __formatCard(results['data'][0])

        #Single card found
        elif results['object'] == "card":
            return __formatCard(results)

        #Nothing found
        else:
            return [None, "Sorry, I couldn't find \"{}\"!".format(query)]

    except KeyError as e:
        return [None, "Something went wrong!"]

def __formatCard(card, givenUri=None):
    name = card['name']
    cost = ""
    textBox = ""
    imageUri = ""
    toReturn = []

    if givenUri == None:
        uri = card['scryfall_uri']
    else:
        uri = givenUri
    
    if 'card_faces' in card:
        if card['layout'] == "transform" or card['layout'] == "modal_dfc":
            cost = card['card_faces'][0]['mana_cost']
            for f in card['card_faces']:
                toReturn.append(__formatCard(f, givenUri=uri))
        else:
            textBox = card['type_line']
            for f in card['card_faces']:
                textBox = (textBox + "\n\n" + 
                           "**" + f['name'] + "  " + f['mana_cost'] + "**" +
                           "\n" + __makeTextBox(f))
            cost = card['mana_cost']
            imageUri = card['image_uris']['normal']
            toReturn = [uri, name + "  " + cost, textBox, imageUri]

    else:
        textBox = __makeTextBox(card)
        cost = card['mana_cost']
        imageUri = card['image_uris']['normal']
        toReturn = [uri, name + "  " + cost, textBox, imageUri]
        
    return toReturn

def __makeTextBox(card):
    textBox = card['type_line'] + "\n\n" + card['oracle_text']
    if 'power' in card and 'toughness' in card:
        if card['power'] == '*' and card['toughness'] == '*':
            textBox = textBox + '\n\\' + card['power'] + '/\\' + card['toughness']
        else:      
            textBox = textBox + '\n' + card['power'] + '/' + card['toughness']

    return textBox

def __parseRandom(query):
    q = ""
    
    terms = query.upper().split("RANDOM")

    if terms[1] != "":
        q = terms[1]

    return q
