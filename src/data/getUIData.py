import urllib.request
import datetime
import re
import pandas as pd

#starting date
startDate = datetime.datetime.strptime("03/07/20", "%m/%d/%y")

#ending date
endingDate = datetime.datetime.strptime("07/18/20", "%m/%d/%y")

currDate = startDate

#iterating through the weeks until the ending date is reached
while (currDate <= endingDate):
    #creating the url string
    currString = (currDate.strftime("%m/%d/%y")).replace('/', '') 
    url = "https://oui.doleta.gov/unemploy/page8/2020/" + currString + ".html"
    
    #printing progress message
    print('working on week ended in: ' + currString)

    #reading in the table
    tables = pd.read_html(url, header=None)
    table = tables[0]

    #keeping only the initial claims from the table
    table = table.iloc[0:, : 4]
    
    #handling the HTML changes
    try:
        table.columns = table.columns.droplevel([-1, -2, -3]) 
    except:
        table.columns = table.columns.droplevel([-1, -2]) 

    #renaming the table
    table = table.rename(columns = {'STATENAME' : 'State', 'Initial Claims Filed During Week Ended  March 7, 2020' : 'Initial Claims', 'Initial Claims Filed During Week Ended  March 7, 2020' : 'Change From Last Week', 'Initial Claims Filed During Week Ended  March 7, 2020' : 'Change From Last Year'})
    
    #creating the filename
    filename = '../../data/raw/UI Claims/'+ currString + '_initial_claims.csv'

    #writing to the table
    table.to_csv(filename)
    
    #incrementing the date
    currDate = currDate + datetime.timedelta(days=7)

