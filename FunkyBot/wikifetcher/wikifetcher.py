#==== Description ====
"""
Contains all necessary functions for searching up Wikipedia articles
"""

#==== Imports ====
import requests

#==== Fetch an article from Wikipedia ====
def fetchArticle(query):
    uri = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    notFound = "https://mediawiki.org/wiki/HyperSwitch/errors/not_found"

    try:
        response = requests.get(url = uri + query.replace(' ', '_'))
        results = response.json()

        if results['type'] == notFound:
            return [None, "Sorry, I couldn't find \"{}\"!".format(query)]
        else:
            return formatArticle(results) 

    except KeyError as e:
        return [None, "Something went wrong!"]

def formatArticle(article):
    title = article['title']
    description = article['description']
    extract = article['extract']
    url = article['content_urls']['desktop']['page']

    if "thumbnail" in article:
        imageUri = article['thumbnail']['source']
    else:
        imageUri = ""

    textBox = description + "\n-----\n" + extract

    return [url, title, textBox, imageUri]