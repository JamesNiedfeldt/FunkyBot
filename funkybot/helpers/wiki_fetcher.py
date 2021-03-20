#==== Description ====
"""
Contains all necessary functions for searching up Wikipedia articles
"""

#==== Imports ====
import requests

from helpers.objects import embeddable as embed
from helpers import helper_functions as h

#==== Fetch an article from Wikipedia ====
def fetchArticle(query,headers):
    uri = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    notFound = "https://mediawiki.org/wiki/HyperSwitch/errors/not_found"

    try:
        response = requests.get(url=uri + query.replace(' ', '_'), headers=headers)
        results = response.json()

        if results['type'] == notFound:
            return embed.empty("Sorry, I couldn't find \"{}\"!".format(query))
        else:
            return __formatArticle(results) 

    except Exception as e:
        h.logException(e)
        return embed.empty("Sorry, something went wrong finding \"{}\"!".format(query))

def __formatArticle(article):
    title = article['title']
    description = article['description']
    extract = article['extract']
    url = article['content_urls']['desktop']['page']

    if "thumbnail" in article:
        imageUri = article['thumbnail']['source']
    else:
        imageUri = ""

    textBox = description + "\n-----\n" + extract

    return embed.Embeddable(url, title, textBox, imageUri)
