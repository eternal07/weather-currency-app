from flask import Flask
from flask import render_template
import os
import json
import datetime
import urllib
import io
import time
#import url_for
from flask import request
from flask import make_response
import sys
import logging


def get_weather(city):
    
    url = "http://api.openweathermap.org/data/2.5/forecast/daily?q={}&count=10&units=metric&mode=json&APPID=19c3424674144fdcbe5d0b597900a246".format("".join(city.split()))
    #url = "http://api.openweathermap.org/data/2.5/forecast/daily?q={}&count=10&units=metric&mode=json".format(city)
    #try:
    webdata = urllib.request.urlopen(url)

    
    #except urllib.error.HTTPError as e:
    #    print('status', e.code)
    #    print('reason', e.reason) 
         
    textdata = io.TextIOWrapper(webdata,encoding='utf-8')
    response_weather = textdata.read()
    return response_weather
    
    
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
@app.route('/')
def index():
    searchcity = request.args.get("searchcity")
    if not searchcity:
        searchcity = request.cookies.get("last_city")
    if not searchcity:
        searchcity = "London"
    print(searchcity)
    data = json.loads(get_weather(searchcity))
    
    try: 
        city = data['city']['name']
    except KeyError:
        return render_template("invalid_city.html", user_input=searchcity)
        
    country = data['city']['country']
    forecast_list = []

    for d in data.get('list'):
        
        day = time.strftime('%d %B', time.localtime(d.get('dt')))
        mini = (d.get("temp").get("min")) 
        maxi = (d.get("temp").get("max"))
        description = d.get("weather")[0].get("description")
        forecast_list.append((day,mini,maxi,description))
    response = make_response(render_template("index.html",forecast_list=forecast_list, city=city ,country=country))
    response.set_cookie("last_city","{},{}".format(city,country), expires=datetime.datetime.today() + datetime.timedelta(days=365))
    return response
 
    
   

if __name__ == '__main__':
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    