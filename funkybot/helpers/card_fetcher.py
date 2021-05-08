#==== Description ====
"""
Contains all necessary functions for searching up Magic: the Gathering cards
"""

#==== Imports ====
import requests

from helpers.objects import embeddable as emb
from helpers import helper_functions as h, global_vars as g

#==== Fetch a card from Scryfall ====
def fetchCard(query):
    name = "https://api.scryfall.com/cards/named"
    search = "https://api.scryfall.com/cards/search"
    random = "https://api.scryfall.com/cards/random"
    
    try:
        #Random card requested
        if query.upper().startswith("RANDOM"):
            response = requests.get(url = random, params = {'q':__parseRandom(query)}, headers = g.apiHeaders)
            results = response.json()

        else:
            #Find by name first
            response = requests.get(url = name, params = {'fuzzy':query}, headers = g.apiHeaders)
            results = response.json()

            if results['object'] == "error":
                #Try a search if not found by name
                response = requests.get(url = search, params = {'q':query}, headers = g.apiHeaders)
                results = response.json()

        #If found multiple cards, take the first
        if results['object'] == "list":
            return __formatCard(results['data'][0])

        #Single card found
        elif results['object'] == "card":
            return __formatCard(results)

        #Nothing found
        else:
            return emb.empty("Sorry, I couldn't find \"{}\"!".format(query))

    except Exception as e:
        h.logException(e)
        return emb.empty("Sorry, something went wrong finding \"{}\"!".format(query))

def __formatCard(card, givenUri=None, givenPrice=None):
    name = card['name']
    cost = ""
    textBox = ""
    imageUri = ""
    price = "No price info found"
    toReturn = []

    if givenUri == None:
        uri = card['scryfall_uri']
    else:
        uri = givenUri

    if givenPrice == None:
        if 'prices' in card and card['prices'][g.props['magic_currency']] != None:
                price = card['prices'][g.props['magic_currency']]
                if g.props['magic_currency'] == 'usd':
                    price = "$" + price
                elif g.props['magic_currency'] == 'eur':
                    price = "€" + price
    else:
        price = givenPrice
    
    if 'card_faces' in card:
        if card['layout'] == "transform" or card['layout'] == "modal_dfc":
            cost = card['card_faces'][0]['mana_cost']
            
            if 'prices' in card and card['prices'][g.props['magic_currency']] != None:
                price = card['prices'][g.props['magic_currency']]
                if g.props['magic_currency'] == 'usd':
                    price = "$" + price
                elif g.props['magic_currency'] == 'eur':
                    price = "€" + price
                    
            for f in card['card_faces']:
                toReturn.append(__formatCard(f, givenUri=uri, givenPrice=price))
        else:
            textBox = card['type_line']
            for f in card['card_faces']:
                textBox = (textBox + "\n\n" + 
                           "**" + f['name'] + "  " + f['mana_cost'] + "**" +
                           "\n" + __makeTextBox(f))
            cost = card['mana_cost']
            imageUri = card['image_uris']['normal']
            
            if 'prices' in card and card['prices'][g.props['magic_currency']] != None:
                price = card['prices'][g.props['magic_currency']]
                if g.props['magic_currency'] == 'usd':
                    price = "$" + price
                elif g.props['magic_currency'] == 'eur':
                    price = "€" + price
                
            toReturn = emb.Embeddable(
                url=uri,
                title=name + " " + cost,
                text=textBox,
                image=imageUri)
            toReturn.setColor(__colorEmbed(card))
            toReturn.setFooter(price)

    else:
        textBox = __makeTextBox(card)
        cost = card['mana_cost']
        imageUri = card['image_uris']['normal']
        
        if 'prices' in card and card['prices'][g.props['magic_currency']] != None:
            price = card['prices'][g.props['magic_currency']]
            if g.props['magic_currency'] == 'usd':
                price = "$" + price
            elif g.props['magic_currency'] == 'eur':
                price = "€" + price
            
        toReturn = emb.Embeddable(
            url=uri,
            title=name + " " + cost,
            text=textBox,
            image=imageUri)
        toReturn.setColor(__colorEmbed(card))
        toReturn.setFooter(price)
        
    return toReturn

def __colorEmbed(card):
    if "Land" in card['type_line']:
        return 6697779
    elif len(card['colors']) > 1:
        return 13408563
    elif len(card['colors']) == 0:
        return 10066329
    elif card['colors'][0] == 'W':
        return 16777214
    elif card['colors'][0] == 'U':
        return 39372
    elif card['colors'][0] == 'B':
        return 0
    elif card['colors'][0] == 'R':
        return 13369395
    elif card['colors'][0] == 'G':
        return 32768
    else:
        return 2303786

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
