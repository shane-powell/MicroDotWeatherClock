import time, datetime, thread, getopt, sys

# Python open weather maps api
import pyowm

#Microdot library
from microdotphat import HEIGHT, scroll,  write_string, scroll_vertical, show, clear

opts, args = getopt.getopt(sys.argv[1:], 'l:k:')

location = 'London, uk'
key = ''

#iterate over params to get location and key
for o, a in opts:
    if o == "-l":
        location = a
    if o == "-k":
        key = a

print location, key

alternate = ":"

clockDisplayTime = 10
alternateDisplayTime = 5
weaString = 'nodata'
statusString = ''
nextWeatherCheckTime = time.time()
w = ''

def getWeather(location, key):
    try:
        print "Using key", key
        owm = pyowm.OWM(key)
        print "Getting weather for", location
        obs = owm.weather_at_place(location)
        w = obs.get_weather()          
    except Exception, e:
        print e
        w= ''
        pass
    return w

while True:

    clockEndTime = time.time() + clockDisplayTime
    while time.time() < clockEndTime:
        print time.time()
        print clockEndTime
        if alternate == ":":
            alternate = " "
        else:
            alternate = ":"
        now = datetime.datetime.now()

        clockString = str(now.hour) + alternate + str(now.minute).zfill(2)
        clear()
        write_string(clockString,0, kerning=False)

        show()
    
        time.sleep(1)

    print "Entering alternate state"


    #Get Weather
    if w == '' or time.time() > nextWeatherCheckTime:
        print 'Getting weather'
        w = getWeather(location, key)
        if w != '':
            print 'Got weather'
            weaString = str(w.get_temperature(unit='celsius')['temp']) + 'C'
            statusString = w.get_status()
            print w.get_status()
            print weaString
        else:
            print 'Failed to get weather!'
        #Add 30 minutes to next check time
        nextWeatherCheckTime = time.time() +  1800

    alternateEndTime = time.time() + alternateDisplayTime
    lines = [weaString, statusString]

    #clear matrix
    clear()

    for line, text in enumerate(lines):
        write_string(text, offset_y = line*7, kerning=False)
    
    show()
    while time.time() < alternateEndTime:
        for x in range(7):
            scroll_vertical()
            show()
            time.sleep(0.02)
        time.sleep(1)
