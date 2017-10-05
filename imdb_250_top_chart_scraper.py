# Simple IMDB scraping script for the top 250 movies

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve as uRet
#from pymongo import MongoClient
import re
import datetime

#mc = MongoClient('mongodb://127.0.0.1/default_db')
#db = mc.get_database()
#movieCharts = db.movie_charts

myUrl = 'http://www.imdb.com/chart/top'

uClient = uReq(myUrl)
pageHtml = uClient.read()
uClient.close()

pageSoup = soup(pageHtml, "html.parser")

chartTableRows = pageSoup.find('table', {'class':'chart'}).find('tbody').find_all('tr')

for tableRow in chartTableRows:

    posterColumn = tableRow.find('td', {'class':'posterColumn'})
    titleColumn = tableRow.find('td', {'class':'titleColumn'})
    movieRatingColumn = tableRow.find('td', {'class':'ratingColumn'})    

    movieId = re.search('t([0-9]+)', titleColumn.a['href'])[0]

    moviePosterSrc = re.sub('_[A-Z0-9_,]+.jpg$', '_V1_UY970_CR0,0,652,970_AL_.jpg', posterColumn.a.img['src'])
    
    movieTitle = titleColumn.a.text

    imdbUrl = titleColumn.a['href']
    
    mainCast = titleColumn.a['title']

    movieYear = re.sub('[^0-9]', '', titleColumn.span.text)

    movieRatingInfo = movieRatingColumn.strong['title']

    movieRating = movieRatingColumn.strong.text

    movie = {
        'rating': {
            'value':movieRating,
            'info':movieRatingInfo
        },
        'year':movieYear,
        'title':movieTitle,
        'movie_poster_url':moviePosterSrc,
        'imdb_url':imdbUrl,
        'top_cast': [x.strip() for x in mainCast.split(',')],
        'created_at':datetime.datetime.utcnow()
    }

    uRet(moviePosterSrc, 'posters/' + movieId + '.jpg')

    print(movieId)

    #_id = movieCharts.insert_one(movie).inserted_id

    #print(_id)

