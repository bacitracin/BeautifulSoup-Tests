# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:14:52 2015

@author: E028770

Using Beautiful Soup to pull down trip reviews from CruiseCritic.com, stores
review info in a CSV
"""

# Maybe later rewrite this using Requests instead of urllib2
from bs4 import BeautifulSoup
from urllib2 import urlopen

# The links on the review pages are relative
base_url = 'http://www.cruisecritic.com'

# These are the individual cruise ship pages, manually entered 
# For next step, scrape these links from the main brand page: 
# http://www.cruisecritic.com/memberreviews/viking-river-cruises/cl/ for example
viking_emerald_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641'
viking_prestige_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=639'
viking_sun_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=392'
viking_legend_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=537'
viking_idun_url = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=660'

viking_emerald_url_2 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=2'
viking_emerald_url_3 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=3'
viking_emerald_url_4 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=4'


# Starts on the cruise page, stores the links to the 25 reviews to a list
def get_cruise_review_links(ship_page):
    individual_review_list = []    
    html = urlopen(ship_page).read()
    ship_soup = BeautifulSoup(html, 'lxml')
    ship_reviews = ship_soup.findAll("div", class_="pull-left review-results-title")

# Grabs the link to the individual review page, adds it to the individual_review_list
    for review in ship_reviews:
        link = review.find('a')['href']
        individual_review_url = base_url + link
        individual_review_list.append(individual_review_url)
         
# Downloading the relevant bits from the page, stores them in a dict
def cruise_review_metrics(individual_review_url):
    html = urlopen(individual_review_url).read()
    review_soup = BeautifulSoup(html, 'lxml')
    main_review_soup = review_soup.find('div', id = 'main-review')
   
# Review Summary
    title = main_review_soup.find("h2").string
   # review_info[username] = review_soup2.find("div", id = "user-user-name").string
    overall_rating = main_review_soup.find('img')['src']
    review_details = main_review_soup.findAll("div", class_="col-sm-4")        
    sail_date, destination, embarkation = review_details[0], review_details[1], review_details[2]
    sail_date, destination, embarkation = sail_date.contents[2], destination.contents[2], embarkation.contents[2]
    sail_date, destination, embarkation = sail_date.strip(), destination.strip(), embarkation.strip()

    body_text= main_review_soup.find("p")
    body_text= body_text.contents
    body_text = body_text[1]
    
    review_date


# Specific ratings    
    cabin_review_soup = review_soup.find('div', class_='subreview')    
    cabin_name = cabin_review_soup.find("h2").string      
    cabin_rating = cabin_review_soup.find('img')['src'] 
    cabin_review = cabin_review_soup.find("p")
    
    dining_rating =
    embarkation_rating =
    enrichment_rating =
    entertainment_rating =
    family_rating =
    fitness_rating =
    public_room_rating =
    rates_rating =
    service_rating =
    shore_excursions_rating =
    value_rating =

# User stats   
    user_number_of_reviews = review_soup.find('div', id = "user-total-reviews")
    user_number_of_reviews = user_number_of_reviews.contents
    user_number_of_reviews = user_number_of_reviews[1]
    
    user_total_posts = review_soup.find('div', id = 'user-total-posts')
    user_total_posts = user_total_posts.string
    
    user_join_year = review_soup.find('div', id = 'user-join-year')
    user_join_year = user_join_year.string

# Throw the stats into a dictionary for the review    
    review_info = {"title" : title,
                   "username" : username,
                   "overall rating" : overall_rating,
                   "sail date" : sail_date,
                   "destination" : destination,
                   "embarkation" : embarkation,
                   "review text" : body_text,
                   "cabin rating" : cabin_rating,
                   "dining rating" : dining_rating,
                   "embarkation rating" : embarkataion_rating,
                   "enrichment rating" : enrichment_rating,
                   "entertainment rating" : entertainment_rating,
                   "family rating" : family_rating,
                   "fitness rating" : fitness_rating,
                   "public room rating" : public_room_rating,
                   "rates rating" : rates_rating,
                   "service rating" : service_rating,
                   "shore excursions rating" : shore_excursions_rating,
                   "value rating" : value_rating,
                   "no. of user reviews" : user_number_of_reviews,
                   "user total posts" : user_total_posts,
                   "user join year" : user_join_year}    
    return review_info    
        
# Iterate across the list of member reviews, save in dataframe, output as CSV
def pull_cruise_reviews(individual_review_list):
    for url in individual_review_list:
        cruise_review_metrics(url)
        
    