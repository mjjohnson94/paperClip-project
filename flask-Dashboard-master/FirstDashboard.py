####################################################################################################

from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


####################################################################################################

app = Flask(__name__)

####################################################################################################

@app.route('/')
def index():

    return render_template('index2.html')

@app.route('/about')
def about():

    return render_template('index3.html')


##################################################### Interactive Button  ###############################################

@app.route('/', methods=['POST'])
def myFormPost():

    text = request.form['text']
    text = ('"' + text + '"')
    
    accessToken = "216111107-PuNWn73xXIm2I8KNyLjnqp0yeuL2huNOuYJqsPOp"
    accessTokenSecret = "UR0blltttJ4ZMrBPkoCAvTZThn9bZ1AYdCeen0WFtKOnK"
    apiKey = "0WyEYyOyQZNfZnuyPDaEryKYF"
    secretKey = "OrMJYIVgXwsjRHs8RuYPX6hLkvDkjNg8tLaTVDhwZ2knVwugZd"


    from TwitterAPI import TwitterAPI
    api = TwitterAPI(apiKey, secretKey, accessToken, accessTokenSecret)

    r = api.request('search/tweets', {'q': text})

    bar = createBarPlot()
    line = createLinePlot()
    tweets = getTweets()
    scorecard = compoundScoreCard()
    map = createMap()

    return render_template('index.html', plot=bar, plot2=line, tweets=tweets, scorecard=scorecard, map=map, tables=[tweets.to_html(classes='data')], titles=tweets.columns.values)


#################################################   Bar Plot    ###################################################

def createBarPlot():

    text = request.form['text']
    text = ('"' + text + '"')

    accessToken = "216111107-PuNWn73xXIm2I8KNyLjnqp0yeuL2huNOuYJqsPOp"
    accessTokenSecret = "UR0blltttJ4ZMrBPkoCAvTZThn9bZ1AYdCeen0WFtKOnK"
    apiKey = "0WyEYyOyQZNfZnuyPDaEryKYF"
    secretKey = "OrMJYIVgXwsjRHs8RuYPX6hLkvDkjNg8tLaTVDhwZ2knVwugZd"


    from TwitterAPI import TwitterAPI
    api = TwitterAPI(apiKey, secretKey, accessToken, accessTokenSecret)

    r = api.request('search/tweets', {'q': text})

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
   
    analyzer = SentimentIntensityAnalyzer()
    sent=[]
    compound = []

    for x in r:

        sent.append(x['text']) 
        vs = analyzer.polarity_scores(sent)
        compound.append(vs['compound']) 

    # r2 = api.request('search/tweets', {'q': text})

    # for x in r2:

    #     sent.append(x['text']) 
    #     vs = analyzer.polarity_scores(sent)
    #     compound.append(vs['compound']) 

    # r3 = api.request('search/tweets', {'q': text})

    # for x in r3:

    #     sent.append(x['text']) 
    #     vs = analyzer.polarity_scores(sent)
    #     compound.append(vs['compound']) 

    # r4 = api.request('search/tweets', {'q': text})

    # for x in r4:

    #     sent.append(x['text']) 
    #     vs = analyzer.polarity_scores(sent)
    #     compound.append(vs['compound']) 

    # r5 = api.request('search/tweets', {'q': text})

    # for x in r5:

    #     sent.append(x['text']) 
    #     vs = analyzer.polarity_scores(sent)
    #     compound.append(vs['compound']) 

        neg = []
        neu = []
        pos = []

    for tweet in sent:
        vs = analyzer.polarity_scores(tweet)
        neg.append(vs['neg'])
        neu.append(vs['neu'])
        pos.append(vs['pos'])

    import statistics
    negativeMean=statistics.mean(neg) 
    positiveMean=statistics.mean(pos) 

    trace1 = go.Bar(         
    y=[positiveMean, negativeMean],
    x=['Positive', 'Negative'],          
    opacity = 1,
    )

    data = [trace1]

    layout = go.Layout(
    autosize=False,
    width=400,
    height=400,
    

    margin=go.layout.Margin(
    pad = 4
    )
)
    layout = go.Layout(
    paper_bgcolor='#1E1E2F',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=False)
)

    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
    margin=dict(l=25, r=25, t=25, b=25))

    fig.update_layout(
    title="Total Tweets by Sentiment Category",
    xaxis_title="Sentiment Category",
    yaxis_title="Total Tweets",
    font=dict(
        family="Open Sans, sans-serif",
        size=12,
        color="#FFFFFF"
    )
)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

