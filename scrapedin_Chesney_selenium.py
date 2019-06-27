# -*- coding: utf-8 -*-
"""
Spyder Editor
6/27/2019

Playing around with scraping one profile (Rebecca's)
"""

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector


driver = webdriver.Chrome('/Users/Audrey Chu/Desktop/chromedriver')
driver.get('https://www.google.com')

# Search for people by name, school, and major
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in/ AND "Rebecca Lindner" \
                       AND "Columbia" AND "Data Science"')
search_query.send_keys(Keys.RETURN)

# Take the first URL from google search
linkedin_url = driver.find_elements_by_class_name('iUh30')[0].text

# Rebecca's LI page
driver.get(linkedin_url)
sel = Selector(text = driver.page_source)

name = sel.xpath('//*[starts-with(@class, "topcard__name")]/text()').extract_first()




# Terminates the application
driver.quit()