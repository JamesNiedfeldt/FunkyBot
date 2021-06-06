#==== Description ====
"""
Contains all necessary functions for searching up games via GiantBomb
"""

#==== Imports ====
import requests
from datetime import datetime as dt

from helpers.objects import embeddable as embed
from helpers import helper_functions as h, global_vars as g

#==== Fetch an article from Wikipedia ====
def fetchGame(query):
    uri = "https://www.giantbomb.com/api/search/"
    helpText = ("[Click here](https://giantbomb.com/search/?q={})".format(query.replace(' ','+'))
                + " for the full search results.")
    searchField = {"name": "Wrong result?", "value": helpText}
    
    params = {
        'query': query,
        'api_key': g.props['giantbomb_key'],
        'format': 'json',
        'limit': '1',
        'resources': 'game',
        'field_list': 'api_detail_url,site_detail_url'}

    try:
        response = requests.get(url=uri, headers=g.apiHeaders, params=params)
        results = response.json()

        if results['number_of_total_results'] == 0:
            return embed.empty("Sorry, I couldn't find \"{}\"!".format(query))
        else:
            toReturn = __formatResult(results['results'][0]['api_detail_url'],
                                      results['results'][0]['site_detail_url'])
            toReturn.addField(searchField)
            return toReturn

    except Exception as e:
        h.logException(e)
        return embed.empty("Sorry, something went wrong finding \"{}\"!".format(query))

def __formatResult(newUri, siteUrl):
    params = {
        'api_key': g.props['giantbomb_key'],
        'format': 'json',
        'field_list': 'deck,developers,genres,image,name,original_release_date,platforms,publishers,similar_games'}
    try:
        response = requests.get(url=newUri, headers=g.apiHeaders, params=params)
        gameResult = response.json()
    except Exception as e:
        raise

    title = gameResult['results']['name']
    text = gameResult['results']['deck']
    imageUri = gameResult['results']['image']['medium_url']
    toReturn = embed.Embeddable(url=siteUrl,
                                title=title,
                                text=text,
                                image=imageUri)

    #Grab genres
    genreField = {"inline": "true", "name": "Genre", "value": ""}
    if 'genres' not in gameResult['results']:
        genreField['value'] = "No genre information found"
    else:
        for r in gameResult['results']['genres']:
            genreField['value'] += r['name'] + ", "
        genreField['value'] = genreField['value'][:-2]

    #Grab release date
    releaseField = {"inline": "true", "name": "Release date", "value": ""}
    if gameResult['results']['original_release_date'] == None:
        releaseField['value'] = "Not currently released"
    else:
        tmp = gameResult['results']['original_release_date']
        tmp = dt.strptime(tmp, '%Y-%m-%d').strftime('%b %d, %Y')
        releaseField['value'] = tmp

    #Grab platforms
    platField = {"name": "Playable on", "value": ""}
    for p in gameResult['results']['platforms']:
        platField['value'] += p['name'] + ", "
    platField['value'] = platField['value'][:-2]

    #Grab developers
    devField = {"inline": "true", "name": "Developers", "value": ""}
    for d in gameResult['results']['developers']:
        devField['value'] += d['name'] + ", "
    devField['value'] = devField['value'][:-2]

    #Grab publishers
    pubField = {"inline": "true", "name": "Publishers", "value": ""}
    if gameResult['results']['publishers'] == None:
        pubField['value'] = "No publisher information found"
    else:
        for p in gameResult['results']['publishers']:
            pubField['value'] += p['name'] + ", "
        pubField['value'] = pubField['value'][:-2]

    #Grab similar games
    similarField = {"name": "Here are some similar games:", "value": ""}
    if gameResult['results']['similar_games'] == None:
        similarField['value'] = "Sorry, I couldn't find any similar games to this one."
    else:
        for s in range(min(3, len(gameResult['results']['similar_games']))):
            similarField['value'] += (
                gameResult['results']['similar_games'][s]['name'] + ", ")
        similarField['value'] = similarField['value'][:-2]

    toReturn.addField(genreField,releaseField,platField,devField,pubField,similarField)
    toReturn.setFooter("Powered by GiantBomb.com")

    return toReturn