###################################################################################################

def createLinePlot():

    text = request.form['text']
    text = ('"' + text + '"')

    accessToken = "216111107-PuNWn73xXIm2I8KNyLjnqp0yeuL2huNOuYJqsPOp"
    accessTokenSecret = "UR0blltttJ4ZMrBPkoCAvTZThn9bZ1AYdCeen0WFtKOnK"
    apiKey = "0WyEYyOyQZNfZnuyPDaEryKYF"
    secretKey = "OrMJYIVgXwsjRHs8RuYPX6hLkvDkjNg8tLaTVDhwZ2knVwugZd"


    from TwitterAPI import TwitterAPI
    api = TwitterAPI(apiKey, secretKey, accessToken, accessTokenSecret)

    r = api.request('search/tweets',  {'q': text, 
                                  'count': 5, 
                                  'until': '2021-10-12',
                                  'lang': 'en'    
                                    
                                  })

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
   
    analyzer = SentimentIntensityAnalyzer()
    sent=[]

    rcompound = []
    r2compound = []
    r3compound = []
    r4compound = []
    r5compound = []

    tweetDate = []

    for x in r:

        sent.append(x['text']) 
        vs = analyzer.polarity_scores(sent)
        rcompound.append(vs['compound']) 
        tweetDate.append(x['created_at']) 
        

        r2 = api.request('search/tweets', {'q': text, 
                                  'count': 5, 
                                  'until': '2021-10-13',
                                  'lang': 'en'    
                                    
                                  })



    for x in r2:

        sent.append(x['text']) 
        vs = analyzer.polarity_scores(sent)
        r2compound.append(vs['compound']) 
        tweetDate.append(x['created_at']) 

    r3 = api.request('search/tweets', {'q': text, 
                                  'count': 5, 
                                  'until': '2021-10-14',
                                  'lang': 'en'    
                                    
                                  })

    for x in r3:

        sent.append(x['text']) 
        vs = analyzer.polarity_scores(sent)
        r3compound.append(vs['compound']) 
        tweetDate.append(x['created_at']) 

    r4 = api.request('search/tweets', {'q': text, 
                                  'count': 5, 
                                  'until': '2021-10-15',
                                  'lang': 'en'    
                                    
                                  })

    for x in r4:

        sent.append(x['text']) 
        vs = analyzer.polarity_scores(sent)
        r4compound.append(vs['compound']) 

    r5 = api.request('search/tweets', {'q': text, 
                                  'count': 5, 
                                  'until': '2021-10-16',
                                  'lang': 'en'    
                                    
                                  })

    for x in r5:

        sent.append(x['text']) 
        vs = analyzer.polarity_scores(sent)
        r5compound.append(vs['compound']) 
        tweetDate.append(x['created_at']) 

    import statistics

    compoundMean1=statistics.mean(rcompound) 
    compoundMean2=statistics.mean(r2compound) 
    compoundMean3=statistics.mean(r3compound) 
    compoundMean4=statistics.mean(r4compound) 
    compoundMean5=statistics.mean(r5compound) 


    dates = pd.to_datetime(tweetDate)
    dates=dates.sort_values()

    cleanDates = []

    for x in dates:
        cleanDates.append(x)    


    trace1 = go.Scatter(         
    y=[compoundMean1, compoundMean2, compoundMean3, compoundMean4, compoundMean5], 
    x=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
    opacity = 0.8,
    marker=dict(color='#e14eca'))

    data = [trace1]

    layout = go.Layout(
    autosize=False,
    width=400,
    height=400,

    margin=go.layout.Margin(
    pad = 4
    )
)
    layout = go.Layout(
    paper_bgcolor='#1E1E2F',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=False),
    xaxis=dict(showgrid=False),
)

    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
    margin=dict(l=25, r=25, t=25, b=25))

    fig.update_layout(
    title="Weekly Sentiment Overview",
    xaxis_title="Date",
    yaxis_title="Compound Sentiment Score",
    font=dict(
        family="Open Sans, sans-serif",
        size=12,
        color="#FFFFFF"
    )
)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

