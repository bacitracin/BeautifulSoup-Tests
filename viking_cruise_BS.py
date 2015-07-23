# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:14:52 2015

@author: Tracy

Using Beautiful Soup to pull down trip reviews from CruiseCritic.com, stores
review info in a CSV
"""

# Maybe later rewrite this using Requests instead of urllib2
from bs4 import BeautifulSoup
from urllib2 import urlopen
import pandas as pd

# The links on the review pages are relative
base_url = 'http://www.cruisecritic.com'

# These are the individual cruise ship pages, manually entered 
# For next step, scrape these links from the main brand page, also add in Selenium for pagination
# http://www.cruisecritic.com/memberreviews/viking-river-cruises/cl/ for example

viking_emerald_url_1= 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641'
viking_emerald_url_2 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=2'
viking_emerald_url_3 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=3'
viking_emerald_url_4 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=4'
viking_emerald_url_5 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=641&page=5'
viking_emerald=[viking_emerald_url_1, viking_emerald_url_2, viking_emerald_url_3,
               viking_emerald_url_4, viking_emerald_url_5]

viking_prestige_url_1= 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=639'
viking_prestige_url_2= 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=639&page=2'
viking_prestige_url_3= 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=639&page=3'
viking_prestige=[viking_prestige_url_1, viking_prestige_url_2, viking_prestige_url_3]
                 

viking_sun_url_1 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=392'
viking_sun_url_2 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=392&page=2'
viking_sun_url_3 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=392&page=3'
viking_sun = [viking_sun_url_1, viking_sun_url_2, viking_sun_url_3]

viking_legend_url_1 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=537'
viking_legend_url_2 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=537&page=2'
viking_legend_url_3 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=537&page=3'
viking_legend = [viking_legend_url_1, viking_legend_url_2, viking_legend_url_3]

viking_idun_url_1 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=660'
viking_idun_url_2 = 'http://www.cruisecritic.com/memberreviews/getreviews.cfm?action=ship&ShipID=660&page=2'
viking_idun = [viking_idun_url_1, viking_idun_url_2]

list_of_urls= [viking_emerald, viking_prestige, viking_sun, viking_legend, viking_idun]
        
# Starts on the given cruise ship review page (urls above), stores the links 
# to individual reviews to a list
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
    return individual_review_list
       

# Downloading the relevant bits from the individual review page, stores them in a dict
def cruise_review_metrics(individual_review_url):
    html = urlopen(individual_review_url).read()
    review_soup = BeautifulSoup(html, 'lxml')
    main_review_soup = review_soup.find('div', id = 'main-review')
   
# Review Summary Stats
    title = main_review_soup.find("h2").string
    username = review_soup.find('div', id = "user-user-name").string.strip()
    overall_rating = main_review_soup.find('img')['src']
    review_details = main_review_soup.findAll("div", class_="col-sm-4")        
    sail_date, destination, embarkation = review_details[0], review_details[1], review_details[2]
    sail_date, destination, embarkation = sail_date.contents[2], destination.contents[2], embarkation.contents[2]
    sail_date, destination, embarkation = sail_date.strip(), destination.strip(), embarkation.strip()

    body_text_soup= main_review_soup.find("p")
    body_text= body_text_soup.contents
    body_text = body_text[1]
    
    #review_date = body_text_soup.find("i")

# Specific ratings    
    cabin_review_soup = review_soup.find('div', class_='subreview')    
    cabin_name = cabin_review_soup.find("h2").string      
    cabin_rating = cabin_review_soup.find('img')['src'] 
    cabin_review = cabin_review_soup.find("p")
    
    table_soup = review_soup.findAll('table')  
    table_one = list(table_soup[0]) #left side of table
    table_two = list(table_soup[1]) #right side of table
    
    dining_rating = list(table_one[3])[3]       
    embarkation_rating = list(table_one[5])[3] 
    enrichment_rating = list(table_one[7])[3]
    entertainment_rating = list(table_one[9])[3]  
    family_rating = list(table_one[11])[3]
    
    fitness_rating = list(table_two[1])[3]  
    public_room_rating = list(table_two[3])[3]    
    rates_rating = list(table_two[5])[3]   
    service_rating = list(table_two[7])[3] 
    shore_excursions_rating = list(table_two[9])[3]  
    value_rating = list(table_two[11])[3]

# User stats   
    
    user_number_of_reviews = review_soup.find('div', id = "user-total-reviews").contents
    user_number_of_reviews = user_number_of_reviews[1]
    
    user_total_posts = review_soup.find('div', id = 'user-total-posts')
    user_total_posts = user_total_posts.string

    user_join_year = review_soup.find('div', id = 'user-join-year')
    user_join_year = user_join_year.string

# Throw the stats into a dictionary for the review    
    review_info = {"ship name" : individual_review_url, 
                   "title" : str(title),
                   "username" : str(username),
                   "overall rating" : overall_rating,
                   "sail date" : str(sail_date),
                   "destination" : str(destination),
                   "embarkation" : str(embarkation),
                   "review text" : body_text,
                   "cabin name" : str(cabin_name),
                   "cabin rating" : cabin_rating,
                   "cabin review" : str(cabin_review),
                   "dining rating" : dining_rating,
                   "embarkation rating" : embarkation_rating,
                   "enrichment rating" : enrichment_rating,
                   "entertainment rating" : entertainment_rating,
                   "family rating" : family_rating,
                   "fitness rating" : fitness_rating,
                   "public room rating" : public_room_rating,
                   "rates rating" : rates_rating,
                   "service rating" : service_rating,
                   "shore excursions rating" : shore_excursions_rating,
                   "value rating" : value_rating,
                   "no. of user reviews" : str(user_number_of_reviews.string),
                   "user total posts" : str(user_total_posts.strip()),
                   "user join year" : str(user_join_year.strip())}      
    return review_info

# Throwing the dictionary into a dataframe & saving it as a CSV
#def write_to_csv:
    #review_df = pd.DataFrame(review_info, index = index, columns = columns)

#review_info = {
#"title" : str(title),
            #   "username" : str(username),
            #   "overall rating" : overall_rating,
            #   "sail date" : str(sail_date),
            #   "destination" : str(destination),
            #   "embarkation" : str(embarkation),
             #  "review text" : body_text,
             #  "cabin name" : str(cabin_name),
             #  "cabin rating" : cabin_rating,
             # "cabin review" : str(cabin_review),
             #  "dining rating" : dining_rating,
             #  "embarkation rating" : embarkation_rating,
             #  "enrichment rating" : enrichment_rating,
             #  "entertainment rating" : entertainment_rating,
             #  "family rating" : family_rating,
             #  "fitness rating" : fitness_rating,
             #  "public room rating" : public_room_rating,
             #  "rates rating" : rates_rating,
             #  "service rating" : service_rating,
             #  "shore excursions rating" : shore_excursions_rating,
             #  "value rating" : value_rating,
             #  "no. of user reviews" : str(user_number_of_reviews.string),
             #  "user total posts" : str(user_total_posts.strip()),
             #  "user join year" : str(user_join_year.strip())}    
                   
# To see what's in the dataframe without checking the CSV, 
# just type "item_dataframe" into the console.

# Appending the dataframe to a CSV. Edit the CSV name here.
#with open('testfile.csv', 'a') as fd:             
 #   item_dataframe.index += 1        
 #   item_dataframe.to_csv(fd, mode='a',header=False, encoding='utf-8')
 #   fd.close()       
    
# Iterate across the list of member reviews, save in dataframe, output as CSV
def pull_cruise_reviews(individual_review_list):
    for url in individual_review_list:
        cruise_review_metrics(url)
        
# in order to pull the list... 
# ship_review_links = get_cruise_review_links(ship_page) 
        
        
# 1. Pull all member reviews for each ship    
#ship_review_links = get_cruise_review_links(ship_page) 

# 2. Iterate across the member reviews & pull each individual review as a dictionary

# 3. Save each dictionary as a row to the Pandas Dataframe

# 4. Write the DF to a CSV, append       

#rows_list.append(individual_review)

#ship_df = pd.DataFrame(rows_list)


#DataFrame.append()

#rows_list = []
#for row in input_rows:

 #       dict1 = {}
        # get input row in dictionary format
        # key = col_name
  #      dict1.update(blah..) 





