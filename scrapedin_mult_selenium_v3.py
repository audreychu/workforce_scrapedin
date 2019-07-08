# -*- coding: utf-8 -*-
"""
7/2/2019

Bring in lookup data

"""

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from pandas import ExcelWriter
import pandas as pd
import numpy as np



# Import CSV to collect data
lookup = pd.read_csv(r"C:\Users\Audrey Chu\Desktop\workforce_scrapedin\May2019_PCA_Lookup.csv")
l_name = lookup['Contact: Full Name'].astype(str)
l_org = lookup['Organization: Organization Name'].astype(str)
l_deg = lookup['Degree Major 1'].astype(str)


# Lookup criteria
# names_ = ['"Rebecca Lindner"', '"Audrey Chu"', '"Abigail Collins"']
# schools_ = ['"Columbia"', '"UC Davis"', '"Georgia Institute of Technology"']
# majors_ = ['"Data Science"', '"Statistics"', '"Computer Science"']

# format lookup, create list comp
# for (a, b, c) in zip(names_, schools_, majors_):
#    print ('site:linkedin.com/in/ AND '+a+' AND '+b+' AND '+c)
# criteria_old = ['site:linkedin.com/in/ AND '+a+' AND '+b+' AND '+c for a,b,c in zip(names_, schools_, majors_)]
criteria = ['site:linkedin.com/in/ AND '+a+' AND '+b+' AND '+c for a,b,c in zip(l_name, l_org, l_deg)]


final = pd.DataFrame()

for i in criteria:    
    driver = webdriver.Chrome('/Users/Audrey Chu/Desktop/chromedriver')
    driver.get('https://www.google.com')
    
    # Search for people by name, school, and major
    search_query = driver.find_element_by_name('q')
    # search_query.send_keys('site:linkedin.com/in/ AND "Rebecca Lindner" \
    #                       AND "Columbia" AND "Data Science"')
    search_query.send_keys(i)
    search_query.send_keys(Keys.RETURN)
    
    # Take the first URL from google search -- will need to expand later
    linkedin_url = driver.find_elements_by_class_name('iUh30')[0].text
    
    # Return LI page
    driver.get(linkedin_url)
    sel = Selector(text = driver.page_source)
    
    # Variables of interest
    name = sel.xpath('//*[starts-with(@class, "topcard__name")]/text()').extract_first()
    job_nogrowth = sel.xpath('//*[starts-with(@class, "section-item__title position__title")]/text()').getall()
    job_growth = sel.xpath('//*[starts-with(@class, "section-item__title experience-group-item__title")]/text()').getall()
    co_nogrowth = sel.xpath('//*[starts-with(@class, "position__company-name")]/text()').getall()
    co_growth = sel.xpath('//*[starts-with(@class, "section-item__title experience-group-header__title")]/text()').getall()
    schools = sel.xpath('//*[starts-with(@class, "section-item__title education-item__title")]/text()').getall()
    degrees = sel.xpath('//*[starts-with(@class, "education-item__degree-info")]/text()').getall()
    location = sel.xpath('//*[starts-with(@class, "topcard__location")]/text()').extract_first()
    industry = sel.xpath('//*[starts-with(@class, "topcard__industry")]/text()').extract_first()
    
    # time ranges include education. No difference between g/ng
    # How do we know which job category starts/matches with time ranges?
    # 4 #### marks education. Anything after includes volunteering, certifs, etc.
    t_start = sel.xpath('//*[starts-with(@class, "date-range__start-date")]/text()').getall()
    t_end = sel.xpath('//*[starts-with(@class, "date-range__end-date")]/text()').getall()
    
    
    # Create dataframe
    data = [[name, schools, degrees, location, industry, job_nogrowth, job_growth, co_nogrowth, co_growth, t_start, t_end]]
    final = final.append(data)
    
    driver.quit()




# Format final data frame
final.columns = ['Name'
                 , 'Schools'
                 , 'Degrees'
                 , 'Location'
                 , 'Industry'
                 , 'Job_NoGrowth'
                 , 'Job_Growth'
                 , 'Co_NoGrowth'
                 , 'Co_Growth'
                 , 'T_Start'
                 , 'T_End']
final = final.reset_index(drop = True)
final.to_excel(r"C:\Users\Audrey Chu\Desktop\workforce_scrapedin\ThreeTest.xlsx")