##################################################################################################


def getTweets():

    text = request.form['text']
    text = ('"' + text + '"')

    accessToken = "216111107-PuNWn73xXIm2I8KNyLjnqp0yeuL2huNOuYJqsPOp"
    accessTokenSecret = "UR0blltttJ4ZMrBPkoCAvTZThn9bZ1AYdCeen0WFtKOnK"
    apiKey = "0WyEYyOyQZNfZnuyPDaEryKYF"
    secretKey = "OrMJYIVgXwsjRHs8RuYPX6hLkvDkjNg8tLaTVDhwZ2knVwugZd"


    from TwitterAPI import TwitterAPI
    api = TwitterAPI(apiKey, secretKey, accessToken, accessTokenSecret)

    r = api.request('search/tweets', {'q': text})

    latestTweets = []

    for x in r:

        latestTweets.append(x['text']) 
        
    tweetLocationDF = pd.DataFrame({'Tweets': latestTweets})
    tweetLocationDF.set_index('Tweets')
    
    return tweetLocationDF

###################################################################################################

def compoundScoreCard():

    text = request.form['text']
    text = ('"' + text + '"')

    accessToken = "216111107-PuNWn73xXIm2I8KNyLjnqp0yeuL2huNOuYJqsPOp"
    accessTokenSecret = "UR0blltttJ4ZMrBPkoCAvTZThn9bZ1AYdCeen0WFtKOnK"
    apiKey = "0WyEYyOyQZNfZnuyPDaEryKYF"
    secretKey = "OrMJYIVgXwsjRHs8RuYPX6hLkvDkjNg8tLaTVDhwZ2knVwugZd"


    from TwitterAPI import TwitterAPI
    api = TwitterAPI(apiKey, secretKey, accessToken, accessTokenSecret)

    r = api.request('search/tweets', {'q': text})

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
   
    analyzer = SentimentIntensityAnalyzer()
    tweet=[]
    compound = []

    for x in r:

        tweet.append(x['text']) 
        vs = analyzer.polarity_scores(tweet)
        compound.append(vs['compound']) 

        compoundScore = np.mean(compound)

        return compoundScore

################################################ MAP ############################################

def createMap():

    import plotly.graph_objects as go

    text = request.form['text']
    text = ('"' + text + '"')

    accessToken = "216111107-PuNWn73xXIm2I8KNyLjnqp0yeuL2huNOuYJqsPOp"
    accessTokenSecret = "UR0blltttJ4ZMrBPkoCAvTZThn9bZ1AYdCeen0WFtKOnK"
    apiKey = "0WyEYyOyQZNfZnuyPDaEryKYF"
    secretKey = "OrMJYIVgXwsjRHs8RuYPX6hLkvDkjNg8tLaTVDhwZ2knVwugZd"


    from TwitterAPI import TwitterAPI
    api = TwitterAPI(apiKey, secretKey, accessToken, accessTokenSecret)

    r = api.request('search/tweets', {'q': text})

    tweetLocation = []

    for x in r: 
    
        tweetLocation.append(x['user']['location'])

    cleanLocationDF = []

    for x in tweetLocation:
        if (x != ""):
            cleanLocationDF.append(x)

    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="app.py") 

    lat=[]
    lon=[]

    for x in cleanLocationDF:
    
        try: 
        
            geolocator = Nominatim(user_agent="appy.py")
            y = geolocator.geocode(x)
            lat.append(y.latitude)
            lon.append(y.longitude)
            
        except Exception:
            pass


    fig = go.Figure(go.Scattermapbox(
    lon = lon, 
    lat = lat,
    mode='markers',
    marker = { 'size': 14, 'color': '#e14eca' }))

    fig.update_layout(
    mapbox = {
        'style': "carto-darkmatter",
        'center': {'lon': -73, 'lat': 46 },
        'zoom': 2},
    showlegend = False)

    fig.update_layout(paper_bgcolor="#1E1E2F")

    fig.update_layout(height=400)

    fig.update_layout(
    margin=dict(l=5, r=5, t=5, b=5))

    fig.show()

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

if __name__ == '__main__':
    app.run()
