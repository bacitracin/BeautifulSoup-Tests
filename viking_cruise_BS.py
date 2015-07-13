# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:14:52 2015

@author: E028770
"""


# This script is for downloading the body of a webpage. Based on Automate the boring stuff

from bs4 import BeautifulSoup
from urllib2 import urlopen

# The links on the review pages are relative
base_url = 'http://www.cruisecritic.com'

# These are the individual cruise ship pages
viking_emerald_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641'
viking_prestige_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=639'
viking_sun_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=392'
viking_legend_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=537'
viking_idun_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=660'

http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=2
http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=3
http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=4

# Starts on the individual ship page, scrapes the reviews (25 per page)
def get_cruise_review_links(ship_page):
    html = urlopen(ship_page).read()
    ship_soup = BeautifulSoup(html, 'lxml')
    ship_reviews = ship_soup.findAll("div", class_="pull-left review-results-title")

#Grabs the link to the individual review page
    for review in ship_reviews:
        link = review.find('a')['href']
        individual_review_url = base_url + link
        

# Extracting the URL from within the page's <a> tags
for link in soup.find_all('a'):
    print(link.get('href'))

    
    #Find the body of the text
    
    #todo : download the page
    #
    