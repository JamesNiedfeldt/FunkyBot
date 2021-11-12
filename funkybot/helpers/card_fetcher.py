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
    mod = ""
    
    try:
        if '|' in query:
            mod = query.split('|')[1].strip()
            query = query.split('|')[0].strip()

        if query.lower() == "random":
            if g.props['magic_ignore_digital']:
                mod += " not:digital"
            response = requests.get(url=random, params={'q':mod}, headers = g.apiHeaders)
            
        #Find by name first
        else:
            response = requests.get(url = name,
                                    params = {'fuzzy':query, 'set': mod},
                                    headers = g.apiHeaders)

            #Try finding by name without set code
            if response.status_code == 404 and mod != "":
                response = requests.get(url = name,
                                        params = {'fuzzy':query},
                                        headers = g.apiHeaders)

            #Try general search
            if response.status_code == 404:
                response = requests.get(url = search,
                                        params = {'q':query},
                                        headers = g.apiHeaders)

        results = response.json()

        #If found multiple cards, take the first
        if results['object'] == "list":
            card = results['data'][0]

        #Single card found
        elif results['object'] == "card":
            card = results

        #Nothing found
        else:
            return emb.empty("Sorry, I couldn't find \"{}\"!".format(query))

        #If digital prints not allowed, get a paper one
        if g.props['magic_ignore_digital'] and card['digital'] and mod == "":
            newQuery = ("oracleid:" + card['oracle_id']
                        + " not:back" + " not:digital")
            response = requests.get(url = search,
                                    params = {'q':newQuery},
                                    headers = g.apiHeaders)
            results = response.json()

            try:
                for c in results['data']:
                    if not c['digital'] and c['set_type'] != "memorabilia":
                        card = c
                        break
            except KeyError: #No non-digital print found, so just send it
                pass

        return __formatCard(card)

    except Exception as e:
        h.logException(e)
        return emb.empty("Sorry, something went wrong finding \"{}\"!".format(query))

def __formatCard(card, givenUri=None, givenPrice=None, givenColor=None, givenSetCode=None):
    name = card['name']
    cost = ""
    textBox = ""
    imageUri = ""
    price = "No price info found"
    color = 0
    setCode = ""
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
                elif g.props['magic_currency'] == 'tix':
                    price = price + " TIX"
    else:
        price = givenPrice

    if givenColor == None:
        color = __colorEmbed(card)
    else:
        color = givenColor

    if givenSetCode == None:
        setCode = card['set'].upper()
    else:
        setCode = givenSetCode
    
    if 'card_faces' in card:
        if card['layout'] == "transform" or card['layout'] == "modal_dfc":
            cost = card['card_faces'][0]['mana_cost']
                    
            for f in card['card_faces']:
                toReturn.append(__formatCard(f, givenUri=uri, givenPrice=price, givenColor=color, givenSetCode=setCode))
        else:
            imageUri = card['image_uris']['normal']
            toReturn = emb.Embeddable(
                url=uri,
                title=name + " " + cost,
                image=imageUri)
            
            for f in card['card_faces']:
                fieldName = "**" + f['name'] + "  " + f['mana_cost'] + "**" 
                fieldText = __makeTextBox(f)
                toReturn.addField({"name": fieldName,
                                   "value": fieldText,
                                   "inline": "true"})
            
            toReturn.setColor(color)
            toReturn.setFooter(setCode + " | " + price + " | Powered by Scryfall.com")

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
        toReturn.setColor(color)
        toReturn.setFooter(setCode + " | " + price + " | Powered by Scryfall.com")
        
    return toReturn

def __colorEmbed(card):
    if len(card['color_identity']) > 1:
        return 13408563
    elif len(card['color_identity']) == 0:
        return 10066329
    elif card['color_identity'][0] == 'W':
        return 16777214
    elif card['color_identity'][0] == 'U':
        return 39372
    elif card['color_identity'][0] == 'B':
        return 0
    elif card['color_identity'][0] == 'R':
        return 13369395
    elif card['color_identity'][0] == 'G':
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
